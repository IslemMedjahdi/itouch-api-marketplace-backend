from flask_restx import Namespace, fields

class UserDto:
    api = Namespace('User', description='user related operations')

    user_info_response = api.model('single_user_info',{
    'data': fields.Nested(api.model('single_user_info_data',{
        'id': fields.Integer(description='The user ID'),
        'email': fields.String(description='The email address'),
        'role': fields.String(description='The user role'),
        'status': fields.String(description='The user status'),
        'created_at': fields.DateTime(description='The user creation date'),
        'updated_at': fields.DateTime(description='The user last update date'),
        'avatar' : fields.String(description='The user avatar',nullable = True)
    })),
    'status': fields.String(description='The status of the response')})

    users_list_response = api.model('users_list_response',{
        'data': fields.List(fields.Nested(api.model('users_list_data',{
            'id': fields.Integer(description='The user ID'),
            'email': fields.String(description='The email address'),
            'role': fields.String(description='The user role'),
            'status': fields.String(description='The user status'),
            'created_at': fields.DateTime(description='The user creation date'),
            'updated_at': fields.DateTime(description='The user last update date'),
            'avatar' : fields.String(description='The user avatar',nullable = True)
        }))),
        'pagination': fields.Nested(api.model('users_list_pagination',{
            'page': fields.Integer(description='The page number'),
            'per_page': fields.Integer(description='The number of items per page'),
            'total': fields.Integer(description='The total number of items'),
            'pages': fields.Integer(description='The total number of pages')
        })),
        'status': fields.String(description='The status of the response')
    })

    suspend_user_response = api.model('suspend_user_response',{
        'id': fields.Integer(description='The user ID'),
        'status': fields.String(description='The status of the response'),
    })

    activate_user_response = api.model('activate_user_response',{
        'id': fields.Integer(description='The user ID'),
        'status': fields.String(description='The status of the response'),    
    })

    new_supplier_request = api.model('new_supplier_request',{
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
        'firstname': fields.String(required=True, description='The user firstname'),
        'lastname': fields.String(required=True, description='The user lastname')
    })

    new_supplier_response = api.model('new_supplier_response',{
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })
    new_user_request = api.model('new_user_request',{
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
        'firstname': fields.String(required=True, description='The user firstname'),
        'lastname': fields.String(required=True, description='The user lastname')
    })

    new_user_response = api.model('new_user_response',{
        'data': fields.Nested(api.model('new_user_info_data',{
        'id': fields.Integer(description='The user ID'),
        'email': fields.String(description='The email address'),
        'firstname': fields.String(description='The user firstname'),
        'lastname': fields.String(description='The user lastname'),
        'role': fields.String(description='The user role'),
        'status': fields.String(description='The user status'),
        'created_at': fields.DateTime(description='The user creation date'),
        'updated_at': fields.DateTime(description='The user last update date'),
        'avatar' : fields.String(description='The user avatar',nullable = True)
    })),
        'status': fields.String(description='The status of the response'),
        'message': fields.String(description='The message of the response')
    })

    update_user_request = api.model('update_user_request',{
        'firstname': fields.String(required=True, description='The user firstname'),
        'lastname': fields.String(required=True, description='The user lastname')
    })

    
    

    update_user_response = api.model('updated_user_info',{
    'data': fields.Nested(api.model('updated_user_info_data',{
        'id': fields.Integer(description='The user ID'),
        #'email': fields.String(description='The email address'),
        'firstname': fields.String(description='The user firstname'),
        'lastname': fields.String(description='The user lastname'),
        #'role': fields.String(description='The user role'),
        #'status': fields.String(description='The user status'),
        #'created_at': fields.DateTime(description='The user creation date'),
        'updated_at': fields.DateTime(description='The user last update date')
    })),
    'status': fields.String(description='The status of the response')})

    update_password_request = api.model('update_password_request',{
        'current_password': fields.String(required=True, description='The user current password'),
        'new_password': fields.String(required=True, description='The user new password')
    })


    update_password_response = api.model('update_password_response',{
        'status': fields.String(description='The status of the response'),  
        'message': fields.Integer(description='The response message'),
  
    })