from flask_restx import Namespace, fields

class ApiDto:
    api = Namespace('Api', description='api related operations')


    create_category_request = api.model('create_category_request',{
        'name': fields.String(required=True, description='The name of the category'),
        'description': fields.String(required=True, description='The category description'),
        #'created_by': fields.String(required=True, description='The user  who create the category'),
    })

    create_category_response = api.model('create_category_response',{
        'data': fields.Nested(api.model('category_info_data',{
        'id': fields.Integer(description='The category ID'),
        'name': fields.String(description='The name of the category'),
        'description': fields.String(description='The category description'),
        #'created_by': fields.String(description='The user  who create the category'),
        'created_at': fields.DateTime(description='The category creation date'),
        'updated_at': fields.DateTime(description='The category last update date')
    })),
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })


    categories_list_response = api.model('categories_list_response',{
        'data': fields.List(fields.Nested(api.model('categories_list_data',{
            'id': fields.Integer(description='The category ID'),
            'name': fields.String(description='The name of the category'),
            'description': fields.String(description='The category description'),
            'created_by': fields.Integer(description='The user  who create the category'),
            'created_at': fields.DateTime(description='The category creation date'),
            'updated_at': fields.DateTime(description='The category last update date')
        }))),
        'status': fields.String(description='The status of the response')
    })


    create_api_request = api.model('create_api_request',{
        'name': fields.String(required=True, description='The name of the api'),
        'description': fields.String(required=True, description='The api description'),
        'category_id': fields.Integer(required=True,description='The api category id'),
    })

    create_api_response = api.model('create_api_response',{
        'data': fields.Nested(api.model('api_info_data',{
        'id': fields.Integer(description='The api ID'),
        'name': fields.String(description='The name of the api'),
        'description': fields.String(description='The api description'),
        'category_id': fields.Integer(description='The api category id'),
        'created_at': fields.DateTime(description='The api creation date'),
        'updated_at': fields.DateTime(description='The api last update date')
    })),
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })


    api_info_response = api.model('api_info',{
    'data': fields.Nested(api.model('api_info_data',{
        'id': fields.Integer(description='The api ID'),
        'name': fields.String(description='The name of the api'),
        'description': fields.String(description='The api description'),
        'category_id': fields.Integer(description='The api category id'),
        'supplier_id': fields.Integer(description='The api supplier id'),
        'status': fields.String(description='The status of the api'),
        'created_at': fields.DateTime(description='The api creation date'),
        'updated_at': fields.DateTime(description='The api last update date')
    })),
    'status': fields.String(description='The status of the response')})

    create_api_key_request = api.model('create_api_key_request',{
        'user_id': fields.Integer(required=True,description='The user id'),
        'status': fields.String(required=True, description='The status of the api key')
    })

    create_api_key_response = api.model('create_api_key_response',{
        'data': fields.Nested(api.model('api_key_info_data',{
        'api_id': fields.Integer(description='The api api id'),
        'user_id': fields.Integer(description='The api user id'),
        'status': fields.String(description='The status of the api key'),
    })),
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })


    api_key_info_response = api.model('api_key_info',{
    'data': fields.Nested(api.model('api_key_info_data',{
        'key': fields.String(description='The api key'),
        'api_id': fields.Integer(description='The api api_id'),
        'user_id': fields.Integer(description='The api user_id'),
        'status': fields.String(description='The status of the api key'),
    })),
    'status': fields.String(description='The status of the response')})


    create_version_request = api.model('create_version_request',{
        'base_url': fields.String(required=True,description='The base url of the api version'),
        'status': fields.String(required=True, description='The status of api version')
    })

    create_version_response = api.model('create_version_response',{
        'data': fields.Nested(api.model('version_info_data',{
        'version': fields.String(description='The version of the api'),
        'api_id': fields.Integer(description='The api api_id'),
        'base_url': fields.String(description='The api base url of the api version'),
        'status': fields.String(description='The status of the api version'),
        'created_at': fields.DateTime(description='The api version creation date'),
        'updated_at': fields.DateTime(description='The api version last update date')
    })),
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })


    version_info_response = api.model('version_info',{
    'data': fields.Nested(api.model('version_info_data',{
        'version': fields.String(description='The version of the api'),
        'api_id': fields.Integer(description='The api api_id'),
        'base_url': fields.String(description='The api base url of the api version'),
        'status': fields.String(description='The status of the api version'),
        'created_at': fields.DateTime(description='The api version creation date'),
        'updated_at': fields.DateTime(description='The api version last update date')
    })),
    'status': fields.String(description='The status of the response')})



    create_endpoint_request = api.model('create_endpoint_request',{
        'endpoint': fields.String(required=True,description='The endpoint of an api version'),
        'method': fields.String(required=True,description='The method of an api version endpoint'),
        'description': fields.String(required=True,description='The description of an api version endpoint'),
        'request_body': fields.String(required=True,description='The request_body of an api version endpoint'),
        'response_body': fields.String(required=True,description='The response_body of an api version endpoint'),

    })

    create_endpoint_response = api.model('create_endpoint_response',{
        'data': fields.Nested(api.model('endpoint_info_data',{
        'api_id': fields.Integer(description='The api id'),
        'version': fields.String(description='The version of the api'),
        'endpoint': fields.String(description='The endpoint of an api version'),
        'method': fields.String(description='The method of an api version endpoint'),
        'description': fields.String(description='The description of an api version endpoint'),
        'request_body': fields.String(description='The request_body of an api version endpoint'),
        'response_body': fields.String(description='The response_body of an api version endpoint'),
    })),
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })


    endpoint_info_response = api.model('endpoint_info',{
    'data': fields.Nested(api.model('endpoint_info_data',{
        'api_id': fields.Integer(description='The api id'),
        'version': fields.String(description='The version of the api'),
        'endpoint': fields.String(description='The endpoint of an api version'),
        'method': fields.String(description='The method of an api version endpoint'),
        'description': fields.String(description='The description of an api version endpoint'),
        'request_body': fields.String(description='The request_body of an api version endpoint'),
        'response_body': fields.String(description='The response_body of an api version endpoint'),
    })),
    'status': fields.String(description='The status of the response')})


    create_header_request = api.model('create_header_request',{
        'key': fields.String(required=True,description='The key of an api version header'),
        'value': fields.String(required=True,description='The value of an api version header'),
    })

    create_header_response = api.model('create_header_response',{
        'data': fields.Nested(api.model('endpoint_info_data',{
        'id': fields.Integer(description='The header id'),
        'key': fields.String(description='The key of an api version header'),
        'value': fields.String(description='The value of an api version header'),
        'created_at': fields.DateTime(description='The api version header creation date'),
        'updated_at': fields.DateTime(description='The api version header last update date')
    })),
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })




