from flask import request, g as top_g
from flask_restx import Resource
from typing import Dict, Tuple

from app.main.controller.dtos.api_dto import ApiDto

from app.main.utils.decorators.auth import role_token_required, require_authentication
from app.main.utils.decorators.discussion import (
    check_delete_discussion_permission,
    check_delete_answer_permission,
)
from app.main.service.api_service import ApiManagement

from app.main.utils.roles import Role

from app.main.service.discussion_service import DiscussionService

from http import HTTPStatus

api = ApiDto.api


create_category_request = ApiDto.create_category_request
create_category_response = ApiDto.create_category_response


@api.route("/categories/create")
class CreateCategory(Resource):
    @api.doc("create category")
    @api.expect(create_category_request, validate=True)
    @api.response(201, "success", create_category_response)
    @role_token_required([Role.ADMIN])
    def post(self):
        post_data = request.json
        return ApiManagement.create_category(request, data=post_data)


categories_list_response = ApiDto.categories_list_response


@api.route("/categories")
class GetCategories(Resource):
    @api.doc("get categories")
    @api.response(200, "Success", categories_list_response)
    def get(self) -> Tuple[Dict[str, any], int]:
        return ApiManagement.get_all_categories()


create_api_request = ApiDto.create_api_request
create_api_response = ApiDto.create_api_response


@api.route("/create")
class CreateApi(Resource):
    @api.doc("create api")
    @api.expect(create_api_request, validate=True)
    @api.response(201, "Success", create_api_response)
    @role_token_required([Role.SUPPLIER])
    def post(self):
        post_data = request.json
        return ApiManagement.create_api(request, data=post_data)


apis_list_response = ApiDto.apis_list_response


@api.route("/")
class GetApis(Resource):
    @api.doc("get apis")
    @api.param("page", "The page number")
    @api.param("per_page", "The number of items per page")
    @api.param("category_ids", "The category ID", type="array")
    @api.param("status", "The status of the apis")
    @api.response(200, "Success", apis_list_response)
    def get(self) -> Tuple[Dict[str, any], int]:
        return ApiManagement.get_all_apis(request)


@api.route("/mine")
class GetApis(Resource):
    @api.doc("get the logged in supplier apis")
    @api.param("page", "The page number")
    @api.param("per_page", "The number of items per page")
    @api.param("category_ids", "The category ID", type="array")
    @api.param("status", "The status of the apis")
    @api.response(200, "Success", apis_list_response)
    def get(self) -> Tuple[Dict[str, any], int]:
        return ApiManagement.get_logged_in_supplier_apis(request)


update_api_request = ApiDto.update_api_request
update_api_response = ApiDto.update_api_response


@api.route("/<int:id>/update")
class UpdateApi(Resource):
    @api.doc("update api")
    @api.expect(update_api_request, validate=True)
    @api.response(200, "Success", update_api_response)
    @role_token_required([Role.SUPPLIER])
    def patch(self, id):
        post_data = request.json
        return ApiManagement.update_api_info(request, api_id=id, data=post_data)


# this route is for getting an api by id
api_info_response = ApiDto.api_info_response


@api.route("/<int:id>")
class GetApiById(Resource):
    @api.doc("get api by id")
    @api.response(200, "Success", api_info_response)
    def get(self, id):
        return ApiManagement.get_single_api(api_id=id)

supplier_api_info_response = ApiDto.supplier_api_info_response
@api.route('/mine/<int:id>')
class GetApiById(Resource):
    @api.doc('get api by id')
    @api.response(200, 'Success', supplier_api_info_response)
    @role_token_required([Role.SUPPLIER])
    def get(self, id):
        return ApiManagement.get_logged_in_supplier_single_api(request, api_id=id)

# this route is for activating a disabled api, supplier cant activate an api that is disabled by an admin
# supplier can only activate his own api
activate_api_response = ApiDto.activate_api_response


@api.route("/<int:id>/activate")
class ActivateApi(Resource):
    @api.doc("activate api")
    @api.response(200, "Success", activate_api_response)
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id):
        return ApiManagement.activate_api(request, api_id=id)


# this route is for deactivating an active api
# supplier can only deactivate his own api
activate_api_response = ApiDto.activate_api_response


@api.route("/<int:id>/deactivate")
class DeactivateApi(Resource):
    @api.doc("deactivate api")
    @api.response(200, "Success", activate_api_response)
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id):
        return ApiManagement.disable_api(request, api_id=id)


# this route is for creating a new version of an api (version_name,base_url,headers,endpoints)

create_api_version_request = ApiDto.create_api_version_request
create_api_version_response = ApiDto.create_api_version_response


@api.route("/<int:id>/versions/create")
class CreateVersion(Resource):
    @api.doc("create version")
    @api.expect(create_api_version_request, validate=True)
    @api.response(201, "Success", create_api_version_response)
    @role_token_required([Role.SUPPLIER])
    def post(self, id):
        post_data = request.json
        return ApiManagement.create_version(request, api_id=id, data=post_data)


