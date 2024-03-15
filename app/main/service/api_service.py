from typing import Dict, Any, Tuple, List
import requests
from http import HTTPStatus

from app.main.model.user_model import User 
from app.main.model.api_category_model import ApiCategory
from app.main.model.api_model import ApiModel
from app.main.model.api_plan_model import ApiPlan
from app.main.model.api_version_model import ApiVersion
from app.main.model.api_header_model import ApiVersionHeader
from app.main.model.api_version_endpoint_model import ApiVersionEndpoint

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
                                'api_status':api.status,
                                'status': 'success',
                                'message': 'The API is already active.'
                                }
                                return response_object, HTTPStatus.OK
                            else:
                                api.status = 'active'
                                db.session.commit()
                                response_object = {
                                    'api_id':api.id,
                                    'api_status':api.status,
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

    @staticmethod
    def disable_api(request, api_id: int) -> Tuple[Dict[str, str], int]:
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
                        if api.supplier_id == resp or user.role == Role.ADMIN:
                            if api.status == 'disabled':
                                response_object = {
                                    'api_id': api.id,
                                    'api_status':api.status,
                                    'status': 'success',
                                    'message': 'The API is already disabled.'
                                }
                                return response_object, HTTPStatus.OK
                            elif api.status == 'active':
                                api.status = 'disabled'
                                db.session.commit()
                                response_object = {
                                    'api_id': api.id,
                                    'api_status':api.status,
                                    'status': 'success',
                                    'message': 'API successfully disabled.'
                                }
                                return response_object, HTTPStatus.OK
                            elif api.status == 'pending':
                                response_object = {
                                    'status': 'fail',
                                    'message': 'Cannot disable a pending API. It must be approved first.'
                                }
                                return response_object, HTTPStatus.FORBIDDEN
                        else:
                            response_object = {
                                'status': 'fail',
                                'message': 'You are not authorized to disable this API.'
                            }
                            return response_object, HTTPStatus.FORBIDDEN
                    else:
                        response_object = {
                            'status': 'fail',
                             'message': 'API not found'
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
    

    @staticmethod
    def get_logged_in_supplier_apis(request) -> Tuple[Dict[str, Any], int]:
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
                
                if not user.role == Role.SUPPLIER:
                    response_object = {
                        'status': 'fail',
                        'message': 'You are not authorized to access this resource '
                    }
                    return response_object, HTTPStatus.FORBIDDEN
                
                page = int(request.args.get('page', 1))
                per_page = int(request.args.get('per_page', 10))
                # Enforce minimum and maximum per_page values
                per_page = max(10, min(per_page, 100))
                # Get the list of category ids
                category_ids = request.args.get('category_ids')
                # get the status
                status = request.args.get('status')


                # Start building the query
                query = ApiModel.query

                # Filter APIs based on these supplier id
                query = query.filter(ApiModel.supplier_id == resp)

                # If category_ids are provided, filter APIs based on these IDs
                if category_ids:
                    category_ids = category_ids.split(',')
                    query = query.filter(ApiModel.category_id.in_(category_ids))

                # If status is provided, filter APIs based on this status
                if status:
                    query = query.filter(ApiModel.status == status)
                # Perform pagination on the filtered query
                apis_pagination = query.paginate(page=page, per_page=per_page)

                

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
    def update_api_info(request,api_id,data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
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
            
            api = ApiModel.query.filter_by(id=api_id).first()
            
            if not api:
                response_object = {
                    'status': 'fail',
                    'message': 'Api does not exist'
                }
                return response_object, HTTPStatus.NOT_FOUND
            

            if not api.supplier_id == resp:
                response_object = {
                    'status': 'fail',
                    'message': 'You are not authorized to access this resource '
                }
                return response_object, HTTPStatus.FORBIDDEN
            
            new_name = data.get('name')
            new_description = data.get('description')
            if new_name:
                api.name = new_name
            if new_description:
                api.description = new_description
            
            db.session.commit()

            response_object = {
                'status': 'success',
                'data': {
                    'id': api.id,
                    'name': api.name,
                    'description': api.description,
                    'updated_at': api.updated_at.isoformat()
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
    def create_version(request,api_id, data: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
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

            
                api = ApiModel.query.filter_by(id=api_id).first()
                if not api:
                    return {'status': 'fail', 'message': 'Api does not exist'}, HTTPStatus.NOT_FOUND
   
                if not api.supplier_id == resp:
                    response_object = {
                        'status': 'fail',
                        'message': 'You are not authorized to access this resource '
                    }
                    return response_object, HTTPStatus.FORBIDDEN

                headers = data.get('headers')
                endpoints = data.get('endpoints')
                methods = ['POST', 'GET', 'PUT', 'DELETE']
                

                # Initialize a dictionary to store endpoints by URL
                endpoints_dict = {}

                # Iterate over each endpoint
                for endpoint in endpoints:
                    url = endpoint.get('url')
                    method = endpoint.get('method')

                    # If the URL is not in the dictionary, add it with an empty set for methods
                    if url not in endpoints_dict:
                        endpoints_dict[url] = set()

                    # Check if the method is valide methode 
                    if not method in methods:
                        return {'status': 'fail', 'message': 'Invalide Methode'}, HTTPStatus.BAD_REQUEST
                    # Check if the method is already in the set for this URL
                    if method in endpoints_dict[url]:
                        # If the method is already present, return a failure response
                        return {'status': 'fail', 'message': f'Duplicate method "{method}" for URL: {url}'}, HTTPStatus.BAD_REQUEST

                    # If the method is unique, add it to the set for this URL
                    endpoints_dict[url].add(method)

                version_name = data.get('version')
                version = ApiVersion.query.filter_by(version=version_name).first()

                if version :
                    return {'status': 'fail', 'message': 'Version already existe'}, HTTPStatus.BAD_REQUEST
 

                
                new_version = ApiVersion(
                    version=version_name,
                    base_url=data.get('base_url'),
                    api_id = api_id,
                    status = 'active'
                )
                db.session.add(new_version)
                db.session.commit()

                endpoints_data = []
                for endpoint in endpoints:
                    new_endpoint = ApiVersionEndpoint(
                        api_id=api_id,
                        version=version_name,
                        endpoint=endpoint.get('url'),
                        method=endpoint.get('method'),
                        description=endpoint.get('description'),
                        request_body=endpoint.get('request_body'),
                        response_body=endpoint.get('response_body'),
                    )
                    db.session.add(new_endpoint)
                    
                    endpoints_data.append({
                        'api_id': new_endpoint.api_id,
                        'version': new_endpoint.version,
                        'endpoint': new_endpoint.endpoint,
                        'method': new_endpoint.method,
                        'description': new_endpoint.description,
                        'request_body': new_endpoint.request_body,
                        'request_body': new_endpoint.request_body,
                    })
                headers_data = []
                for header in headers:
                    new_header = ApiVersionHeader(
                        api_id=api_id,
                        version=version_name,
                        key=header.get('key'),
                        value=header.get('value'),
                    )
                    db.session.add(new_header)
                    
                    headers_data.append({
                        'api_id': new_header.api_id,
                        'aversion': new_header.version,
                        'key': new_header.key,
                        'value': new_header.value
                    })

                db.session.commit()

                response_object = {
                    'data': {
                        'version': new_version.version,
                        'base_url': new_version.base_url,
                        'api_id': new_version.api_id,
                        'status': new_version.status,
                        'created_at': new_version.created_at.isoformat(),
                        'updated_at': new_version.updated_at.isoformat()
                    },
                    'headers': headers_data,
                    'endpoints': endpoints_data,
                    'status': 'success',
                    'message': 'Successfully created a version.'
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
    def get_all_api_versions(request, api_id) -> Tuple[Dict[str, Any], int]:
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            # Enforce minimum and maximum per_page values
            per_page = max(10, min(per_page, 100))
            status = request.args.get('status')

            api = ApiModel.query.filter_by(id=api_id).first()
            if not api:
                return {'status': 'fail', 'message': 'Api not found'}, HTTPStatus.NOT_FOUND
        
            if api.status != 'active':
                return {'status': 'fail', 'message': 'Api is not active'}, HTTPStatus.FORBIDDEN
        
            # Start building the query
            query = ApiVersion.query.filter(ApiVersion.api_id == api_id)

            # If status is provided, filter API versions based on this status
            if status:
                query = query.filter(ApiVersion.status == status)
            # Perform pagination on the filtered query
            versions_pagination = query.paginate(page=page, per_page=per_page)

        
            version_list = []
            for version in versions_pagination.items:
                version_data = {
                    'version': version.version,
                    'base_url': version.base_url,
                    'status': version.status,
                    'created_at': version.created_at.isoformat(),
                    'updated_at': version.updated_at.isoformat(),
                }
                version_list.append(version_data)

            response_object = {
                'status': 'success',
                'data': version_list,
                'pagination': {
                    'page': versions_pagination.page,
                    'per_page': versions_pagination.per_page,
                    'pages': versions_pagination.pages,
                    'total': versions_pagination.total
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
    def get_single_api_version(api_id, version) -> Tuple[Dict[str, str], int]:
        try:
            api = ApiModel.query.filter_by(id=api_id).first()

            if not api:
                return {'status': 'fail', 'message': 'Api not found'}, HTTPStatus.NOT_FOUND
        
            if api.status != 'active':
                return {'status': 'fail', 'message': 'Api is not active'}, HTTPStatus.FORBIDDEN
        
            api_version = ApiVersion.query.filter_by(api_id=api_id, version=version).first()

            if not api_version:
                return {'status': 'fail', 'message': 'Version not found'}, HTTPStatus.NOT_FOUND
            
            if api_version.status != 'active':
                return {'status': 'fail', 'message': 'Version is not active'}, HTTPStatus.FORBIDDEN
            
            
            headers_data = []
            headers =ApiVersionHeader.query.filter_by(api_id=api.id, api_version= version).all()

            for header in headers:
                header_data = {
                    'key': header.key,
                    'value': header.value,
                }
                headers_data.append(header_data)

            endpoints_data = []
            endpoints =ApiVersionEndpoint.query.filter_by(api_id=api.id, version= version).all()

            for endpoint in endpoints:
                endpoint_data = {
                    'endpoint': endpoint.endpoint,
                    'method': endpoint.method,
                    'description': endpoint.description,
                    'request_body': endpoint.request_body,
                    'response_body': endpoint.response_body,
                }
                endpoints_data.append(endpoint_data)

            api_version_data = {
                'version': api_version.version,
                'base_url': api_version.base_url,
                'api':{
                    'id': api.id,
                    'name':api.name
                },
                'status': api_version.status,
                'created_at': api_version.created_at.isoformat(),
                'updated_at': api_version.updated_at.isoformat(),
            }
            response_object = {
                'status': 'success',
                'data': api_version_data,
                'headers':headers_data,
                'endpoints':endpoints_data
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
    def test_api(request,api_id,version,params):
        api = ApiModel.query.filter_by(id=api_id).first()
        if not api:
            return {'status': 'fail', 'message': 'Api not found'}, HTTPStatus.NOT_FOUND
        
        if api.status != 'active':
            return {'status': 'fail', 'message': 'Api is not active'}, HTTPStatus.FORBIDDEN
        
        api_version = ApiVersion.query.filter_by(api_id=api_id, version=version).first()

        if not api_version:
            return {'status': 'fail', 'message': 'Version not found'}, HTTPStatus.NOT_FOUND
        
        if api_version.status != 'active':
            return {'status': 'fail', 'message': 'Version is not active'}, HTTPStatus.FORBIDDEN
        
        base_url = api_version.base_url

        headers = ApiVersionHeader.query.filter_by(api_id=api_id, api_version=version).all()

        headers = {header.key: header.value for header in headers}

        url = f'{base_url}/{params}'
        
        method = request.method

        response = requests.request(method, url, headers=headers, data=request.data)
        
        return {'status': 'success', 'data': response.json()}, response.status_code


  

  
