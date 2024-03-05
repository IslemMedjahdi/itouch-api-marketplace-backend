import os
from faker import Faker

fake = Faker()

def get_all_users_request(per_page: int = None , page: int = None):
    return {
        'per_page': per_page or fake.per_page(),
        'page': page or fake.page(),
    } 

def update_request(first_name: str = None , last_name: str = None):
    return {
        'firstname': first_name or fake.first_name(),
        'lastname': last_name or fake.last_name(),
    } 

def update_password_request(new_password: str = None , current_pssword: str = None):
    return {
        'new_password': new_password or fake.new_password(),
        'current_pssword': current_pssword or fake.current_pssword(),
    } 




