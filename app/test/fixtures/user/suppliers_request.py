from faker import Faker
from app.main.utils.roles import Role


fake = Faker()

def create_supplier_request(email: str = None, password: str = None,first_name: str = None,last_name: str = None):
    return {
        'email': email or fake.email(),
        'password': password or fake.password(),
        'firstname': first_name or fake.first_name(),
        'lastname': last_name or fake.last_name(),
        'role' : Role.SUPPLIER
    } 

