import os
from flask.testing import FlaskClient
from app.test.fixtures.auth.login_request import login_request, admin_login
from app.test.fixtures.auth.register_request import register_request
from app.test.fixtures.user.suppliers_request import create_supplier_request
from app.test.fixtures.user.users_request import get_all_users_request, update_request, update_password_request



def test_get_all_users(client: FlaskClient):

    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    response = client.get('/users/', headers={'Authorization': token})

    assert response.status_code == 200
    assert 'data' in response.json
    assert 'pagination' in response.json
    #do we need to add other assert ?



def test_successfull_get_singel_user(client: FlaskClient):

    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    #create the user
    register_request_data = register_request()
    new_user_response  = client.post('/users/', headers={'Authorization': token}, json=register_request_data)
    assert new_user_response.status_code == 201
    user_id = new_user_response.json['data']['id']

    #the request to get the user
    response = client.get(f'/users/{user_id}', headers={'Authorization': token})
    assert response.status_code == 200
    assert response.json['data']['id'] == user_id
    assert response.json['data']['firstname'] == register_request_data['firstname']  
    assert response.json['data']['lastname'] == register_request_data['lastname']

def test_get_singel_user_with_non_existent_id(client: FlaskClient):

    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    non_existent_user_response = client.get('/users/9999', headers={'Authorization': token})
    assert non_existent_user_response.status_code == 404
   

def test_successful_create_new_user(client: FlaskClient):
    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']
    response = client.post('/users/', json=register_request(), headers={'Authorization': token})

    assert response.status_code == 201

def test_create_new_user_with_invalid_email(client: FlaskClient):
    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']
    response = client.post('/users/', json=register_request(email='abc13@'), headers={'Authorization': token})

    assert response.status_code == 400

def test_create_new_user_with_existing_email(client: FlaskClient):
    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    register_request_data = register_request()
    response = client.post('/users/', json=register_request_data, headers={'Authorization': token})

    assert response.status_code == 201

    response = client.post('/users/', json=register_request_data, headers={'Authorization': token})
    
    assert response.status_code == 409


def test_successfull_suspend_user(client: FlaskClient):

    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    #create the user
    new_user_response  = client.post('/users/', json=register_request(), headers={'Authorization': token})
    assert new_user_response.status_code == 201
    user_status = new_user_response.json['data']['status']
    user_id = new_user_response.json['data']['id']

    #the request to suspend the user
    response = client.patch(f'/users/{user_id}/suspend', headers={'Authorization': token})
    assert response.status_code == 200

    #the request to get the user and then check that the status changed to suspended
    response = client.get(f'/users/{user_id}', headers={'Authorization': token})
    assert response.status_code == 200
    assert response.json['data']['id'] == user_id
    assert response.json['data']['status'] == 'suspended'
    



def test_suspend_user_with_non_existent_id(client: FlaskClient):

    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    non_existent_user_response = client.patch('/users/9999/suspend', headers={'Authorization': token})
    assert non_existent_user_response.status_code == 404




def test_successfull_activate_user(client: FlaskClient):

    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    #create the user
    new_user_response  = client.post('/users/', json=register_request(), headers={'Authorization': token})
    assert new_user_response.status_code == 201
    user_status = new_user_response.json['data']['status']
    user_id = new_user_response.json['data']['id']

    #suspend the user
    suspend_response = client.patch(f'/users/{user_id}/suspend', headers={'Authorization': token})
    assert suspend_response.status_code == 200

    #activate the user
    response = client.patch(f'/users/{user_id}/activate', headers={'Authorization': token})
    assert response.status_code == 200

    #the request to get the user and then check that the status changed to active
    response = client.get(f'/users/{user_id}', headers={'Authorization': token})
    assert response.status_code == 200
    assert response.json['data']['id'] == user_id
    assert response.json['data']['status'] == 'active'



def test_activate_user_with_non_existent_id(client: FlaskClient):

    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    non_existent_user_response = client.patch('/users/9999/activate', headers={'Authorization': token})
    assert non_existent_user_response.status_code == 404




def test_successful_create_new_supplier(client: FlaskClient):
    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']
    response = client.post('/users/suppliers', json=create_supplier_request(), headers={'Authorization': token})

    assert response.status_code == 201

def test_create_new_supplier_with_invalid_email(client: FlaskClient):
    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']
    response = client.post('/users/suppliers', json=create_supplier_request(email='abc13@'), headers={'Authorization': token})

    assert response.status_code == 400

def test_create_new_supplier_with_existing_email(client: FlaskClient):
    login_response = client.post('/auth/login', json=admin_login())
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']

    create_supplier_request_data = create_supplier_request()
    response = client.post('/users/suppliers', json=create_supplier_request_data, headers={'Authorization': token})

    assert response.status_code == 201

    response = client.post('/users/suppliers', json=create_supplier_request_data, headers={'Authorization': token})
    
    assert response.status_code == 409



def test_update(client: FlaskClient):
    register_request_data = register_request()
    response = client.post('/auth/register', json=register_request_data)

    assert response.status_code == 201

    login_request_data = login_request(email=register_request_data['email'], password=register_request_data['password'])
    login_response = client.post('/auth/login', json=login_request_data)
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']
    update_request_data = update_request()

    response = client.patch('/users/update', headers={'Authorization': token}, json=update_request_data)
    assert response.status_code == 200
    user_id = response.json['data']['id']

    #the request to get the user and then check that the user info has been changed
    response = client.get('auth/me', headers={'Authorization': token})
    assert response.status_code == 200
    assert response.json['data']['id'] == user_id
    assert response.json['data']['firstname'] == update_request_data['firstname']
    assert response.json['data']['lastname'] == update_request_data['lastname']


def test_update_password_with_invalide_current_password(client: FlaskClient):
    register_request_data = register_request()
    response = client.post('/auth/register', json=register_request_data)

    assert response.status_code == 201

    login_request_data = login_request(email=register_request_data['email'], password=register_request_data['password'])
    login_response = client.post('/auth/login', json=login_request_data)
    
    assert login_response.status_code == 200

    token = login_response.json['Authorization']
    update_password_request_data = update_password_request(new_password="newpassword123", current_pssword="not very true current password")

    response = client.patch('/users/password', headers={'Authorization': token}, json = update_password_request_data)
    assert response.status_code == 400


