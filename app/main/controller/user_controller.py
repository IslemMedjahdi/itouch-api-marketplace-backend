from flask import request
from flask_restx import Resource

from typing import Dict, Tuple
from app.main.service.user_service import UserManagement
from app.main.controller.dtos.user_dto import UserDto

from app.main.utils.decorators import role_token_required

api = UserDto.api


user_info_response = UserDto.user_info_response
@api.route('/<int:user_id>')
class UserInfo(Resource):
    @api.doc('user info')
    @api.response(200, 'Success', user_info_response)
    @role_token_required(['admin'])
    def get(self,user_id: int) -> Tuple[Dict[str, any], int]:
        #print("user_id", user_id)
        return UserManagement.get_single_user(user_id) 


users_list_response = UserDto.users_list_response
@api.route("/")
class UsersList(Resource):
    @api.doc('list of registered users')
    @api.param('page', 'The page number')
    @api.param('per_page', 'The number of items per page')
    @api.response(200, 'Success', UserDto.users_list_response)
    @role_token_required(['admin'])
    def get(self) -> Tuple[Dict[str, any], int]:
        return UserManagement.get_all_users(request)
    
suspend_user_response = UserDto.suspend_user_response
@api.route('/<int:user_id>/suspend')
class SuspendUser(Resource):
    @api.doc('suspend user')
    @api.response(200, 'Success', suspend_user_response)
    @role_token_required(['admin'])
    def patch(self,user_id: int) -> Tuple[Dict[str, any], int]:
        return UserManagement.suspend_user(user_id)
    
activate_user_response = UserDto.activate_user_response
@api.route('/<int:user_id>/activate')
class ActivateUser(Resource):
    @api.doc('activate user')
    @api.response(200, 'Success', activate_user_response)
    @role_token_required(['admin'])
    def patch(self,user_id: int) -> Tuple[Dict[str, any], int]:
        return UserManagement.activate_user(user_id)

new_supplier_request = UserDto.new_supplier_request
new_supplier_response = UserDto.new_supplier_response
@api.route('/suppliers')
class NewSupplier(Resource):
    @api.doc("Create supplier")
    @api.expect(new_supplier_request, validate=True)
    @api.response(200,'success',new_supplier_response)
    @role_token_required(['admin'])
    def post(self) -> Tuple[Dict[str, any], int]:
        post_data = request.json
        return UserManagement.create_supplier(data=post_data)