from flask import request, g as top_g
from flask_restx import Resource

from app.main.controller.dtos.api_dto import ApiDto

from app.main.utils.decorators.auth import role_token_required, require_authentication
from app.main.utils.decorators.discussion import (
    check_delete_discussion_permission,
    check_delete_answer_permission,
)

from app.main.utils.roles import Role

from app.main.service.discussion_service import DiscussionService
from app.main.core import ServicesInitializer

from http import HTTPStatus

api = ApiDto.api


@api.route("/categories/create")
class CreateCategory(Resource):
    @api.doc("create category")
    @api.expect(ApiDto.create_category_request, validate=True)
    @api.response(HTTPStatus.CREATED, "success")
    @role_token_required([Role.ADMIN])
    def post(self):
        ServicesInitializer.an_api_category_service().create_category(
            request.json, top_g.user.get("id")
        )
        return HTTPStatus.CREATED


@api.route("/categories")
class GetCategories(Resource):
    @api.doc("get categories")
    @api.response(HTTPStatus.OK, "Success", ApiDto.categories_list_response)
    def get(self):
        categories = ServicesInitializer.an_api_category_service().get_all_categories()

        return {
            "data": [category.to_dict() for category in categories],
        }, HTTPStatus.OK


@api.route("/create")
class CreateApi(Resource):
    @api.doc("create api")
    @api.expect(ApiDto.create_api_request, validate=True)
    @api.response(HTTPStatus.CREATED, "Success")
    @role_token_required([Role.SUPPLIER])
    def post(self):
        ServicesInitializer.an_api_service().create_api(
            request.json, top_g.user.get("id")
        )
        return HTTPStatus.CREATED


@api.route("/")
class GetApis(Resource):
    @api.doc("get apis")
    @api.param("page", "The page number")
    @api.param("per_page", "The number of items per page")
    @api.param("category_ids", "The category ID", type="array")
    @api.param("status", "The status of the apis")
    @api.response(HTTPStatus.OK, "Success", ApiDto.apis_list_response)
    def get(self):
        apis, pagination = ServicesInitializer.an_api_service().get_apis(request.args)
        return {
            "data": apis,
            "pagination": pagination,
        }, HTTPStatus.OK


@api.route("/mine")
class GetMyApis(Resource):
    @api.doc("get my apis")
    @api.param("page", "The page number")
    @api.param("per_page", "The number of items per page")
    @api.param("category_ids", "The category ID", type="array")
    @api.param("status", "The status of the apis")
    @api.response(HTTPStatus.OK, "Success", ApiDto.apis_list_response)
    @role_token_required([Role.SUPPLIER])
    def get(self):
        apis, pagination = ServicesInitializer.an_api_service().get_apis(
            {**request.args, "supplierId": top_g.user.get("id")}
        )
        return {
            "data": apis,
            "pagination": pagination,
        }, HTTPStatus.OK


@api.route("/<int:id>/update")
class UpdateApi(Resource):
    @api.doc("update api")
    @api.expect(ApiDto.update_api_request, validate=True)
    @api.response(HTTPStatus.OK, "Success")
    @role_token_required([Role.SUPPLIER])
    def patch(self, id):
        ServicesInitializer.an_api_service().update_api(
            id, top_g.user.get("id"), request.json
        )
        return HTTPStatus.OK


@api.route("/<int:id>")
class GetApiById(Resource):
    @api.doc("get api by id")
    @api.response(HTTPStatus.OK, "Success", ApiDto.api_info_response)
    def get(self, id):
        api_data = ServicesInitializer.an_api_service().get_api_by_id(id)
        return {
            "data": api_data,
        }, HTTPStatus.OK


@api.route("/mine/<int:id>")
class GetMyApiById(Resource):
    @api.doc("get my api by id")
    @api.response(HTTPStatus.OK, "Success", ApiDto.api_info_response)
    @role_token_required([Role.SUPPLIER])
    def get(self, id):
        api_data = ServicesInitializer.an_api_service().get_api_by_id(id)
        return {
            "data": api_data,
        }, HTTPStatus.OK


@api.route("/<int:id>/activate")
class ActivateApi(Resource):
    @api.doc("activate api")
    @api.response(HTTPStatus.OK, "Success")
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id):
        ServicesInitializer.an_api_service().activate_api(
            api_id=id, user_id=top_g.user.get("id"), role=top_g.user.get("role")
        )
        return HTTPStatus.OK


@api.route("/<int:id>/deactivate")
class DeactivateApi(Resource):
    @api.doc("deactivate api")
    @api.response(HTTPStatus.OK, "Success")
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id):
        ServicesInitializer.an_api_service().deactivate_api(
            api_id=id, user_id=top_g.user.get("id"), role=top_g.user.get("role")
        )
        return HTTPStatus.OK


