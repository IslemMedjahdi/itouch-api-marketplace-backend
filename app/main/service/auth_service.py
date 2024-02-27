from typing import Dict, Tuple

from app.main.model.user_model import User
from app.main import db, flask_bcrypt

from app.main.utils.validators import isEmailValid
from http import HTTPStatus

class Auth:

    @staticmethod
    def login_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if not user:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist'
                }
                return response_object, HTTPStatus.NOT_FOUND
            
            if not user.check_password(data.get('password')):
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, HTTPStatus.UNAUTHORIZED
            
            if not user.check_status('active'):
                response_object = {
                    'status': 'fail',
                    'message': 'User is not active.'
                }
                return response_object, HTTPStatus.FORBIDDEN
            
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'Authorization': auth_token
            }
            return response_object, HTTPStatus.OK                
                
            
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @staticmethod
    def register_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if not user:
                email = data.get('email')

                if not isEmailValid(email):
                    response_object = {
                        'status': 'fail',
                        'message': 'Invalid email format.'
                    }
                    return response_object, HTTPStatus.BAD_REQUEST
                
                new_user = User(
                    email=data.get('email'),
                    password=data.get('password'),
                    firstname=data.get('firstname'),
                    lastname=data.get('lastname')
                )


                db.session.add(new_user)
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
                return response_object, HTTPStatus.CREATED
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.'
                }
                return response_object, HTTPStatus.CONFLICT
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @staticmethod
    def get_logged_in_user(request) -> Tuple[Dict[str, str], int]:
        auth_token = request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            
            if isinstance(resp, str):
                response_object = {
                'status': 'fail',
                'message': resp
                }
                return response_object, HTTPStatus.UNAUTHORIZED
            
            user = User.query.filter_by(id=resp).first()

            if not user:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist'
                }
                return response_object, HTTPStatus.NOT_FOUND
            
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'email': user.email,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'role': user.role,
                    'status': user.status,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat()
                }
            }
            return response_object, HTTPStatus.OK
            
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, HTTPStatus.UNAUTHORIZED