# this route is for getting all versions of an api
api_versions_list_response = ApiDto.api_versions_list_response


@api.route("/<int:id>/versions")
class GetVersions(Resource):
    @api.doc("get versions")
    @api.param("page", "The page number")
    @api.param("per_page", "The number of items per page")
    @api.param("status", "The status of the api versions")
    @api.response(200, "Success", api_versions_list_response)
    def get(self, id):
        return ApiManagement.get_all_api_versions(request, api_id=id)


# this route is for getting a version of an api by id
api_version_info_response = ApiDto.api_version_info_response
@api.route('/<int:id>/versions/<string:version>')
class GetVersion(Resource):
    @api.doc('get version')
    @api.response(200, 'Success',api_version_info_response)
    def get(self, id, version):
        return ApiManagement.get_single_api_version(api_id = id, version= version)

supplier_api_version_info_response = ApiDto.supplier_api_version_info_response
@api.route('/mine/<int:id>/versions/<string:version>')
class GetVersion(Resource):
    @api.doc('get version')
    @api.response(200, 'Success', supplier_api_version_info_response)
    @role_token_required([Role.SUPPLIER])
    def get(self, id, version):
        return ApiManagement.get_logged_in_supplier_single_api_version(request,api_id=id, version=version)

# this route is for activating a version of an api, supplier can only activate his own version
# supplier cant activate a version that is disabled by an admin
activate_api_version_response = ApiDto.activate_api_version_response
@api.route("/<int:id>/versions/<string:version>/activate")
class ActivateVersion(Resource):
    @api.doc("activate version")
    @api.response(200, "Success", activate_api_version_response)
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id, version):
        return ApiManagement.activate_api_version(request, api_id= id, version=version)


# this route is for deactivating a version of an api, supplier can only deactivate his own version
@api.route("/<int:id>/versions/<string:version>/deactivate")
class DeactivateVersion(Resource):
    @api.doc("deactivate version")
    @api.response(200, "Success", activate_api_version_response)
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id, version):
        return ApiManagement.disable_api_version(request, api_id=id, version=version)


# this route is for deleting a version of an api, supplier can only delete his own version
# @api.route("/<int:id>/versions/<string:version>/delete", doc=False)
# class DeleteVersion(Resource):
#     @api.doc("delete version")
#     @api.response(200, "Success")
#     @role_token_required([Role.SUPPLIER])
#     def delete(self, id, version):
#         return "Not implemented yet"


# this route is for adding a new header to a version of an api
create_header_request = ApiDto.create_header_request
create_header_response = ApiDto.create_header_response
@api.route("/<int:id>/versions/<string:version>/headers/create")
class CreateHeader(Resource):
    @api.doc("create header")
    @api.expect(create_header_request, validate=True)
    @api.response(201, "Success", create_header_response)
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        post_data = request.json
        return ApiManagement.create_header(request,data=post_data,api_id=id,version=version)

# this route is for deleting a header from a version of an api
# @api.route(
#     "/<int:id>/versions/<string:version>/headers/<int:header_id>/delete", doc=False
# )
# class DeleteHeader(Resource):
#     @api.doc("delete header")
#     @api.response(200, "Success")
#     @role_token_required([Role.SUPPLIER])
#     def delete(self, id, version, header_id):
#         return "Not implemented yet"


# this route is for updating a header from a version of an api
update_header_request = ApiDto.update_header_request
@api.route(
    "/<int:id>/versions/<string:version>/headers/<int:header_id>/update"
    )
class UpdateHeader(Resource):
    @api.doc("update header")
    @api.expect(create_header_request, validate=True)
    @api.response(200, "Success", create_header_response)
    @role_token_required([Role.SUPPLIER])
    def patch(self, id, version, header_id):
        post_data = request.json
        return ApiManagement.update_header(request, data=post_data, api_id=id, version=version, header_id=header_id)


# this route is for adding a new endpoint to a version of an api (endpoints are only for documentation purposes)
create_endpoint_request = ApiDto.create_endpoint_request
create_endpoint_response = ApiDto.create_endpoint_response
@api.route("/<int:id>/versions/<string:version>/endpoints/create")
class CreateEndpoint(Resource):
    @api.doc("create endpoint")
    @api.expect(create_endpoint_request, validate=True)
    @api.response(201, "Success", create_endpoint_response)
    @role_token_required([Role.SUPPLIER])
    def post(self, id, version):
        post_data = request.json
        return ApiManagement.create_endpoint(request,api_id=id, version=version, data=post_data)


# this route is for deleting an endpoint from a version of an api
@api.route(
    "/<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/delete", doc=False
)
class DeleteEndpoint(Resource):
    @api.doc("delete endpoint")
    @api.response(200, "Success")
    @role_token_required([Role.SUPPLIER])
    def delete(self, id, version, endpoint_id):
        return "Not implemented yet"


# this route is for updating an endpoint from a version of an api
@api.route(
    "/<int:id>/versions/<string:version>/endpoints/<int:endpoint_id>/update", doc=False
)
class UpdateEndpoint(Resource):
    @api.doc("update endpoint")
    @api.response(200, "Success")
    @role_token_required([Role.SUPPLIER])
    def patch(self, id, version, endpoint_id):
        return "Not implemented yet"


