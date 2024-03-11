from typing import Dict, Any, Tuple, List

from http import HTTPStatus

from app.main.model.user_model import User 
from app.main.model.api_category_model import ApiCategory
from app.main.model.api_model import ApiModel
from app.main.model.api_plan_model import ApiPlan
from app.main import db, flask_bcrypt
from app.main.utils.validators import isEmailValid
from app.main.utils.roles import Role

from app.main.service.media_service import MediaService


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
    def create_api(request, data: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
        try:
            auth_token = request.headers.get('Authorization')
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                
                if isinstance(resp, str):
                    return {'status': 'fail', 'message': resp}, HTTPStatus.UNAUTHORIZED
                
                user = User.query.filter_by(id=resp).first()

                if not user:
                    return {'status': 'fail', 'message': 'User does not exist'}, HTTPStatus.NOT_FOUND
                
                if not user.check_status('active'):
                    return {'status': 'fail', 'message': 'User is not active.'}, HTTPStatus.FORBIDDEN

                category_id = data.get('category_id')
                category = ApiCategory.query.filter_by(id=category_id).first()
                if not category:
                    return {'status': 'fail', 'message': 'Category does not exist'}, HTTPStatus.NOT_FOUND
   

                plans = data.get('plans')
                plan_names_set = set()
                for plan in plans:
                    plan_name = plan.get('name')
                    # Check if the plan name is already in the set
                    if plan_name in plan_names_set:
                        return {'status': 'fail', 'message': f'Duplicate plan name: {plan_name}'}, HTTPStatus.BAD_REQUEST
                    plan_names_set.add(plan_name)  # Add plan name to set

                
                new_api = ApiModel(
                    name=data.get('name'),
                    description=data.get('description'),
                    category_id=category_id,
                    supplier_id=resp
                )
                db.session.add(new_api)
                db.session.commit()

                
                plans_data = []
                for plan in plans:
                    new_plan = ApiPlan(
                        name=plan.get('name'),
                        description=plan.get('description'),
                        price=plan.get('price'),
                        max_requests=plan.get('max_requests'),
                        duration=plan.get('duration'),
                        api_id=new_api.id
                    )
                    db.session.add(new_plan)
                    
                    plans_data.append({
                        'name': new_plan.name,
                        'description': new_plan.description,
                        'price': new_plan.price,
                        'max_requests': new_plan.max_requests,
                        'duration': new_plan.duration
                    })

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
                    'plans': plans_data,
                    'status': 'success',
                    'message': 'Successfully created an API.'
                }
                return response_object, HTTPStatus.CREATED
            else:
                return {'status': 'fail', 'message': 'Provide a valid auth token.'}, HTTPStatus.UNAUTHORIZED
        
        except Exception as e:
            db.session.rollback()

            response_object = {
                'status': 'fail',
                'message': 'Try again',
                'error': str(e)
            }
            return response_object, HTTPStatus.INTERNAL_SERVER_ERROR


    @staticmethod
    def get_single_api(api_id: int) -> Tuple[Dict[str, str], int]:
        try:
            api = ApiModel.query.filter_by(id=api_id).first()
            if api:
                plans_data = []
                category_name = ApiCategory.query.filter_by(id=api.category_id).first().name
                supplier_firstname = User.query.filter_by(id=api.supplier_id).first().firstname
                supplier_lastname = User.query.filter_by(id=api.supplier_id).first().lastname 
                plans =ApiPlan.query.filter_by(api_id=api.id).all()

                for plan in plans:
                    plan_data = {
                        'name': plan.name,
                        'description': plan.description,
                        'price': plan.price,
                        'max_requests': plan.max_requests,
                        'duration': plan.duration
                    }
                    plans_data.append(plan_data)

                api_data = {
                    'id': api.id,
                    'name': api.name,
                    'description': api.description,
                    'category_id': api.category_id,
                    'category':{
                        'id': api.category_id,
                        'name':category_name
                    },
                    'supplier_id': api.supplier_id,
                    'supplier':{
                        'id':api.supplier_id,
                        'firstname':supplier_firstname,
                        'lastname': supplier_lastname
                    },
                    'status': api.status,
                    'created_at': api.created_at.isoformat(),
                    'updated_at': api.updated_at.isoformat(),
                    'image' : MediaService.generate_cover_url(api.id)
                }
                response_object = {
                    'status': 'success',
                    'data': api_data,
                    'plans':plans_data
                }
                return response_object, HTTPStatus.OK
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Api not found'
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
    def get_all_apis(request) -> Tuple[Dict[str, Any], int]:
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            # Enforce minimum and maximum per_page values
            per_page = max(10, min(per_page, 100))
            category_ids = request.args.get('category_ids')
            status = request.args.get('status')


            # Start building the query
            query = ApiModel.query

            # If category_ids are provided, filter APIs based on these IDs
            if category_ids:
                category_ids = category_ids.split(',')
                query = query.filter(ApiModel.category_id.in_(category_ids))

            # If status is provided, filter APIs based on this status
            if status:
                query = query.filter(ApiModel.status == status)
            # Perform pagination on the filtered query
            apis_pagination = query.paginate(page=page, per_page=per_page)

            
            #apis_pagination = ApiModel.query.paginate(page=page, per_page=per_page)

            api_list = []
            for api in apis_pagination.items:
                category_name = ApiCategory.query.filter_by(id=api.category_id).first().name
                supplier_firstname = User.query.filter_by(id=api.supplier_id).first().firstname
                supplier_lastname = User.query.filter_by(id=api.supplier_id).first().lastname  
                api_data = {
                    'id': api.id,
                    'name': api.name,
                    'description': api.description,
                    'category_id': api.category_id,
                    'category':{
                        'id': api.category_id,
                        'name':category_name
                    },
                    'supplier_id': api.supplier_id,
                    'supplier':{
                        'id':api.supplier_id,
                        'firstname':supplier_firstname,
                        'lastname': supplier_lastname
                    },
                    'status': api.status,
                    'created_at': api.created_at.isoformat(),
                    'updated_at': api.updated_at.isoformat(),
                    'image': MediaService.generate_cover_url(api.id)
                }
                api_list.append(api_data)

            response_object = {
                'status': 'success',
                'data': api_list,
                'pagination': {
                    'page': apis_pagination.page,
                    'per_page': apis_pagination.per_page,
                    'pages': apis_pagination.pages,
                    'total': apis_pagination.total
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
    def activate_api(request,api_id: int) -> Tuple[Dict[str, str], int]:
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
            
                api = ApiModel.query.filter_by(id=api_id).first()
                user = User.query.filter_by(id=resp).first()

                if user:
                    if api:
                        if api.supplier_id == resp or user.role == Role.ADMIN :
                            if api.status == 'active':
                                response_object = {
                                'api_id':api.id,
                                'status': 'success',
                                'message': 'The API is already active.'
                                }
                                return response_object, HTTPStatus.OK
                            else:
                                api.status = 'active'
                                db.session.commit()
                                response_object = {
                                    'api_id':api.id,
                                    'status': 'success',
                                    'message': 'Api status updated to active'
                                }
                                return response_object, HTTPStatus.OK
                        else:
                            response_object = {
                                'status':'fail',
                                'message':'You are not authorized to activate this API because it does not belong to you.'
                            }
                            return response_object, HTTPStatus.FORBIDDEN
                    else:
                        response_object = {
                            'status': 'fail',
                            'message': 'Api not found'
                        }
                        return response_object, HTTPStatus.NOT_FOUND
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'User does not exist'
                    }
                    return response_object, HTTPStatus.NOT_FOUND
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
