from flask_restx import Namespace, fields
from .user_dto import UserDto


class ApiDto:
    api = Namespace("Api", description="api related operations")

    create_category_request = api.model(
        "create_category_request",
        {
            "name": fields.String(
                required=True, description="The name of the category"
            ),
            "description": fields.String(
                required=True, description="The category description"
            ),
            #'created_by': fields.String(required=True, description='The user  who create the category'),
        },
    )

    create_category_response = api.model(
        "create_category_response",
        {
            "data": fields.Nested(
                api.model(
                    "category_info_data",
                    {
                        "id": fields.Integer(description="The category ID"),
                        "name": fields.String(description="The name of the category"),
                        "description": fields.String(
                            description="The category description"
                        ),
                        #'created_by': fields.String(description='The user  who create the category'),
                        "created_at": fields.DateTime(
                            description="The category creation date"
                        ),
                        "updated_at": fields.DateTime(
                            description="The category last update date"
                        ),
                    },
                )
            ),
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
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
                            "id": fields.Integer(description="The category ID"),
                            "name": fields.String(
                                description="The name of the category"
                            ),
                            "description": fields.String(
                                description="The category description"
                            ),
                            "created_by": fields.Integer(
                                description="The user  who create the category"
                            ),
                            "created_at": fields.DateTime(
                                description="The category creation date"
                            ),
                            "updated_at": fields.DateTime(
                                description="The category last update date"
                            ),
                        },
                    )
                )
            ),
            "status": fields.String(description="The status of the response"),
        },
    )

    create_api_request = api.model(
        "create_api_request",
        {
            "name": fields.String(required=True, description="The name of the api"),
            "description": fields.String(
                required=True, description="The api description"
            ),
            "category_id": fields.Integer(
                required=True, description="The api category id"
            ),
            "plans": fields.List(
                fields.Nested(
                    api.model(
                        "api_plan",
                        {
                            "name": fields.String(
                                required=True, description="The name of the plan"
                            ),
                            "description": fields.String(
                                required=True, description="The plan description"
                            ),
                            "price": fields.Integer(
                                required=True, description="The plan price"
                            ),
                            "max_requests": fields.Integer(
                                required=True,
                                description="The maximum number of requests allowed",
                            ),
                            "duration": fields.Integer(
                                required=True,
                                description="The duration of the plan in days",
                            ),
                        },
                    )
                ),
                required=True,
                description="List of plans associated with the API",
            ),
        },
    )

    create_api_response = api.model(
        "create_api_response",
        {
            "data": fields.Nested(
                api.model(
                    "api_info_data",
                    {
                        "id": fields.Integer(description="The api ID"),
                        "name": fields.String(description="The name of the api"),
                        "description": fields.String(description="The api description"),
                        "category_id": fields.Integer(
                            description="The api category id"
                        ),
                        "created_at": fields.DateTime(
                            description="The api creation date"
                        ),
                        "updated_at": fields.DateTime(
                            description="The api last update date"
                        ),
                    },
                )
            ),
            "plans": fields.List(
                fields.Nested(
                    api.model(
                        "api_plan",
                        {
                            "name": fields.String(description="The name of the plan"),
                            "description": fields.String(
                                description="The plan description"
                            ),
                            "price": fields.Integer(description="The plan price"),
                            "max_requests": fields.Integer(
                                description="The maximum number of requests allowed"
                            ),
                            "duration": fields.Integer(
                                description="The duration of the plan in days"
                            ),
                        },
                    )
                ),
                description="List of plans associated with the API",
            ),
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    api_info_response = api.model(
        "api_info",
        {
            "data": fields.Nested(
                api.model(
                    "api_info_data",
                    {
                        "id": fields.Integer(description="The api ID"),
                        "name": fields.String(description="The name of the api"),
                        "description": fields.String(description="The api description"),
                        "category_id": fields.Integer(
                            description="The api category id"
                        ),
                        "category": fields.Nested(
                            api.model(
                                "api_category_info_data",
                                {
                                    "id": fields.Integer(
                                        description="The api category id"
                                    ),
                                    "name": fields.String(
                                        description="The api category name"
                                    ),
                                },
                            )
                        ),
                        "supplier_id": fields.Integer(
                            description="The api supplier id"
                        ),
                        "supplier": fields.Nested(
                            api.model(
                                "api_supplier_info_data",
                                {
                                    "id": fields.Integer(
                                        description="The api supplier id"
                                    ),
                                    "firstname": fields.String(
                                        description="The api supplier firstname"
                                    ),
                                    "lastname": fields.String(
                                        description="The api supplier lastname"
                                    ),
                                },
                            )
                        ),
                        "status": fields.String(description="The status of the api"),
                        "created_at": fields.DateTime(
                            description="The api creation date"
                        ),
                        "updated_at": fields.DateTime(
                            description="The api last update date"
                        ),
                        "image": fields.String(description="The picture of the api"),
                    },
                )
            ),
            "plans": fields.List(
                fields.Nested(
                    api.model(
                        "api_plan",
                        {
                            "name": fields.String(description="The name of the plan"),
                            "description": fields.String(
                                description="The plan description"
                            ),
                            "price": fields.Integer(description="The plan price"),
                            "max_requests": fields.Integer(
                                description="The maximum number of requests allowed"
                            ),
                            "duration": fields.Integer(
                                description="The duration of the plan in days"
                            ),
                        },
                    )
                ),
                description="List of plans associated with the API",
            ),
            "status": fields.String(description="The status of the response"),
        },
    )

    supplier_api_info_response = api.model(
        "supplier_api_info",
        {
            "data": fields.Nested(
                api.model(
                    "supplier_api_info_data",
                    {
                        "id": fields.Integer(description="The api ID"),
                        "name": fields.String(description="The name of the api"),
                        "description": fields.String(description="The api description"),
                        "category_id": fields.Integer(
                            description="The api category id"
                        ),
                        "category": fields.Nested(
                            api.model(
                                "api_category_info_data",
                                {
                                    "id": fields.Integer(
                                        description="The api category id"
                                    ),
                                    "name": fields.String(
                                        description="The api category name"
                                    ),
                                },
                            )
                        ),
                        "supplier_id": fields.Integer(
                            description="The api supplier id"
                        ),
                        "supplier": fields.Nested(
                            api.model(
                                "api_supplier_info_data",
                                {
                                    "id": fields.Integer(
                                        description="The api supplier id"
                                    ),
                                    "firstname": fields.String(
                                        description="The api supplier firstname"
                                    ),
                                    "lastname": fields.String(
                                        description="The api supplier lastname"
                                    ),
                                },
                            )
                        ),
                        "status": fields.String(description="The status of the api"),
                        "created_at": fields.DateTime(
                            description="The api creation date"
                        ),
                        "updated_at": fields.DateTime(
                            description="The api last update date"
                        ),
                        "image": fields.String(description="The picture of the api"),
                    },
                )
            ),
            "plans": fields.List(
                fields.Nested(
                    api.model(
                        "api_plan",
                        {
                            "name": fields.String(description="The name of the plan"),
                            "description": fields.String(
                                description="The plan description"
                            ),
                            "price": fields.Integer(description="The plan price"),
                            "max_requests": fields.Integer(
                                description="The maximum number of requests allowed"
                            ),
                            "duration": fields.Integer(
                                description="The duration of the plan in days"
                            ),
                        },
                    )
                ),
                description="List of plans associated with the API",
            ),
            "status": fields.String(description="The status of the response"),
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
                            "id": fields.Integer(description="The api ID"),
                            "name": fields.String(description="The name of the api"),
                            "description": fields.String(
                                description="The api description"
                            ),
                            "category_id": fields.Integer(
                                description="The api category id"
                            ),
                            "category": fields.Nested(
                                api.model(
                                    "api_category_info_data",
                                    {
                                        "id": fields.Integer(
                                            description="The api category id"
                                        ),
                                        "name": fields.String(
                                            description="The api category name"
                                        ),
                                    },
                                )
                            ),
                            "supplier_id": fields.Integer(
                                description="The api supplier id"
                            ),
                            "supplier": fields.Nested(
                                api.model(
                                    "api_supplier_info_data",
                                    {
                                        "id": fields.Integer(
                                            description="The api supplier id"
                                        ),
                                        "firstname": fields.String(
                                            description="The api supplier firstname"
                                        ),
                                        "lastname": fields.String(
                                            description="The api supplier lastname"
                                        ),
                                    },
                                )
                            ),
                            "status": fields.String(
                                description="The status of the api"
                            ),
                            "created_at": fields.DateTime(
                                description="The api creation date"
                            ),
                            "updated_at": fields.DateTime(
                                description="The api last update date"
                            ),
                            "image": fields.String(
                                description="The picture of the api"
                            ),
                        },
                    )
                )
            ),
            "status": fields.String(description="The status of the response"),
        },
    )

    activate_api_response = api.model(
        "activate_api_response",
        {
            "api_id": fields.Integer(description="The api ID"),
            "api_status": fields.String(description="The new status of the api"),
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    update_api_request = api.model(
        "update_api_request",
        {
            "name": fields.String(required=True, description="The api name"),
            "description": fields.String(
                required=True, description="The api description"
            ),
        },
    )

    update_api_response = api.model(
        "updated_api_info",
        {
            "data": fields.Nested(
                api.model(
                    "updated_api_info_data",
                    {
                        "id": fields.Integer(description="The api ID"),
                        "name": fields.String(description="The api name"),
                        "description": fields.String(description="The api description"),
                        "updated_at": fields.DateTime(
                            description="The api last update date"
                        ),
                    },
                )
            ),
            "status": fields.String(description="The status of the response"),
        },
    )

    create_api_version = api.model(
        "create_api_version",
        {
            "version": fields.String(required=True, description="The api version"),
            "base_url": fields.String(required=True, description="The api base url"),
            "headers": fields.List(
                fields.Nested(
                    api.model(
                        "api_header",
                        {
                            "key": fields.String(
                                required=True, description="The header key"
                            ),
                            "value": fields.String(
                                required=True, description="The header value"
                            ),
                        },
                    )
                ),
                required=True,
                description="List of headers associated with the API version",
            ),
            "endpoints": fields.List(
                fields.Nested(
                    api.model(
                        "api_endpoint",
                        {
                            "url": fields.String(
                                required=True, description="The endpoint url"
                            ),
                            "method": fields.String(
                                required=True, description="The endpoint method"
                            ),
                            "description": fields.String(
                                required=True, description="The endpoint description"
                            ),
                            "request_body": fields.String(
                                required=True, description="The endpoint request body"
                            ),
                            "response_body": fields.String(
                                required=True, description="The endpoint response body"
                            ),
                        },
                    )
                ),
                required=True,
                description="List of endpoints associated with the API version",
            ),
        },
    )

    discussions_response = api.model(
        "discussions_response",
        {
            "id": fields.Integer(description="The unique identifier of the discussion"),
            "title": fields.String(
                required=True, description="The title of the discussion"
            ),
            "user_id": fields.Integer(
                required=True,
                description="The ID of the user who created the discussion",
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
                model=UserDto.user_details,
            ),
            "answer": fields.String(description="The answer of the discussion"),
            "created_at": fields.DateTime(
                description="The date and time when the answer was created"
            ),
            "votes": fields.Integer(description="The number of votes of the answer"),
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
                model=UserDto.user_details,
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
    update_api_request = api.model(
        "update_api_request",
        {
            "name": fields.String(required=True, description="The api name"),
            "description": fields.String(
                required=True, description="The api description"
            ),
        },
    )

    update_api_response = api.model(
        "updated_api_info",
        {
            "data": fields.Nested(
                api.model(
                    "updated_api_info_data",
                    {
                        "id": fields.Integer(description="The api ID"),
                        "name": fields.String(description="The api name"),
                        "description": fields.String(description="The api description"),
                        "updated_at": fields.DateTime(
                            description="The api last update date"
                        ),
                    },
                )
            ),
            "status": fields.String(description="The status of the response"),
        },
    )

    create_api_version_request = api.model(
        "create_api_version",
        {
            "version": fields.String(required=True, description="The api version"),
            "base_url": fields.String(required=True, description="The api base url"),
            "headers": fields.List(
                fields.Nested(
                    api.model(
                        "api_header",
                        {
                            "key": fields.String(
                                required=True, description="The header key"
                            ),
                            "value": fields.String(
                                required=True, description="The header value"
                            ),
                        },
                    )
                ),
                required=True,
                description="List of headers associated with the API version",
            ),
            "endpoints": fields.List(
                fields.Nested(
                    api.model(
                        "api_endpoint",
                        {
                            "url": fields.String(
                                required=True, description="The endpoint url"
                            ),
                            "method": fields.String(
                                required=True, description="The endpoint method"
                            ),
                            "description": fields.String(
                                required=True, description="The endpoint description"
                            ),
                            "request_body": fields.String(
                                required=True, description="The endpoint request body"
                            ),
                            "response_body": fields.String(
                                required=True, description="The endpoint response body"
                            ),
                        },
                    )
                ),
                required=True,
                description="List of endpoints associated with the API version",
            ),
        },
    )

    create_api_version_response = api.model(
        "create_api_version_response",
        {
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    api_version_info_response = api.model(
        "api_version_info",
        {
            "data": fields.Nested(
                api.model(
                    "api_version_info_data",
                    {
                        "version": fields.String(description="The api version"),
                        "api": fields.Nested(
                            api.model(
                                "api_info_data",
                                {
                                    "id": fields.Integer(description="The api id"),
                                    "name": fields.String(description="The api name"),
                                },
                            )
                        ),
                        "status": fields.String(description="The status of the api"),
                        "created_at": fields.DateTime(
                            description="The api creation date"
                        ),
                        "updated_at": fields.DateTime(
                            description="The api last update date"
                        ),
                    },
                )
            ),
            "endpoints": fields.List(
                fields.Nested(
                    api.model(
                        "api_version_endpoints",
                        {
                            "endpoint": fields.String(
                                description="The endpoint of the version"
                            ),
                            "method": fields.String(description="The endpoint method"),
                            "description": fields.String(
                                description="The endpoint description"
                            ),
                            "request_body": fields.String(
                                description="The endpoint request_body"
                            ),
                            "response_body": fields.String(
                                description="The endpoint response_body"
                            ),
                        },
                    )
                ),
                description="List of endpoints associated with the API version",
            ),
            "status": fields.String(description="The status of the response"),
        },
    )

    supplier_api_version_info_response = api.model(
        "supplier_api_version_info",
        {
            "data": fields.Nested(
                api.model(
                    "supplier_api_version_info_data",
                    {
                        "version": fields.String(description="The api version"),
                        "base_url": fields.String(
                            description="The api version base_url"
                        ),
                        "api": fields.Nested(
                            api.model(
                                "api_info_data",
                                {
                                    "id": fields.Integer(description="The api id"),
                                    "name": fields.String(description="The api name"),
                                },
                            )
                        ),
                        "status": fields.String(description="The status of the api"),
                        "created_at": fields.DateTime(
                            description="The api creation date"
                        ),
                        "updated_at": fields.DateTime(
                            description="The api last update date"
                        ),
                    },
                )
            ),
            "headers": fields.List(
                fields.Nested(
                    api.model(
                        "api_version_headers",
                        {
                            "key": fields.String(description="The key of the header"),
                            "value": fields.String(description="The header value"),
                        },
                    )
                ),
                description="List of headers associated with the API version",
            ),
            "endpoints": fields.List(
                fields.Nested(
                    api.model(
                        "api_version_endpoints",
                        {
                            "endpoint": fields.String(
                                description="The endpoint of the version"
                            ),
                            "method": fields.String(description="The endpoint method"),
                            "description": fields.String(
                                description="The endpoint description"
                            ),
                            "request_body": fields.String(
                                description="The endpoint request_body"
                            ),
                            "response_body": fields.String(
                                description="The endpoint response_body"
                            ),
                        },
                    )
                ),
                description="List of endpoints associated with the API version",
            ),
            "status": fields.String(description="The status of the response"),
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
                            "version": fields.Integer(description="The api version"),
                            "status": fields.String(
                                description="The status of the api version"
                            ),
                            "created_at": fields.DateTime(
                                description="The api version creation date"
                            ),
                            "updated_at": fields.DateTime(
                                description="The api version last update date"
                            ),
                        },
                    )
                )
            ),
            "status": fields.String(description="The status of the response"),
        },
    )

    activate_api_version_response = api.model(
        "activate_api_version_response",
        {
            "version": fields.String(description="The version"),
            "version_status": fields.String(
                description="The new status of the version"
            ),
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    create_header_request = api.model(
        "create_header_request",
        {
            "key": fields.String(
                required=True, description="The key of the header"
            ),
            "value": fields.String(
                required=True, description="The header value"
            ),
        },
    )

    create_header_response = api.model(
        "create_header_response",
        {
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    delete_header_response = api.model(
        "delete_header_response",
        {
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    update_header_request = api.model(
        "update_header_request",
        {
            "key": fields.String(
                description="The key of the header"
            ),
            "value": fields.String(
                description="The header value"
            ),
        },
    )

    create_endpoint_request = api.model(
        "create_endpoint_request",
        {
            "url": fields.String(
                required=True, description="The url of the endpoint"
            ),
            "method": fields.String(
                required=True, description="The endpoint method"
            ),
            "description": fields.String(
                required=True, description="The endpoint description"
            ),
            "request_body": fields.String(
                required=True, description="The endpoint request body"
            ),
            "response_body": fields.String(
                required=True, description="The endpoint response body"
            ),
        },
    )

    create_endpoint_response = api.model(
        "create_endpoint_response",
        {
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    delete_endpoint_response = api.model(
        "delete_endpoint_response",
        {
            "status": fields.String(description="The status of the response"),
            "message": fields.String(description="The message of the response"),
        },
    )

    update_endpoint_request = api.model(
        "update_endpoint_request",
        {
            "description": fields.String(
                description="The endpoint description"
            ),
            "request_body": fields.String(
                description="The endpoint request body"
            ),
            "response_body": fields.String(
                description="The endpoint response body"
            ),
        },
    )
