import math
from typing import Dict
from app.main.model.api_category_model import ApiCategory
from app.main.model.api_model import ApiModel
from app.main.model.api_plan_model import ApiPlan
from app.main.model.user_model import User
from app.main import db
from app.main.utils.exceptions import NotFoundException, BadRequestException
from app.main.core.lib.media_manager import MediaManager


class ApiService:

    def __init__(self, media_manager: MediaManager):
        self.media_manager = media_manager

    def create_api(self, data: Dict, user_id: str):
        if (
            ApiCategory.query.filter_by(id=data.get("category_id", None)).first()
            is None
        ):
            raise NotFoundException(
                "No API Category found with id: {}".format(
                    data.get("category_id", None)
                )
            )

        ApiService.__validate_plans(self, data.get("plans", []))

        new_api = ApiModel(
            name=data.get("name", None),
            description=data.get("description", None),
            category_id=data.get("category_id", None),
            supplier_id=user_id,
        )

        db.session.add(new_api)
        db.session.commit()

        for plan in data.get("plans", []):
            new_plan = ApiPlan(
                name=plan.get("name", None),
                price=plan.get("price", None),
                max_requests=plan.get("max_requests", None),
                duration=plan.get("duration", None),
                api_id=new_api.id,
            )
            db.session.add(new_plan)

    def __validate_plans(self, plans: Dict):
        names = []
        for plan in plans:
            if plan.get("name") in names:
                raise BadRequestException(
                    "Duplicate plan name found: {}".format(plan.name)
                )
            if plan.get("price") < 0:
                raise BadRequestException("Price cannot be negative")
            if plan.get("max_requests") < 0:
                raise BadRequestException("Max requests cannot be negative")
            if plan.get("duration") < 0:
                raise BadRequestException("Duration cannot be negative")
            names.append(plan.get("name"))

    def get_apis(self, query_params: Dict):
        page = int(query_params.get("page", 1))
        per_page = int(query_params.get("per_page", 10))
        status = query_params.get("status", None)
        category_ids = query_params.get("categoryIds", [])
        supplier_id = query_params.get("supplierId", None)

        query = (
            db.session.query(ApiModel, User, ApiCategory)
            .join(User, ApiModel.supplier_id == User.id)
            .join(ApiCategory, ApiModel.category_id == ApiCategory.id)
        )

        if status is not None:
            query = query.filter(ApiModel.status == status)

        if category_ids:
            query = query.filter(ApiModel.category_id.in_(category_ids))

        if supplier_id is not None:
            query = query.filter(ApiModel.supplier_id == supplier_id)

        total = query.count()

        pagination = {
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": math.ceil(total / per_page),
        }

        query = query.limit(per_page).offset((page - 1) * per_page)

        apis = query.all()

        result = []
        for api, user, category in apis:
            api_dict = {
                "id": api.id,
                "name": api.name,
                "description": api.description,
                "category_id": api.category_id,
                "category": {
                    "id": category.id,
                    "name": category.name,
                },
                "supplier_id": api.supplier_id,
                "supplier": {
                    "id": user.id,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                },
                "status": api.status,
                "created_at": api.created_at.isoformat(),
                "updated_at": api.updated_at.isoformat(),
                "image": self.media_manager.get_media_url_by_id(
                    api.id
                ),  # TODO: this will be api.image_id
            }
            result.append(api_dict)

        return result, pagination

    def update_api(self, api_id, supplier_id, data):
        api = ApiModel.query.filter_by(id=api_id, supplier_id=supplier_id).first()
        if api is None:
            raise NotFoundException("No API found with id: {}".format(api_id))

        if api.supplier_id != supplier_id:
            raise BadRequestException("You are not the owner of the API")

        if data.get("category_id", None) is not None:
            if (
                ApiCategory.query.filter_by(id=data.get("category_id", None)).first()
                is None
            ):
                raise NotFoundException(
                    "No API Category found with id: {}".format(
                        data.get("category_id", None)
                    )
                )
            api.category_id = data.get("category_id", None)

        if data.get("name", None) is not None:
            api.name = data.get("name", None)

        if data.get("description", None) is not None:
            api.description = data.get("description", None)

        db.session.commit()

    def get_api_by_id(self, api_id):
        query = (
            db.session.query(ApiModel, User, ApiCategory)
            .join(User, ApiModel.supplier_id == User.id)
            .join(ApiCategory, ApiModel.category_id == ApiCategory.id)
        )

        api = query.filter(ApiModel.id == api_id).first()

        if api is None:
            raise NotFoundException("No API found with id: {}".format(api_id))

        api, user, category = api

        plans = ApiPlan.query.filter_by(api_id=api.id).all()

        api_dict = {
            "id": api.id,
            "name": api.name,
            "description": api.description,
            "category_id": api.category_id,
            "category": {
                "id": category.id,
                "name": category.name,
            },
            "supplier_id": api.supplier_id,
            "supplier": {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
            },
            "created_at": api.created_at.isoformat(),
            "updated_at": api.updated_at.isoformat(),
            "image": self.media_manager.get_media_url_by_id(api.id),
            "plans": [
                {
                    "name": plan.name,
                    "description": plan.description,
                    "price": plan.price,
                    "max_requests": plan.max_requests,
                    "duration": plan.duration,
                }
                for plan in plans
            ],
        }

        return api_dict

    def activate_api(self, api_id: int, supplier_id: int, role: str):
        api = ApiModel.query.filter_by(id=api_id).first()
        if api is None:
            raise NotFoundException("No API found with id: {}".format(api_id))

        if role == "supplier" and api.supplier_id != supplier_id:
            raise BadRequestException("You are not the owner of the API")

        api.status = "active"

        db.session.commit()

    def deactivate_api(self, api_id: int, supplier_id: int, role: str):
        api = ApiModel.query.filter_by(id=api_id).first()
        if api is None:
            raise NotFoundException("No API found with id: {}".format(api_id))

        if role == "supplier" and api.supplier_id != supplier_id:
            raise BadRequestException("You are not the owner of the API")

        api.status = "inactive"

        db.session.commit()
