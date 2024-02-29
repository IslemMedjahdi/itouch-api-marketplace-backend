from typing import Dict, Any, Tuple, List

from http import HTTPStatus

from app.main.model.user_model import User
from app.main import db, flask_bcrypt
from app.main.utils.validators import isEmailValid


class UserManagement: 
    @staticmethod
    def get_all_users(request) -> Tuple[Dict[str, Any], int]:
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))

            users_pagination = User.query.paginate(page=page, per_page=per_page)

            user_list = []
            for user in users_pagination.items:
                user_data = {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'status': user.status,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat()
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
                    role='supplier',
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
                    'role': user.role,
                    'status': user.status,
                    'created_at': user.created_at.isoformat(),
                    'updated_at': user.updated_at.isoformat()
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
                user.status = 'active'
                db.session.commit()
                response_object = {
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
                user.status = 'suspended'
                db.session.commit()
                response_object = {
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
