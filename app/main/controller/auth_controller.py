from flask import request
from flask_restx import Resource

from typing import Dict, Tuple

from app.main.service.auth_service import Auth
from app.main.controller.dtos.auth_dto import AuthDto


api = AuthDto.api


user_login_request = AuthDto.user_login_request
user_login_response = AuthDto.user_login_response
@api.route('/login')
class UserLogin(Resource):
    @api.doc('user login')
    @api.expect(user_login_request, validate=True)
    @api.response(200, 'Success', user_login_response)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return Auth.login_user(data=post_data)

user_register_request = AuthDto.user_register_request
user_register_response = AuthDto.user_register_response
@api.route('/register')
class UserRegister(Resource):
    @api.doc('user register')
    @api.expect(user_register_request, validate=True)
    @api.response(201, 'Success', user_register_response)
    def post(self) -> Tuple[Dict[str, str], int]:
        post_data = request.json
        return Auth.register_user(data=post_data)
    

user_info_response = AuthDto.user_info_response
@api.route('/me')
class UserInfo(Resource):
    @api.doc('user info')
    @api.response(200, 'Success', user_info_response)
    def get(self) -> Tuple[Dict[str, any], int]:
        return Auth.get_logged_in_user(request)