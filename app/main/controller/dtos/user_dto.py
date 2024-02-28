from flask_restx import Namespace, fields

class UserDto:
    api = Namespace('User', description='user related operations')

    user_info_response = api.model('user_info',{
    'data': fields.Nested(api.model('user_info_data',{
        'id': fields.Integer(description='The user ID'),
        'email': fields.String(description='The email address'),
        'role': fields.String(description='The user role'),
        'status': fields.String(description='The user status'),
        'created_at': fields.DateTime(description='The user creation date'),
        'updated_at': fields.DateTime(description='The user last update date')
    })),
    'status': fields.String(description='The status of the response')})

    users_list_response = api.model('users_list_response',{
        'data': fields.List(fields.Nested(api.model('users_list_data',{
            'id': fields.Integer(description='The user ID'),
            'email': fields.String(description='The email address'),
            'role': fields.String(description='The user role'),
            'status': fields.String(description='The user status'),
            'created_at': fields.DateTime(description='The user creation date'),
            'updated_at': fields.DateTime(description='The user last update date')
        }))),
        'pagination': fields.Nested(api.model('users_list_pagination',{
            'page': fields.Integer(description='The page number'),
            'per_page': fields.Integer(description='The number of items per page'),
            'total': fields.Integer(description='The total number of items'),
            'pages': fields.Integer(description='The total number of pages')
        })),
        'status': fields.String(description='The status of the response')
    })