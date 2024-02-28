from flask import request
from flask_restx import Resource

from typing import Dict, Tuple

from app.main.controller.dtos.user_dto import UserDto

from app.main.utils.decorators import role_token_required

from app.main.utils.roles import Role

api = UserDto.api


user_info_response = UserDto.user_info_response
@api.route('/<int:user_id>')
class UserInfo(Resource):
    @api.doc('user info')
    @api.response(200, 'Success', user_info_response)
    @role_token_required([Role.ADMIN])
    def get(self,user_id: int) -> Tuple[Dict[str, any], int]:
        user_id = request.args.get('user_id')
        print("user_id", user_id)
        return "not implemented yet", 404


users_list_response = UserDto.users_list_response
@api.route("/")
class UsersList(Resource):
    @api.doc('list of registered users')
    @api.param('page', 'The page number')
    @api.param('per_page', 'The number of items per page')
    @api.response(200, 'Success', UserDto.users_list_response)
    @role_token_required([Role.ADMIN])
    def get(self) -> Tuple[Dict[str, any], int]:
        return "not implemented yet", 404
    
suspend_user_response = UserDto.suspend_user_response
@api.route('/<int:user_id>/suspend')
class SuspendUser(Resource):
    @api.doc('suspend user')
    @api.response(200, 'Success', suspend_user_response)
    @role_token_required([Role.ADMIN])
    def patch(self,user_id: int) -> Tuple[Dict[str, any], int]:
        return "not implemented yet", 404
    
activate_user_response = UserDto.activate_user_response
@api.route('/<int:user_id>/activate')
class ActivateUser(Resource):
    @api.doc('activate user')
    @api.response(200, 'Success', activate_user_response)
    @role_token_required([Role.ADMIN])
    def patch(self,user_id: int) -> Tuple[Dict[str, any], int]:
        return "not implemented yet", 404

new_supplier_request = UserDto.new_supplier_request
new_supplier_response = UserDto.new_supplier_response
@api.route('/suppliers')
class NewSupplier(Resource):
    @api.doc("Create supplier")
    @api.expect(new_supplier_request, validate=True)
    @api.response(200,'success',new_supplier_response)
    @role_token_required([Role.ADMIN])
    def post(self) -> Tuple[Dict[str, any], int]:
        return "not implemented yet", 404