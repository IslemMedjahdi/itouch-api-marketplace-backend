from flask import request
from flask_restx import Resource

from typing import Dict, Tuple

from app.main.controller.dtos.user_dto import UserDto


api = UserDto.api


user_info_response = UserDto.user_info_response
@api.route('/<string:user_id>')
class UserInfo(Resource):
    @api.doc('user info')
    @api.response(200, 'Success', user_info_response)
    def get(self) -> Tuple[Dict[str, any], int]:
        return "not implemented yet", 404


users_list_response = UserDto.users_list_response
@api.route("/")
class UsersList(Resource):
    @api.doc('list of registered users')
    @api.param('page', 'The page number')
    @api.param('per_page', 'The number of items per page')
    @api.response(200, 'Success', UserDto.users_list_response)
    def get(self) -> Tuple[Dict[str, any], int]:
        return "not implemented yet", 404