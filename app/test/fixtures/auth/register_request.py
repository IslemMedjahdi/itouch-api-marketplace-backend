import os

def register_request(email: str = None, password: str = None,first_name: str = None,last_name: str = None):
    return {
        'email': email or 'test_user@gmail.com',
        'password': password or '123456',
        'firstname': first_name or 'Test',
        'lastname': last_name or 'User'
    } 