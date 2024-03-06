from faker import Faker


fake = Faker()

def create_category_request(name: str = None, description: str = None):
    return {
        'name': name or fake.name(),
        'description': description or fake.paragraph()
    } 

