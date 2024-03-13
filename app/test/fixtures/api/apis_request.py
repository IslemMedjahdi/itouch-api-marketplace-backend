import faker

fake = faker.Faker()

def create_api_request(name: str = None, description: str = None, plans: list = None):
    api_data = {
        'name': name or fake.name(),
        'description': description or fake.paragraph(),
        'plans': plans or []
    }
    return api_data

def create_plan(name: str = None, description: str = None, price: int = 0, max_requests: int = 0, duration: int = 0):
    return {
        'name': name or fake.word(),
        'description': description or fake.sentence(),
        'price': price or fake.random_int(min=1, max=100),
        'max_requests': max_requests or fake.random_int(min=1, max=1000),
        'duration': duration or fake.random_int(min=1, max=365)
    }
