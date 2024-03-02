import os
from app.main import create_app

from flask_restx  import Api
from flask import Blueprint

from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.user_controller import api as users_ns
from app.main.controller.api_controller import api as api_ns

from app.main.model.user_model import User

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(blueprint,
        title='ITOUCH API MARKETPLACE API',
        version='1.0',
        description="ITOUCH API MARKETPLACE IS A PLATFORM THAT ALLOWS USERS TO CREATE, MANAGE AND MONETIZE THEIR API'S.",
        authorizations=authorizations,
        security='apikey'
)

api.add_namespace(auth_ns,path='/auth')
api.add_namespace(users_ns,path='/users')
api.add_namespace(api_ns,path='/apis')

app = create_app(os.getenv('FLASK_ENV',"dev"))

app.register_blueprint(blueprint)
app.app_context().push()

with app.app_context():    
    User.create_default_admin()

# import models to let the migrate tool know
from app.main.model.user_model import User
from app.main.model.api_model import ApiModel
from app.main.model.api_category_model import ApiCategory
from app.main.model.api_version_model import ApiVersion
from app.main.model.api_plan_model import ApiPlan
from app.main.model.api_header_model import ApiVersionHeader
from app.main.model.api_version_endpoint_model import ApiVersionEndpoint