import pytest
from flask import g
from app.main.model.user_model import User
from app.main.utils.exceptions import BadRequestError

# from .fixtures.user.add_user import add_user
from .fixtures.user.suspend_user import suspend_user

from app.main.utils.roles import Role
from app.main.utils.decorators.auth import role_token_required
from faker import Faker

fake = Faker()


# Fixture to set up a test user with a specific role
@pytest.fixture
def setup_test_user_id(test_db):
    # Add a test user with a specific role to the database
    user_id = 1
    return user_id


# Test case for valid token and allowed role
def test_valid_token_and_allowed_role(app, setup_test_user_id):
    auth_token = User.encode_auth_token(setup_test_user_id)
    with app.test_request_context(headers={"Authorization": auth_token}):

        @role_token_required(allowed_roles=[Role.ADMIN])
        def view_function():
            pass

        view_function()

        assert g.user["role"] == Role.ADMIN


# Test case for valid token but disallowed role
def test_valid_token_but_disallowed_role(app, setup_test_user_id):
    auth_token = User.encode_auth_token(setup_test_user_id)
    with app.test_request_context(headers={"Authorization": auth_token}):

        @role_token_required(allowed_roles=[Role.USER])  # Disallowed role
        def view_function():
            pass

        with pytest.raises(BadRequestError):
            view_function()


# Test case for missing token
def test_missing_token(app):
    with app.test_request_context():

        @role_token_required(allowed_roles=[Role.ADMIN])
        def view_function():
            pass

        with pytest.raises(BadRequestError):
            view_function()


# Test case for invalid token
def test_invalid_token(app):
    with app.test_request_context(headers={"Authorization": "invalid_token"}):

        @role_token_required(allowed_roles=[Role.ADMIN])
        def view_function():
            pass

        with pytest.raises(BadRequestError):
            view_function()


def test_valid_token_allowed_role_but_inactive_user(app, setup_test_user_id, test_db):
    # Modify the setup to set up a user with inactive status
    # password = fake.password()
    # new_user = add_user(
    #     db=test_db,
    #     email="New_user@gmail.com",
    #     firstname="New User",
    #     lastname="New User",
    #     password=password,
    # )
    # new_user.status = "suspended"
    # new_user.role = Role.ADMIN
    # new_user.commit
    suspend_user(test_db, setup_test_user_id)
    auth_token = User.encode_auth_token(setup_test_user_id)

    with app.test_request_context(headers={"Authorization": auth_token}):

        @role_token_required(allowed_roles=[Role.ADMIN])
        def view_function():
            pass

        # Expect BadRequestError to be raised due to inactive user
        with pytest.raises(BadRequestError):
            view_function()
