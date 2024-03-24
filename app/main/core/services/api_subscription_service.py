import json
from datetime import datetime, timedelta

from flask import Request

from app.main import db

from app.main.core.lib.chargily_api import ChargilyApi
from app.main.model.api_model import ApiModel
from app.main.model.api_plan_model import ApiPlan
from app.main.model.api_subscription_model import ApiSubscription
from app.main.utils.exceptions import NotFoundError, BadRequestError


class ApiSubscriptionService:
    def __init__(self, chargily_api: ChargilyApi):
        self.chargily_api = chargily_api

    def create_charigly_checkout(
        self, api_id: str, plan_name: str, user_id: str, redirect_url: str
    ) -> str:
        api = ApiModel.query.filter_by(id=api_id).first()
        if api is None:
            raise NotFoundError(f"No API found with id: {api_id}")

        plan = ApiPlan.query.filter_by(api_id=api_id, name=plan_name).first()
        if plan is None:
            raise NotFoundError(f"No plan found with name: {plan_name}")

        price_id = plan.chargily_price_id

        if price_id is None:
            raise BadRequestError("Failed to get price id from chargily API")

        checkout_url = self.chargily_api.create_checkout(
            price_id=price_id,
            redirect_url=redirect_url,
            metadata={"api_id": api_id, "plan_name": plan_name, "user_id": user_id},
        )

        if checkout_url is None:
            raise BadRequestError("Failed to create checkout URL in chargily API")

        return checkout_url

    def handle_chargily_webhook(self, request: Request):
        signature = request.headers.get("signature")

        body = request.json

        if signature is None:
            raise BadRequestError("No signature found in headers")

        if body is None:
            raise BadRequestError("No body found in request")

        payload = body.decode("utf-8")

        if not self.chargily_api.verify_webhook_signature(payload, signature):
            raise BadRequestError("Invalid signature, STOP TRYING TO HACK US")

        event = json.loads(payload)

        if event["type"] == "checkout.paid":
            checkout = event["data"]

            api_id = checkout["metadata"]["api_id"]
            plan_name = checkout["metadata"]["plan_name"]
            user_id = checkout["metadata"]["user_id"]

            api = ApiModel.query.filter_by(id=api_id).first()
            if api is None:
                raise NotFoundError(f"No API found with id: {api_id}")

            plan = ApiPlan.query.filter_by(api_id=api_id, name=plan_name).first()
            if plan is None:
                raise NotFoundError(f"No plan found with name: {plan_name}")

            duration = plan.duration

            subscription = ApiSubscription(
                api_id=api_id,
                plan_name=plan_name,
                user_id=user_id,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=duration),
                max_requests=plan.max_requests,
                status="active",
            )

            db.session.add(subscription)
            db.session.commit()
