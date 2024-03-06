from flask import request
from flask_restx import Resource

from typing import Dict, Tuple
from app.main.service.user_service import UserManagement
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
        #print("user_id", user_id)
        return UserManagement.get_single_user(user_id) 

new_user_request = UserDto.new_user_request
new_user_response = UserDto.new_user_response
users_list_response = UserDto.users_list_response
@api.route("/")
class UsersList(Resource):
    @api.doc('list of registered users')
    @api.param('page', 'The page number')
    @api.param('per_page', 'The number of items per page')
    @api.response(200, 'Success', UserDto.users_list_response)
    @role_token_required([Role.ADMIN])
    def get(self) -> Tuple[Dict[str, any], int]:
        return UserManagement.get_all_users(request)
    @api.doc("Create user")
    @api.expect(new_user_request, validate=True)
    @api.response(200,'success',new_user_response)
    @role_token_required([Role.ADMIN])
    def post(self) -> Tuple[Dict[str, any], int]:
        post_data = request.json
        return UserManagement.create_user(data=post_data)
    
suspend_user_response = UserDto.suspend_user_response
@api.route('/<int:user_id>/suspend')
class SuspendUser(Resource):
    @api.doc('suspend user')
    @api.response(200, 'Success', suspend_user_response)
    @role_token_required([Role.ADMIN])
    def patch(self,user_id: int) -> Tuple[Dict[str, any], int]:
        return UserManagement.suspend_user(user_id)
    
activate_user_response = UserDto.activate_user_response
@api.route('/<int:user_id>/activate')
class ActivateUser(Resource):
    @api.doc('activate user')
    @api.response(200, 'Success', activate_user_response)
    @role_token_required([Role.ADMIN])
    def patch(self,user_id: int) -> Tuple[Dict[str, any], int]:
        return UserManagement.activate_user(user_id)

new_supplier_request = UserDto.new_supplier_request
new_supplier_response = UserDto.new_supplier_response
@api.route('/suppliers')
class NewSupplier(Resource):
    @api.doc("Create supplier")
    @api.expect(new_supplier_request, validate=True)
    @api.response(201,'success',new_supplier_response)
    @role_token_required([Role.ADMIN])
    def post(self) -> Tuple[Dict[str, any], int]:
        post_data = request.json
        return UserManagement.create_supplier(data=post_data)


update_user_request = UserDto.update_user_request
update_user_response = UserDto.update_user_response
@api.route('/update')
class UpdateMe(Resource):
    @api.doc("Update the user informations")
    @api.expect(update_user_request, validate=True)
    @api.response(200,'success',update_user_response)
    def patch(self) -> Tuple[Dict[str, any], int]:
        post_data = request.json
        return UserManagement.update_logged_in_user_info(request,data=post_data)

update_password_request = UserDto.update_password_request
update_password_response = UserDto.update_password_response
@api.route('/password')
class UpdatePassword(Resource):
    @api.doc("Update the logged in user password")
    @api.expect(update_password_request, validate=True)
    @api.response(200,'success',update_password_response)
    def patch(self) -> Tuple[Dict[str, any], int]:
        post_data = request.json
        return UserManagement.update_logged_in_user_password(request,data=post_data)



