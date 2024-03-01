from flask_restx  import Api
from flask import Blueprint

import pytest

from app.main import create_app, db

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
        title='ITOUCH API MARKETPLACE API DOCUMENTATION',
        version='1.0',
        description="ITOUCH API MARKETPLACE IS A PLATFORM THAT ALLOWS USERS TO CREATE, MANAGE AND MONETIZE THEIR API'S.",
        authorizations=authorizations,
        security='apikey'
)

api.add_namespace(auth_ns,path='/auth')
api.add_namespace(users_ns,path='/users')

@pytest.fixture()
def app():
    app = create_app("test")
    app.register_blueprint(blueprint)
    app.app_context().push()

    with app.app_context():
        db.create_all()

        User.create_default_admin()
        
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()


# import models to let the migrate tool know
from app.main.model.user_model import User
from app.main.model.api_model import Api
from app.main.model.api_category_model import ApiCategory
from app.main.model.api_version_key_model import ApiVersionKey
from app.main.model.api_version_model import ApiVersion
from app.main.model.api_version_request_model import ApiVersionRequest
from app.main.model.api_version_plan_model import ApiVersionPlan
from app.main.model.api_header_model import ApiVersionHeader