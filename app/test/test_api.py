import os
from flask.testing import FlaskClient
from app.test.fixtures.auth.login_request import login_request, admin_login
from app.test.fixtures.auth.register_request import register_request
from app.test.fixtures.api.categories_request import create_category_request



def test_get_all_categories(client: FlaskClient):
    response = client.get('/apis/categories')  

    assert response.status_code == 200
    assert 'data' in response.json
    #do we need to add other assert ?


def test_successful_create_new_category(client: FlaskClient):
    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']
    create_category_request_data = create_category_request()
    response = client.post('/apis/categories/create', json=create_category_request_data, headers={'Authorization': token})

    assert response.status_code == 201
    assert response.json['data']['name'] == create_category_request_data['name']  
    assert response.json['data']['description'] == create_category_request_data['description']


