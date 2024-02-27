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
                    password_hash=data.get('password'),
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
