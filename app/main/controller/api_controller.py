from flask import request
from flask_restx import Resource
from typing import Dict, Tuple

from app.main.controller.dtos.api_dto import ApiDto

from app.main.utils.decorators import role_token_required
from app.main.service.api_service import ApiManagement

from app.main.utils.roles import Role

api = ApiDto.api


create_category_request = ApiDto.create_category_request
create_category_response = ApiDto.create_category_response
@api.route('/categories/create')
class CreateCategory(Resource):
    @api.doc('create category')
    @api.expect(create_category_request, validate=True)
    @api.response(201,'success',create_category_response)
    @role_token_required([Role.ADMIN])
    def post(self):
        post_data = request.json
        return ApiManagement.create_category(request,data=post_data)

categories_list_response = ApiDto.categories_list_response
@api.route('/categories')
class GetCategories(Resource):
    @api.doc('get categories')
    @api.response(200, 'Success',categories_list_response)
    def get(self) -> Tuple[Dict[str, any], int]:
        return ApiManagement.get_all_categories()
    

create_api_request = ApiDto.create_api_request
create_api_response = ApiDto.create_api_response
@api.route('/create')
class CreateApi(Resource):
    @api.doc('create api')
    @api.expect(create_api_request, validate=True)
    @api.response(201, 'Success', create_api_response)
    @role_token_required([Role.SUPPLIER])
    def post(self):
        post_data = request.json
        return ApiManagement.create_api(request,data=post_data)


apis_list_response = ApiDto.apis_list_response
@api.route('/')
class GetApis(Resource):
    @api.doc('get apis')
    @api.param('page', 'The page number')
    @api.param('per_page', 'The number of items per page')
    @api.param('category_ids', 'The category ID', type='array')
    @api.param('status', 'The status of the apis')
    @api.response(200, 'Success', apis_list_response)
    def get(self) ->Tuple[Dict[str, any], int]:
        return ApiManagement.get_all_apis(request)


@api.route('/mine')
class GetApis(Resource):
    @api.doc('get the logged in supplier apis')
    @api.param('page', 'The page number')
    @api.param('per_page', 'The number of items per page')
    @api.param('category_ids', 'The category ID', type='array')
    @api.param('status', 'The status of the apis')
    @api.response(200, 'Success', apis_list_response)
    def get(self) ->Tuple[Dict[str, any], int]:
        return ApiManagement.get_logged_in_supplier_apis(request)



update_api_request = ApiDto.update_api_request
update_api_response = ApiDto.update_api_response
@api.route('/<int:id>/update')
class UpdateApi(Resource):
    @api.doc('update api')
    @api.expect(update_api_request, validate=True)
    @api.response(200, 'Success', update_api_response)
    @role_token_required([Role.SUPPLIER])
    def patch(self, id):
        post_data = request.json
        return ApiManagement.update_api_info(request,api_id=id,data=post_data)


# this route is for getting an api by id
api_info_response = ApiDto.api_info_response
@api.route('/<int:id>')
class GetApiById(Resource):
    @api.doc('get api by id')
    @api.response(200, 'Success', api_info_response)
    def get(self, id):
        return ApiManagement.get_single_api(api_id=id)

# this route is for activating a disabled api, supplier cant activate an api that is disabled by an admin
# supplier can only activate his own api
activate_api_response = ApiDto.activate_api_response
@api.route('/<int:id>/activate')
class ActivateApi(Resource):
    @api.doc('activate api')
    @api.response(200, 'Success', activate_api_response)
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id):
        return ApiManagement.activate_api(request,api_id=id)

# this route is for deactivating an active api 
# supplier can only deactivate his own api
activate_api_response = ApiDto.activate_api_response
@api.route('/<int:id>/deactivate')
class DeactivateApi(Resource):
    @api.doc('deactivate api')
    @api.response(200, 'Success', activate_api_response)
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id):
        return ApiManagement.disable_api(request,api_id=id)

# this route is for creating a new version of an api (version_name,base_url,headers,endpoints)

create_api_version_request = ApiDto.create_api_version_request
create_api_version_response = ApiDto.create_api_version_response
@api.route('/<int:id>/versions/create')
class CreateVersion(Resource):
    @api.doc('create version')
    @api.expect(create_api_version_request, validate=True)
    @api.response(201, 'Success', create_api_version_response)
    @role_token_required([Role.SUPPLIER])
    def post(self, id):
        post_data = request.json
        return ApiManagement.create_version(request,api_id=id,data=post_data)

# this route is for getting all versions of an api
@api.route('/<int:id>/versions',doc=False)
class GetVersions(Resource):
    @api.doc('get versions')
    @api.response(200, 'Success')
    def get(self, id):
        return "Not implemented yet"

# this route is for getting a version of an api by id
@api.route('/<int:id>/versions/<string:version>',doc=False)
class GetVersion(Resource):
    @api.doc('get version')
    @api.response(200, 'Success')
    def get(self, id, version):
        return "Not implemented yet"

