import math
from typing import Dict
from app.main.model.api_model import ApiModel
from app.main.model.api_request_model import ApiRequest
from app.main.model.user_model import User
from app.main import db
from app.main.utils.exceptions import NotFoundError, BadRequestError


class ApiRequestService:

    def get_api_requests(self, query_params: Dict, user_id: str, api_id: int):
        page = int(query_params.get("page", 1))
        per_page = int(query_params.get("per_page", 10))
        http_status = query_params.get("http_status", None)
        api_version = query_params.get("version")
        start_date = query_params.get("start_date")
        end_date = query_params.get("end_date")

        query = (
            db.session.query(ApiRequest, ApiModel, User)
            .join(ApiModel, ApiRequest.api_id == ApiModel.id)
            .join(
                User,
                ApiRequest.user_id == User.id,
            )
        )

        api = ApiModel.query.filter_by(id=api_id).first()

        if api is None:
            raise NotFoundError("No API found with id: {}".format(api_id))

        if api.supplier_id != user_id:
            raise BadRequestError("You are not allowed to view this requests")

        query = query.filter(ApiRequest.api_id == api_id)

        if http_status is not None:
            query = query.filter(ApiRequest.http_status == http_status)

        if api_version is not None:
            api_version = api_version.lower()
            query = query.filter(ApiRequest.api_version == api_version)

        if start_date is not None:
            query = query.filter(ApiRequest.request_at >= start_date)

        if end_date is not None:
            query = query.filter(ApiRequest.response_at <= end_date)

        total = query.count()

        pagination = {
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": math.ceil(total / per_page),
        }

        query = query.limit(per_page).offset((page - 1) * per_page)

        requests = query.all()

        result = []
        for request, api, user in requests:
            request_dict = {
                "id": request.id,
                "api_id": api.id,
                "api": {
                    "id": api.id,
                    "name": api.name,
                    "supplier_id": api.supplier_id,
                },
                "api_version": request.api_version,
                "user_id": user.id,
                "user": {
                    "id": user.id,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                },
                "request_url": request.request_url,
                "request_method": request.request_method,
                "http_status": request.http_status,
                "request_at": request.request_at.isoformat(),
                "response_at": request.response_at.isoformat(),
                "response_time": request.response_time,
            }
            result.append(request_dict)

        return result, pagination
