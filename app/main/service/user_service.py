from typing import Dict, Any, Tuple, List

from http import HTTPStatus

from app.main.model.user_model import User
from app.main import db, flask_bcrypt
from app.main.utils.validators import isEmailValid
from app.main.utils.roles import Role

from app.main.service.media_service import MediaService

class UserManagement: 
    @staticmethod
    def get_all_users(request) -> Tuple[Dict[str, Any], int]:
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            # Enforce minimum and maximum per_page values
            per_page = max(10, min(per_page, 100))
            
            users_pagination = User.query.paginate(page=page, per_page=per_page)

            user_list = []
            for user in users_pagination.items:
                user_data = {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'status': user.status,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat(),
                    'avatar:': MediaService.generate_avatar_url(user.id),
                }
                user_list.append(user_data)

            response_object = {
                'status': 'success',
                'data': user_list,
                'pagination': {
                    'page': users_pagination.page,
                    'per_page': users_pagination.per_page,
                    'pages': users_pagination.pages,
                    'total': users_pagination.total
                }
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
    def create_supplier(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
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
                    email=email,  
                    role=Role.SUPPLIER,
                    password=data.get('password'),
                    firstname=data.get('firstname'),
                    lastname=data.get('lastname')
                )

                db.session.add(new_user)
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully created a supplier.',
                }
                return response_object, HTTPStatus.CREATED
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Supplier already exists.'
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
    def get_single_user(user_id: int) -> Tuple[Dict[str, str], int]:
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                user_data = {
                    'id': user.id,
                    'email': user.email,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
                    'role': user.role,
                    'status': user.status,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat(),
                    'avatar:': MediaService.generate_avatar_url(user.id),
                }
                response_object = {
                    'status': 'success',
                    'data': user_data
                }
                return response_object, HTTPStatus.OK
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User not found'
                }
                return response_object, HTTPStatus.NOT_FOUND
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def activate_user(user_id: int) -> Tuple[Dict[str, str], int]:
        try:
            user = User.query.get(user_id)
            if user:
                if user.status =='active':
                    response_object = {
                        'id':user.id,
                        'user_status':user.status,
                        'status': 'success',
                        'message': 'The User is already active.'
                    }
                    return response_object, HTTPStatus.OK
                elif user.status == 'suspended':
                    user.status = 'active'
                    db.session.commit()
                    response_object = {
                        'id':user.id,
                        'user_status':user.status,
                        'status': 'success',
                        'message': 'User status updated to active'
                    }
                    return response_object, HTTPStatus.OK
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User not found'
                }
                return response_object, HTTPStatus.NOT_FOUND
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR

    @staticmethod
    def suspend_user(user_id: int) -> Tuple[Dict[str, str], int]:
        try:
            user = User.query.get(user_id)
            if user:
                if user.status == 'suspended':
                    response_object = {
                        'id': user.id,
                        'user_status':user.status,
                        'status': 'success',
                        'message': 'The User is already suspended.'
                    }
                    return response_object, HTTPStatus.OK
                elif user.status == 'active':
                    user.status = 'suspended'
                    db.session.commit()
                    response_object = {
                        'id':user.id,
                        'user_status':user.status,
                        'status': 'success',
                        'message': 'User status updated to suspended'
                    }
                    return response_object, HTTPStatus.OK
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User not found'
                }
                return response_object, HTTPStatus.NOT_FOUND
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR

    
    @staticmethod
    def update_logged_in_user_info(request,data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
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
            

            new_firstname = data.get('firstname')
            new_lastname = data.get('lastname')
            if new_firstname:
                user.firstname = new_firstname
            if new_lastname:
                user.lastname = new_lastname
            
            db.session.commit()

            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'firstname': user.firstname,
                    'lastname': user.lastname,
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
    

    @staticmethod
    def update_logged_in_user_password(request,data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
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
            
            current_password = data.get('current_password')
            new_password = data.get('new_password')

            # Verify current password
            if not current_password:
                response_object = {
                    'status': 'fail',
                    'message': 'Current password is required'
                }
                return response_object, HTTPStatus.BAD_REQUEST

            if not user.check_password(current_password):
                response_object = {
                    'status': 'fail',
                    'message': 'Incorrect current password'
                }
                return response_object, HTTPStatus.UNAUTHORIZED

            # Update password
            password_hash = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password_hash = password_hash
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Password updated successfully'
                
            }
            return response_object, HTTPStatus.OK
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, HTTPStatus.UNAUTHORIZED



    @staticmethod
    def create_user(data: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
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
                    email=email,  
                    password=data.get('password'),
                    firstname=data.get('firstname'),
                    lastname=data.get('lastname')
                )

                db.session.add(new_user)
                db.session.commit()

                response_object = {
                    'data': {
                    'id' : new_user.id,
                    'email': new_user.email,
                    'firstname': new_user.firstname,
                    'lastname': new_user.lastname,
                    'status' : new_user.status,
                    'created_at': new_user.created_at.isoformat(),
                    'updated_at': new_user.updated_at.isoformat()
                    },
                    'status': 'success',
                    'message': 'Successfully created a user.',
                }
                return response_object, HTTPStatus.CREATED
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists.'
                }
                return response_object, HTTPStatus.CONFLICT
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR
