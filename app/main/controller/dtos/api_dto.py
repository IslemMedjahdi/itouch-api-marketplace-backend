from flask_restx import Namespace, fields

class ApiDto:
    api = Namespace('Api', description='api related operations')


    create_category_request = api.model('create_category_request',{
        'name': fields.String(required=True, description='The name of the category'),
        'description': fields.String(required=True, description='The category description'),
        #'created_by': fields.String(required=True, description='The user  who create the category'),
    })

    create_category_response = api.model('create_category_response',{
        'data': fields.Nested(api.model('user_info_data',{
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