# this route is for activating a version of an api, supplier can only activate his own version
# supplier cant activate a version that is disabled by an admin
@api.route('/<int:id>/versions/<string:version>/activate',doc=False)
class ActivateVersion(Resource):
    @api.doc('activate version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id, version):
        return "Not implemented yet"
    
# this route is for deactivating a version of an api, supplier can only deactivate his own version
@api.route('/<int:id>/versions/<string:version>/deactivate',doc=False)
class DeactivateVersion(Resource):
    @api.doc('deactivate version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id, version):
        return "Not implemented yet"

# this route is for deleting a version of an api, supplier can only delete his own version
@api.route('/<int:id>/versions/<string:version>/delete',doc=False)
class DeleteVersion(Resource):
    @api.doc('delete version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version):
        return "Not implemented yet"

# this route is for adding a new header to a version of an api
@api.route('/<int:id>/versions/<string:version>/headers/create',doc=False)
class CreateHeader(Resource):
    @api.doc('create header')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        return "Not implemented yet"

# this route is for deleting a header from a version of an api
@api.route('/<int:id>/versions/<string:version>/headers/<int:header_id>/delete',doc=False)
class DeleteHeader(Resource):
    @api.doc('delete header')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version, header_id):
        return "Not implemented yet"

# this route is for updating a header from a version of an api
@api.route('/<int:id>/versions/<string:version>/headers/<int:header_id>/update',doc=False)
class UpdateHeader(Resource):
    @api.doc('update header')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def patch(self, id, version, header_id):
        return "Not implemented yet"

# this route is for adding a new endpoint to a version of an api (endpoints are only for documentation purposes)
@api.route('/<int:id>/versions/<string:version>/endpoints/create',doc=False)
class CreateEndpoint(Resource):
    @api.doc('create endpoint')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        return "Not implemented yet"

# this route is for deleting an endpoint from a version of an api
@api.route('/<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/delete',doc=False)
class DeleteEndpoint(Resource):
    @api.doc('delete endpoint')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version, endpoint_id):
        return "Not implemented yet"

# this route is for updating an endpoint from a version of an api
@api.route('/<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/update',doc=False)
class UpdateEndpoint(Resource):
    @api.doc('update endpoint')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def patch(self, id, version, endpoint_id):
        return "Not implemented yet"

# this route is for testing a version of API
# the id is the of the api, version is the version of the api, and params are the request parameters
# First We check if the api id exists and is not disabled
# Then we check if the version exists and is not disabled
# Then we send a request to base_url/params with the headers and method specified in the version
# We return the response
# TODO: The request must be from a whitelist domains
@api.route('/test/<int:id>/<string:version>/<path:params>',doc=False)
class TestEndpoint(Resource):
    @api.doc('test endpoint')
    @api.response(200, 'Success')
    def get(self, id, version, params): # the method will be get for now
        print(params)
        print(id)
        print(version)
        return "Not implemented yet"

# this route is for subscribing to a plan of an api
# this will be without payment for now
@api.route('/<int:id>/plans/<string:plan>/subscribe',doc=False)
class SubscribePlan(Resource):
    @api.doc('subscribe plan')
    @api.response(200, 'Success')
    @role_token_required([Role.USER])
    def post(self, id, plan):
        return "Not implemented yet"

# this route if for creating an api key that will be used to access the api
# before generating the api key we must check if the user has an active subscription to the api
@api.route('/<int:id>/api_key/create',doc=False)
class CreateApiKey(Resource):
    @api.doc('create api key')
    @api.response(201, 'Success')
    @role_token_required([Role.USER])
    def post(self, id):
        return "Not implemented yet"

# this route is for deleting an api key
@api.route('/<int:id>/api_key/delete',doc=False)
class DeleteApiKey(Resource):
    @api.doc('delete api key')
    @api.response(200, 'Success')
    @role_token_required([Role.USER])
    def delete(self, id):
        return "Not implemented yet"
    
# this route is for getting all api keys of an api
@api.route('/<int:id>/api_keys',doc=False)
class GetApiKeys(Resource):
    @api.doc('get api keys')
    @api.response(200, 'Success')
    @role_token_required([Role.USER])
    def get(self, id):
        return "Not implemented yet"
    
@api.route('/call/<int:id>/<string:version>/<path:params>',doc=False)
class CallApi(Resource):
    @api.doc('call api')
    @api.response(200, 'Success')
    def get(self, id, version, params):
        api_key = request.headers.get('X-API-KEY')
        api_id = id
        version = version
        body = request.get_json()
        # check if the api exists
        # check if the api is active
        # check if the version exists
        # check if the version is active
        # check if the api_key exists
        # check if the api_key is active
        # check if the api_key belongs to the api
        # check if user has an active (not expired) subscription to the api
        # check if the user has enough requests left
        # call the api with base_url of the version and the params and headers of the version
        # add an api request to the database with the required info
        # return the response
        return "Not implemented yet"