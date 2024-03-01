import os

def login_request(email: str = None , password: str = None):
    return {
        'email': email or os.getenv('DEFAULT_ADMIN_EMAIL','admin@itouch.com'),
        'password': password or os.getenv('DEFAULT_ADMIN_PASSWORD','admin123'),
    } 