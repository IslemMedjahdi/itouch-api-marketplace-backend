from flask import request
from flask_restx import Resource

from app.main.controller.dtos.api_dto import ApiDto

from app.main.utils.decorators import role_token_required

from app.main.utils.roles import Role

api = ApiDto.api

@api.route('/categories/create')
class CreateCategory(Resource):
    @api.doc('create category')
    @api.response(201, 'Success')
    @role_token_required([Role.ADMIN])
    def post(self):
        return "Not implemented yet"
    
@api.route('/categories')
class GetCategories(Resource):
    @api.doc('get categories')
    @api.response(200, 'Success')
    def get(self):
        return "Not implemented yet"
    
@api.route('/create')
class CreateApi(Resource):
    @api.doc('create api')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self):
        return "Not implemented yet"
    
@api.route('/')
class GetApis(Resource):
    @api.doc('get apis')
    @api.response(200, 'Success')
    def get(self):
        return "Not implemented yet"

@api.route('/<int:id>/delete')
class DeleteApi(Resource):
    @api.doc('delete api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id):
        return "Not implemented yet"
    
@api.route('/<int:id>/update')
class UpdateApi(Resource):
    @api.doc('update api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def patch(self, id):
        return "Not implemented yet"
    
@api.route('/<int:id>')
class GetApiById(Resource):
    @api.doc('get api by id')
    @api.response(200, 'Success')
    def get(self, id):
        return "Not implemented yet"
    
@api.route('/<int:id>/activate')
class ActivateApi(Resource):
    @api.doc('activate api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id):
        return "Not implemented yet"
    
@api.route('/<int:id>/deactivate')
class DeactivateApi(Resource):
    @api.doc('deactivate api')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id):
        return "Not implemented yet"

@api.route('/<int:id>/versions/create')
class CreateVersion(Resource):
    @api.doc('create version')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions')
class GetVersions(Resource):
    @api.doc('get versions')
    @api.response(200, 'Success')
    def get(self, id):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions/<string:version>')
class GetVersion(Resource):
    @api.doc('get version')
    @api.response(200, 'Success')
    def get(self, id, version):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions/<string:version>/activate')
class ActivateVersion(Resource):
    @api.doc('activate version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id, version):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions/<string:version>/deactivate')
class DeactivateVersion(Resource):
    @api.doc('deactivate version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER,Role.ADMIN])
    def patch(self, id, version):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions/<string:version>/delete')
class DeleteVersion(Resource):
    @api.doc('delete version')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions/<string:version>/headers/create')
class CreateHeader(Resource):
    @api.doc('create header')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions/<string:version>/headers/<int:header_id>/delete')
class DeleteHeader(Resource):
    @api.doc('delete header')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version, header_id):
        return "Not implemented yet"
    
@api.route('/<int:id>/versions/<string:version>/headers/<int:header_id>/update')
class UpdateHeader(Resource):
    @api.doc('update header')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def patch(self, id, version, header_id):
        return "Not implemented yet"

@api.route('<int:id>/versions/<string:version>/endpoints/create')
class CreateEndpoint(Resource):
    @api.doc('create endpoint')
    @api.response(201, 'Success')
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        return "Not implemented yet"

@api.route('<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/delete')
class DeleteEndpoint(Resource):
    @api.doc('delete endpoint')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version, endpoint_id):
        return "Not implemented yet"

@api.route('<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/update')
class UpdateEndpoint(Resource):
    @api.doc('update endpoint')
    @api.response(200, 'Success')
    @role_token_required([Role.SUPPLIER])
    def patch(self, id, version, endpoint_id):
        return "Not implemented yet"

@api.route('/test/<int:id>/<string:version>/<path:params>')
class TestEndpoint(Resource):
    @api.doc('test endpoint')
    @api.response(200, 'Success')
    def get(self, id, version, params):
        print(params)
        print(id)
        print(version)
        return "Not implemented yet"
