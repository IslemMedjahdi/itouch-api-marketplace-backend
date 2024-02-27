from flask_restx import Namespace, fields

class AuthDto:
    api = Namespace('Auth', description='authentication related operations')
    
    user_login_request = api.model('user_login',{
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password')
    })

    user_login_response = api.model('user_login_success',{
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response'),
        'Authorization': fields.String(description='The access token')
    })

    user_register_request = api.model('user_register',{
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
        'firstname': fields.String(required=True, description='The user firstname'),
        'lastname': fields.String(required=True, description='The user lastname')
    })

    user_register_response = api.model('user_register_success',{
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })

    user_info_response = api.model('user_info',{
    'data': fields.Nested(api.model('user_info_data',{
        'id': fields.Integer(description='The user ID'),
        'email': fields.String(description='The email address'),
        'role': fields.String(description='The user role'),
        'status': fields.String(description='The user status'),
        'created_at': fields.DateTime(description='The user creation date'),
        'updated_at': fields.DateTime(description='The user last update date')
    })),
    'status': fields.String(description='The status of the response')
})