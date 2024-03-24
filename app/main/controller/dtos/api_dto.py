from flask_restx import Namespace, fields
from .user_dto import UserDto


class ApiDto:
    api = Namespace("Api", description="api related operations")

    create_category_request = api.model(
        "create_category_request",
        {
            "name": fields.String(
                required=True,
            ),
            "description": fields.String(
                required=True,
            ),
        },
    )

    categories_list_response = api.model(
        "categories_list_response",
        {
            "data": fields.List(
                fields.Nested(
                    api.model(
                        "categories_list_data",
                        {
                            "id": fields.Integer(),
                            "name": fields.String(),
                            "description": fields.String(),
                            "created_by": fields.Integer(),
                            "created_at": fields.DateTime(),
                            "updated_at": fields.DateTime(),
                        },
                    )
                )
            ),
        },
    )

    create_api_request = api.model(
        "create_api_request",
        {
            "name": fields.String(
                required=True,
            ),
            "description": fields.String(
                required=True,
            ),
            "category_id": fields.Integer(
                required=True,
            ),
            "plans": fields.List(
                fields.Nested(
                    api.model(
                        "api_plan",
                        {
                            "name": fields.String(
                                required=True,
                            ),
                            "description": fields.String(
                                required=True,
                            ),
                            "price": fields.Integer(
                                required=True,
                            ),
                            "max_requests": fields.Integer(
                                required=True,
                            ),
                            "duration": fields.Integer(
                                required=True,
                            ),
                        },
                    )
                ),
                required=True,
            ),
        },
    )

    apis_list_response = api.model(
        "apis_list_response",
        {
            "data": fields.List(
                fields.Nested(
                    api.model(
                        "apis_list_data",
                        {
                            "id": fields.Integer(),
                            "name": fields.String(),
                            "description": fields.String(),
                            "category_id": fields.Integer(),
                            "category": fields.Nested(
                                api.model(
                                    "api_category_info_data",
                                    {
                                        "id": fields.Integer(),
                                        "name": fields.String(),
                                    },
                                )
                            ),
                            "supplier_id": fields.Integer(),
                            "supplier": fields.Nested(
                                api.model(
                                    "api_supplier_info_data",
                                    {
                                        "id": fields.Integer(),
                                        "firstname": fields.String(),
                                        "lastname": fields.String(),
                                    },
                                )
                            ),
                            "status": fields.String(),
                            "created_at": fields.DateTime(),
                            "updated_at": fields.DateTime(),
                            "image": fields.String(),
                        },
                    )
                )
            ),
        },
    )

    update_api_request = api.model(
        "update_api_request",
        {
            "name": fields.String(),
            "description": fields.String(),
            "category_id": fields.Integer(),
        },
    )

    api_info_response = api.model(
        "api_info",
        {
            "data": fields.Nested(
                api.model(
                    "api_info_data",
                    {
                        "id": fields.Integer(),
                        "name": fields.String(),
                        "description": fields.String(),
                        "category_id": fields.Integer(),
                        "category": fields.Nested(
                            api.model(
                                "api_category_info_data",
                                {
                                    "id": fields.Integer(),
                                    "name": fields.String(),
                                },
                            )
                        ),
                        "supplier_id": fields.Integer(),
                        "supplier": fields.Nested(
                            api.model(
                                "api_supplier_info_data",
                                {
                                    "id": fields.Integer(),
                                    "firstname": fields.String(),
                                    "lastname": fields.String(),
                                },
                            )
                        ),
                        "status": fields.String(),
                        "created_at": fields.DateTime(),
                        "updated_at": fields.DateTime(),
                        "image": fields.String(),
                        "plans": fields.List(
                            fields.Nested(
                                api.model(
                                    "api_plan",
                                    {
                                        "name": fields.String(),
                                        "description": fields.String(),
                                        "price": fields.Integer(),
                                        "max_requests": fields.Integer(),
                                        "duration": fields.Integer(),
                                    },
                                )
                            ),
                        ),
                    },
                ),
            ),
        },
    )

    create_api_version_request = api.model(
        "create_api_version",
        {
            "version": fields.String(
                required=True,
            ),
            "base_url": fields.String(
                required=True,
            ),
            "headers": fields.List(
                fields.Nested(
                    api.model(
                        "api_header",
                        {
                            "key": fields.String(
                                required=True,
                            ),
                            "value": fields.String(
                                required=True,
                            ),
                        },
                    )
                ),
                required=True,
            ),
            "endpoints": fields.List(
                fields.Nested(
                    api.model(
                        "api_endpoint",
                        {
                            "url": fields.String(
                                required=True,
                            ),
                            "method": fields.String(
                                required=True,
                            ),
                            "description": fields.String(
                                required=True,
                            ),
                            "request_body": fields.String(
                                required=True,
                            ),
                            "response_body": fields.String(
                                required=True,
                            ),
                        },
                    )
                ),
                required=True,
            ),
        },
    )

    api_versions_list_response = api.model(
        "api_versions_list_response",
        {
            "data": fields.List(
                fields.Nested(
                    api.model(
                        "api_versions_list_data",
                        {
                            "version": fields.String(),
                            "status": fields.String(),
                            "created_at": fields.DateTime(),
                            "updated_at": fields.DateTime(),
                        },
                    )
                )
            ),
        },
    )

    api_version_info_response = api.model(
        "api_version_info",
        {
            "data": fields.Nested(
                api.model(
                    "api_version_info_data",
                    {
                        "version": fields.String(),
                        "status": fields.String(),
                        "created_at": fields.DateTime(),
                        "updated_at": fields.DateTime(),
                        "api": fields.Nested(
                            api.model(
                                "api_info_summary_data",
                                {
                                    "id": fields.Integer(),
                                    "name": fields.String(),
                                },
                            )
                        ),
                        "endpoints": fields.List(
                            fields.Nested(
                                api.model(
                                    "api_version_endpoints",
                                    {
                                        "endpoint": fields.String(),
                                        "method": fields.String(),
                                        "description": fields.String(),
                                        "request_body": fields.String(),
                                        "response_body": fields.String(),
                                    },
                                )
                            ),
                        ),
                    },
                )
            ),
        },
    )

    full_api_version_info_response = api.model(
        "full_api_version_info",
        {
            "data": fields.Nested(
                api.model(
                    "full_api_version_info_data",
                    {
                        "version": fields.String(),
                        "status": fields.String(),
                        "base_url": fields.String(),
                        "created_at": fields.DateTime(),
                        "updated_at": fields.DateTime(),
                        "api": fields.Nested(
                            api.model(
                                "api_info_summary_data",
                                {
                                    "id": fields.Integer(),
                                    "name": fields.String(),
                                },
                            )
                        ),
                        "endpoints": fields.List(
                            fields.Nested(
                                api.model(
                                    "full_api_version_endpoints",
                                    {
                                        "endpoint": fields.String(),
                                        "method": fields.String(),
                                        "description": fields.String(),
                                        "request_body": fields.String(),
                                        "response_body": fields.String(),
                                    },
                                )
                            ),
                            description="List of endpoints associated with the API version",
                        ),
                        "headers": fields.List(
                            fields.Nested(
                                api.model(
                                    "full_api_version_headers",
                                    {
                                        "id": fields.Integer(),
                                        "key": fields.String(),
                                        "value": fields.String(),
                                        "created_at": fields.DateTime(),
                                        "updated_at": fields.DateTime(),
                                    },
                                )
                            )
                        ),
                    },
                )
            ),
        },
    )

    # ------------------- UN REFACTORED -------------------

    discussions_response = api.model(
        "discussions_response",
        {
            "id": fields.Integer(description="The unique identifier of the discussion"),
            "title": fields.String(
                required=True, description="The title of the discussion"
            ),
            "user": fields.Nested(
                description="The user who created the discussion",
                model=UserDto.user_info_response,
            ),
            "created_at": fields.DateTime(
                description="The date and time when the discussion was created"
            ),
            "api_id": fields.Integer(
                required=True, description="The API ID associated with the discussion"
            ),
        },
    )

    create_discussion_request = api.model(
        "create_discussion_request",
        {
            "title": fields.String(
                required=True, description="The title of the discussion"
            ),
            "question": fields.String(
                required=True, description="The question of the discussion"
            ),
        },
    )

    discussion_answer_response = api.model(
        "create_discussion_answer_response",
        {
            "id": fields.Integer(description="The unique identifier of the answer"),
            "discussion_id": fields.Integer(
                description="The unique identifier of the discussion"
            ),
            "user": fields.Nested(
                description="The user who created the answer",
                model=UserDto.user_info_response,
            ),
            "answer": fields.String(description="The answer of the discussion"),
            "created_at": fields.DateTime(
                description="The date and time when the answer was created"
            ),
            "votes": fields.Integer(
                description="The number of votes of the answer", attribute="votes_count"
            ),
        },
    )
    discussion_details_response = api.model(
        "discussion_details_response",
        {
            "id": fields.Integer(description="The unique identifier of the discussion"),
            "title": fields.String(
                required=True, description="The title of the discussion"
            ),
            "question": fields.String(
                required=True, description="The question of the discussion"
            ),
            "user": fields.Nested(
                description="The user who created the answer",
                model=UserDto.user_info_response,
            ),
            "created_at": fields.DateTime(
                description="The date and time when the discussion was created"
            ),
            "api_id": fields.Integer(
                required=True, description="The API ID associated with the discussion"
            ),
            "answers": fields.List(fields.Nested(discussion_answer_response)),
        },
    )

    create_discussion_answer_request = api.model(
        "create_discussion_answer_request",
        {
            "answer": fields.String(
                required=True, description="The answer of the discussion"
            ),
        },
    )

    create_vote_request = api.model(
        "create_vote_request",
        {
            "vote": fields.String(
                required=True, description="The vote of the answer", enum=["up", "down"]
            ),
        },
    )
