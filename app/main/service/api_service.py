from typing import Dict, Any, Tuple, List

from http import HTTPStatus

from app.main.model.user_model import User 
from app.main.model.api_category_model import ApiCategory
from app.main.model.api_model import ApiModel
from app.main import db, flask_bcrypt
from app.main.utils.validators import isEmailValid
from app.main.utils.roles import Role



class ApiManagement: 
    @staticmethod
    def create_category(request,data: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
        try:
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
                
                if not user.check_status('active'):
                    response_object = {
                        'status': 'fail',
                        'message': 'User is not active.'
                    }
                    return response_object, HTTPStatus.FORBIDDEN
                    
                new_api_category = ApiCategory(
                    name=data.get('name'),
                    description=data.get('description'),
                    created_by=resp
                )

                db.session.add(new_api_category)
                db.session.commit()

                response_object = {
                    'data': {
                        'id': new_api_category.id,
                        'name': new_api_category.name,
                        'description': new_api_category.description,
                        'created_by': new_api_category.created_by,
                        'created_at': new_api_category.created_at.isoformat(),
                        'updated_at': new_api_category.updated_at.isoformat()
                    },
                    'status': 'success',
                    'message': 'Successfully created a category.'
                }
                return response_object, HTTPStatus.CREATED
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return response_object, HTTPStatus.UNAUTHORIZED
        
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR
    

    @staticmethod
    def get_all_categories() -> Tuple[Dict[str, Any], int]:
        try:
            categories = ApiCategory.query.all()
            categories_data = []
            for category in categories:
                category_data = {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'created_by': category.created_by,
                    'created_at': category.created_at.isoformat() if category.created_at else None,
                    'updated_at': category.updated_at.isoformat() if category.updated_at else None,
                }
                categories_data.append(category_data)
            response_object = {
                'data': categories_data,
                'status': 'success'
            }
            return response_object, HTTPStatus.OK
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Failed to retrieve categories.',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR


    @staticmethod
    def create_api(request,data: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
        try:
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
                
                if not user.check_status('active'):
                    response_object = {
                        'status': 'fail',
                        'message': 'User is not active.'
                    }
                    return response_object, HTTPStatus.FORBIDDEN

                
                category_id = data.get('category_id')
                category = ApiCategory.query.filter_by(id=category_id).first()
                if not category:
                    response_object = {
                        'status': 'fail',
                        'message': 'Category does not exist'
                    }
                    return response_object, HTTPStatus.NOT_FOUND


                    
                new_api = ApiModel(
                    name=data.get('name'),
                    description=data.get('description'),
                    category_id=category_id,
                    supplier_id=resp
                )

                db.session.add(new_api)
                db.session.commit()

                response_object = {
                    'data': {
                        'id': new_api.id,
                        'name': new_api.name,
                        'description': new_api.description,
                        'category_id': new_api.category_id,
                        'created_at': new_api.created_at.isoformat(),
                        'updated_at': new_api.updated_at.isoformat()
                    },
                    'status': 'success',
                    'message': 'Successfully created an api.'
                }
                return response_object, HTTPStatus.CREATED
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Provide a valid auth token.'
                }
                return response_object, HTTPStatus.UNAUTHORIZED
        
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR
    
