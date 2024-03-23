from typing import Callable, List
from functools import wraps
from flask import request, g
from http import HTTPStatus
from app.main.service.auth_service import Auth


def require_authentication(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        response, status = Auth.get_logged_in_user(request)
        if status != HTTPStatus.OK:
            return response, status
        g.user = response.get("data")
        return f(*args, **kwargs)

    return decorated


def role_token_required(allowed_roles: List[str]) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            response, status = Auth.get_logged_in_user(request)

            if status != HTTPStatus.OK:
                return response, status

            role = response.get("data").get("role")

            if role not in allowed_roles:
                response = {
                    "status": "fail",
                    "message": "You do not have permission to access this resource",
                }
                return response, HTTPStatus.UNAUTHORIZED

            g.user = response.get("data")

            return f(*args, **kwargs)

        return decorated

    return decorator