# TODO: The request must be from a whitelist domains
@api.route("/test/<int:id>/<string:version>/<path:params>")
class TestEndpoint(Resource):
    @api.doc("test endpoint")
    @api.response(200, "Success")
    def get(self, id, version, params):
        return ApiManagement.test_api(request, id, version, params)

    @api.doc("test endpoint")
    @api.response(200, "Success")
    def post(self, id, version, params):
        return ApiManagement.test_api(request, id, version, params)

    @api.doc("test endpoint")
    @api.response(200, "Success")
    def patch(self, id, version, params):
        return ApiManagement.test_api(request, id, version, params)

    @api.doc("test endpoint")
    @api.response(200, "Success")
    def delete(self, id, version, params):
        return ApiManagement.test_api(request, id, version, params)


@api.route("/<int:id>/plans/<string:plan>/subscribe", doc=False)
class SubscribePlan(Resource):
    @api.doc("subscribe plan")
    @api.response(200, "Success")
    @role_token_required([Role.USER])
    def post(self, id, plan):
        return "Not implemented yet"


@api.route("/<int:id>/api_key/create", doc=False)
class CreateApiKey(Resource):
    @api.doc("create api key")
    @api.response(201, "Success")
    @role_token_required([Role.USER])
    def post(self, id):
        return "Not implemented yet"


# this route is for deleting an api key
@api.route("/<int:id>/api_key/delete", doc=False)
class DeleteApiKey(Resource):
    @api.doc("delete api key")
    @api.response(200, "Success")
    @role_token_required([Role.USER])
    def delete(self, id):
        return "Not implemented yet"


# this route is for getting all api keys of an api
@api.route("/<int:id>/api_keys", doc=False)
class GetApiKeys(Resource):
    @api.doc("get api keys")
    @api.response(200, "Success")
    @role_token_required([Role.USER])
    def get(self, id):
        return "Not implemented yet"


@api.route("/call/<int:id>/<string:version>/<path:params>", doc=False)
class CallApi(Resource):
    @api.doc("call api")
    @api.response(200, "Success")
    def get(self, id, version, params):
        api_key = request.headers.get("X-API-KEY")
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


@api.route("/<int:api_id>/discussions")
class Discussions(Resource):
    @api.doc("get a specific api discussions")
    @api.marshal_list_with(ApiDto.discussions_response, envelope="data")
    @api.response(HTTPStatus.OK, "Success", ApiDto.discussions_response)
    def get(self, api_id):
        return DiscussionService.get_all_by_api_id(api_id), HTTPStatus.OK

    @api.doc("create a new discussion")
    @api.expect(ApiDto.create_discussion_request, validate=True)
    @api.marshal_with(
        ApiDto.discussions_response, envelope="data", code=HTTPStatus.CREATED
    )
    @require_authentication
    def post(self, api_id):
        return (
            DiscussionService.create_new_discussion(
                api_id, api.payload, top_g.user.get("id")
            ),
            HTTPStatus.CREATED,
        )


@api.route("/<int:api_id>/discussions/<int:discussion_id>")
class DiscussionDetails(Resource):
    @api.doc("get a specific discussion")
    @api.marshal_with(ApiDto.discussion_details_response, envelope="data")
    def get(self, discussion_id, **_):
        return DiscussionService.get_by_id(discussion_id), HTTPStatus.OK

    @api.doc("delete a specific discussion")
    @api.response(HTTPStatus.OK, "Success")
    @require_authentication
    @check_delete_discussion_permission
    def delete(self, discussion_id, **_):
        DiscussionService.delete_discussion(discussion_id)
        return HTTPStatus.OK


@api.route("/<int:api_id>/discussions/<int:discussion_id>/answers")
class DiscussionAnswers(Resource):
    @api.doc("create a new discussion answer")
    @api.expect(ApiDto.create_discussion_answer_request, validate=True)
    @api.marshal_with(
        ApiDto.discussion_answer_response, envelope="data", code=HTTPStatus.CREATED
    )
    @require_authentication
    def post(self, discussion_id, **_):
        return (
            DiscussionService.create_new_answer(
                discussion_id, api.payload, top_g.user.get("id")
            ),
            HTTPStatus.CREATED,
        )


@api.route("/<int:api_id>/discussions/<int:discussion_id>/answers/<int:answer_id>")
class AnswerDetails(Resource):
    @api.doc("get a specific answer")
    @api.marshal_with(ApiDto.discussion_answer_response, envelope="data")
    def get(self, answer_id, **_):
        return (DiscussionService.get_answer_by_id(answer_id), HTTPStatus.OK)

    @api.doc("delete a specific answer")
    @api.response(HTTPStatus.OK, "Success")
    @require_authentication
    @check_delete_answer_permission
    def delete(self, answer_id, **_):
        DiscussionService.delete_answer(answer_id)
        return HTTPStatus.OK


# TODO: add votes