@api.route("/<int:id>/versions/create")
class CreateVersion(Resource):
    @api.doc("create version")
    @api.expect(ApiDto.create_api_version_request, validate=True)
    @api.response(HTTPStatus.CREATED, "Success")
    @role_token_required([Role.SUPPLIER])
    def post(self, id):
        ServicesInitializer.an_api_version_service().create_api_version(
            api_id=id, data=request.json, supplier_id=top_g.user.get("id")
        )
        return HTTPStatus.CREATED


# this route is for getting all versions of an api
api_versions_list_response = ApiDto.api_versions_list_response


@api.route("/<int:id>/versions")
class GetVersions(Resource):
    @api.doc("get versions")
    @api.param("status", "The status of the api versions")
    @api.response(HTTPStatus.OK, "Success", api_versions_list_response)
    def get(self, id):
        versions = ServicesInitializer.an_api_version_service().get_api_versions(
            api_id=id, query_params=request.args
        )

        return {
            "data": versions,
        }, HTTPStatus.OK


@api.route("/<int:id>/versions/<string:version>")
class GetVersion(Resource):
    @api.doc("get version")
    @api.response(HTTPStatus.OK, "Success", ApiDto.api_version_info_response)
    def get(self, id, version):
        version = ServicesInitializer.an_api_version_service().get_api_version(
            api_id=id, version=version
        )
        return {
            "data": version,
        }, HTTPStatus.OK


@api.route("/mine/<int:id>/versions/<string:version>")
class GetMyApiVersion(Resource):
    @api.doc("get version")
    @api.response(HTTPStatus.OK, "Success", ApiDto.full_api_version_info_response)
    @role_token_required([Role.SUPPLIER])
    def get(self, id, version):
        version = ServicesInitializer.an_api_version_service().get_full_api_version(
            api_id=id, version=version
        )
        return {
            "data": version,
        }, HTTPStatus.OK


@api.route("/<int:id>/versions/<string:version>/activate")
class ActivateVersion(Resource):
    @api.doc("activate version")
    @api.response(HTTPStatus.OK, "Success")
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id, version):
        ServicesInitializer.an_api_version_service().activate_version(
            api_id=id,
            version=version,
            supplier_id=top_g.user.get("id"),
            role=top_g.user.get("role"),
        )
        return HTTPStatus.OK


@api.route("/<int:id>/versions/<string:version>/deactivate")
class DeactivateVersion(Resource):
    @api.doc("deactivate version")
    @api.response(HTTPStatus.OK, "Success")
    @role_token_required([Role.SUPPLIER, Role.ADMIN])
    def patch(self, id, version):
        ServicesInitializer.an_api_version_service().deactivate_version(
            api_id=id,
            version=version,
            supplier_id=top_g.user.get("id"),
            role=top_g.user.get("role"),
        )
        return HTTPStatus.OK


@api.route("/test/<int:id>/<string:version>/<path:params>")
class TestEndpoint(Resource):
    @api.doc("test endpoint")
    def get(self, id, version, params):
        return ServicesInitializer.an_api_tests_service().test_get(
            api_id=id, version=version, params=params
        )

    @api.doc("test endpoint")
    def post(self, id, version, params):
        return ServicesInitializer.an_api_tests_service().test_post(
            api_id=id, version=version, params=params, data=api.payload
        )

    @api.doc("test endpoint")
    def patch(self, id, version, params):
        return ServicesInitializer.an_api_tests_service().test_patch(
            api_id=id, version=version, params=params, data=api.payload
        )

    @api.doc("test endpoint")
    def delete(self, id, version, params):
        return ServicesInitializer.an_api_tests_service().test_delete(
            api_id=id, version=version, params=params
        )


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
# vote is either up or down
# user can only vote once
# user can change his vote
# user can remove his vote
# user can only vote on an answer
@api.route(
    "/<int:api_id>/discussions/<int:discussion_id>/answers/<int:answer_id>/votes"
)
class Votes(Resource):
    @api.doc("vote on an answer")
    @api.expect(ApiDto.create_vote_request, validate=True)
    @api.response(HTTPStatus.OK, "Success")
    @require_authentication
    def post(self, answer_id, **_):
        DiscussionService.vote_on_answer(
            answer_id, top_g.user.get("id"), api.payload.get("vote")
        )
        return HTTPStatus.OK

    @api.doc("remove vote from an answer")
    @api.response(HTTPStatus.OK, "Success")
    @require_authentication
    def delete(self, answer_id, **_):
        DiscussionService.remove_vote(answer_id, top_g.user.get("id"))
        return HTTPStatus.OK
