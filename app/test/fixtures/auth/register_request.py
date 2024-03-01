from faker import Faker

fake = Faker()

def register_request(email: str = None, password: str = None,first_name: str = None,last_name: str = None):
    return {
        'email': email or fake.email(),
        'password': password or fake.password(),
        'firstname': first_name or fake.first_name(),
        'lastname': last_name or fake.last_name()
    } 
