from flask import request
from flask_restx import Resource

from app.main.controller.dtos.api_dto import ApiDto

from app.main.utils.decorators import role_token_required

from app.main.utils.roles import Role

api = ApiDto.api


# this route is for creating a new category
@api.route('/categories/create')
class CreateCategory(Resource):
    @api.doc('create category')
    @api.response(201, 'Success')
    @role_token_required([Role.ADMIN])
    def post(self):
        return "Not implemented yet"

# this route is for getting all categories    
@api.route('/categories')
class GetCategories(Resource):
    @api.doc('get categories')
    @api.response(200, 'Success')
    def get(self):
        return "Not implemented yet"
    

# this route for creating a new api: (name, description, category_id, supplier_id)
@api.route('/create')
class CreateApi(Resource):
    @api.doc('create api')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self):
        return "Not implemented yet"


# this route is for getting all apis
@api.route('/')
class GetApis(Resource):
    @api.doc('get apis')
    @api.response(200, 'Success')
    def get(self):
        return "Not implemented yet"

# this route is for deleting an api
@api.route('/<int:id>/delete')
class DeleteApi(Resource):
    @api.doc('delete api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id):
        return "Not implemented yet"

# this route is for updating an api (name,description,category,plans)
@api.route('/<int:id>/update')
class UpdateApi(Resource):
    @api.doc('update api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def patch(self, id):
        return "Not implemented yet"

# this route is for getting an api by id
@api.route('/<int:id>')
class GetApiById(Resource):
    @api.doc('get api by id')
    @api.response(200, 'Success')
    def get(self, id):
        return "Not implemented yet"

# this route is for activating a disabled api, supplier cant activate an api that is disabled by an admin
# supplier can only activate his own api
@api.route('/<int:id>/activate')
class ActivateApi(Resource):
    @api.doc('activate api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id):
        return "Not implemented yet"

# this route is for deactivating an active api 
# supplier can only deactivate his own api
@api.route('/<int:id>/deactivate')
class DeactivateApi(Resource):
    @api.doc('deactivate api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id):
        return "Not implemented yet"

# this route is for creating a new version of an api (version_name,base_url,headers,endpoints)
@api.route('/<int:id>/versions/create')
class CreateVersion(Resource):
    @api.doc('create version')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id):
        return "Not implemented yet"

# this route is for getting all versions of an api
@api.route('/<int:id>/versions')
class GetVersions(Resource):
    @api.doc('get versions')
    @api.response(200, 'Success')
    def get(self, id):
        return "Not implemented yet"

# this route is for getting a version of an api by id
@api.route('/<int:id>/versions/<string:version>')
class GetVersion(Resource):
    @api.doc('get version')
    @api.response(200, 'Success')
    def get(self, id, version):
        return "Not implemented yet"

# this route is for activating a version of an api, supplier can only activate his own version
# supplier cant activate a version that is disabled by an admin
@api.route('/<int:id>/versions/<string:version>/activate')
class ActivateVersion(Resource):
    @api.doc('activate version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id, version):
        return "Not implemented yet"
    
# this route is for deactivating a version of an api, supplier can only deactivate his own version
@api.route('/<int:id>/versions/<string:version>/deactivate')
class DeactivateVersion(Resource):
    @api.doc('deactivate version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id, version):
        return "Not implemented yet"

# this route is for deleting a version of an api, supplier can only delete his own version
@api.route('/<int:id>/versions/<string:version>/delete')
class DeleteVersion(Resource):
    @api.doc('delete version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version):
        return "Not implemented yet"

# this route is for adding a new header to a version of an api
@api.route('/<int:id>/versions/<string:version>/headers/create')
class CreateHeader(Resource):
    @api.doc('create header')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        return "Not implemented yet"

# this route is for deleting a header from a version of an api
@api.route('/<int:id>/versions/<string:version>/headers/<int:header_id>/delete')
class DeleteHeader(Resource):
    @api.doc('delete header')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version, header_id):
        return "Not implemented yet"

# this route is for updating a header from a version of an api
@api.route('/<int:id>/versions/<string:version>/headers/<int:header_id>/update')
class UpdateHeader(Resource):
    @api.doc('update header')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def patch(self, id, version, header_id):
        return "Not implemented yet"

# this route is for adding a new endpoint to a version of an api (endpoints are only for documentation purposes)
@api.route('/<int:id>/versions/<string:version>/endpoints/create')
class CreateEndpoint(Resource):
    @api.doc('create endpoint')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        return "Not implemented yet"

# this route is for deleting an endpoint from a version of an api
@api.route('/<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/delete')
class DeleteEndpoint(Resource):
    @api.doc('delete endpoint')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version, endpoint_id):
        return "Not implemented yet"

# this route is for updating an endpoint from a version of an api
@api.route('/<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/update')
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
@api.route('/test/<int:id>/<string:version>/<path:params>')
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
@api.route('/<int:id>/plans/<string:plan>/subscribe')
class SubscribePlan(Resource):
    @api.doc('subscribe plan')
    @api.response(200, 'Success')
    @role_token_required([Role.USER])
    def post(self, id, plan):
        return "Not implemented yet"

# this route if for creating an api key that will be used to access the api
# before generating the api key we must check if the user has an active subscription to the api
@api.route('/<int:id>/api_key/create')
class CreateApiKey(Resource):
    @api.doc('create api key')
    @api.response(201, 'Success')
    @role_token_required([Role.USER])
    def post(self, id):
        return "Not implemented yet"

# this route is for deleting an api key
@api.route('/<int:id>/api_key/delete')
class DeleteApiKey(Resource):
    @api.doc('delete api key')
    @api.response(200, 'Success')
    @role_token_required([Role.USER])
    def delete(self, id):
        return "Not implemented yet"
    
# this route is for getting all api keys of an api
@api.route('/<int:id>/api_keys')
class GetApiKeys(Resource):
    @api.doc('get api keys')
    @api.response(200, 'Success')
    @role_token_required([Role.USER])
    def get(self, id):
        return "Not implemented yet"
    
@api.route('/call/<int:id>/<string:version>/<path:params>')
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