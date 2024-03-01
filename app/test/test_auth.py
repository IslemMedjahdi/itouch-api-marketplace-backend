import os
from flask.testing import FlaskClient
from app.test.fixtures.auth.login_request import login_request
from app.test.fixtures.auth.register_request import register_request


def test_successfull_login(client: FlaskClient):
    response = client.post('/auth/login', json=login_request())

    assert response.status_code == 200
    assert 'Authorization' in response.json

def test_login_with_not_found_email(client: FlaskClient):
    response = client.post('/auth/login', json=login_request(email='not_found@itouch.com'))

    assert response.status_code == 404
    assert 'Authorization' not in response.json

def test_login_with_invalid_password(client: FlaskClient):
    response = client.post('/auth/login', json=login_request(password='123'))

    assert response.status_code == 400
    assert 'Authorization' not in response.json

def test_successful_register(client: FlaskClient):
    response = client.post('/auth/register', json=register_request())

    assert response.status_code == 201

def test_register_with_invalid_email(client: FlaskClient):
    response = client.post('/auth/register', json=register_request(email='abc13@'))

    assert response.status_code == 400

def test_register_with_existing_email(client: FlaskClient):
    response = client.post('/auth/register', json=register_request(email = 'test1@itouch.com'))

    assert response.status_code == 201

    response = client.post('/auth/register', json=register_request(email = 'test1@itouch.com'))
    
    assert response.status_code == 409