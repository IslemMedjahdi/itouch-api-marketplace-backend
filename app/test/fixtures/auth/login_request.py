import os
from faker import Faker

fake = Faker()

def login_request(email: str = None , password: str = None):
    return {
        'email': email or fake.email(),
        'password': password or fake.password(),
    } 

def admin_login(email: str = None , password: str = None):
    return {    
        'email':email or  os.getenv('DEFAULT_ADMIN_EMAIL','admin@itouch.com'),
        'password': password or os.getenv('DEFAULT_ADMIN_PASSWORD','admin123')
    }
