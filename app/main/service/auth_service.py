from typing import Dict, Tuple

from app.main.model.user_model import User
from app.main import db, flask_bcrypt

import re

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
                return response_object, 404
            
            if not user.check_password(data.get('password')):
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401
            
            if not user.check_status('active'):
                response_object = {
                    'status': 'fail',
                    'message': 'User is not active.'
                }
                return response_object, 401
            
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'Authorization': auth_token
            }
            return response_object, 200                
                
            
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, 500
        
    @staticmethod
    def register_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if not user:
                email = data.get('email')
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    response_object = {
                        'status': 'fail',
                        'message': 'Invalid email format.'
                    }
                    return response_object, 400

                password = data.get('password')
                password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

                new_user = User(
                    email=data.get('email'),
                    password_hash=password_hash,
                    firstname=data.get('firstname'),
                    lastname=data.get('lastname')
                )


                db.session.add(new_user)
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.'
                }
                return response_object, 202
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, 500
