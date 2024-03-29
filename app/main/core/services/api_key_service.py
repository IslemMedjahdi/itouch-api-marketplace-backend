from app.main.model.api_subscription_model import ApiSubscription
from app.main.utils.exceptions import NotFoundError


class ApiKeyService:

    def create_api_key(self, subscription_id: int, user_id: int):
        subscription = ApiSubscription.query.filter_by(
            id=subscription_id, user_id=user_id
        ).first()

        if subscription is None:
            raise NotFoundError(f"No subscription found with id: {subscription_id}")

        if subscription.max_requests <= 0:
            raise NotFoundError(
                "Subscription has no requests left, Please Renew Subscription"
            )

        raise Exception("Not Implemented Yet")
