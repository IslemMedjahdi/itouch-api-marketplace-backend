import os
from app.main import create_app

from flask_restx  import Api
from flask import Blueprint

from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.user_controller import api as users_ns


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

app = create_app(os.getenv('FLASK_ENV',"dev"))

app.register_blueprint(blueprint)
app.app_context().push()

# import models to let the migrate tool know
from app.main.model.user_model import User