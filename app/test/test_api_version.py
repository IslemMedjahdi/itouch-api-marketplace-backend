import pytest

from app.main.utils.exceptions import NotFoundError, BadRequestError
from app.main.model.api_category_model import ApiCategory
from app.main.model.api_model import ApiModel
from app.main.model.user_model import User
from app.main.model.api_version_model import ApiVersion
from app.main.utils.roles import Role
from app.main.core.services.api_version_service import ApiVersionService
from faker import Faker


fake = Faker()
api_version_service = ApiVersionService()


@pytest.fixture
def mock_data(test_db):
    password = fake.password()
    supplier = User(
        email="supplier@gmail.com",
        firstname="supplier",
        lastname="supplier",
        password=password,
        role=Role.SUPPLIER,
    )
    category = ApiCategory(
        name="Test category", description="Test category Description", created_by=1
    )

    test_db.session.add_all([supplier, category])
    test_db.session.commit()
    api = ApiModel(
        name="API",
        description="API Description",
        supplier_id=supplier.id,
        category_id=category.id,
        status="active",
    )
    test_db.session.add(api)
    test_db.session.commit()
    yield supplier, category, api
    objects_to_delete = [
        supplier,
        category,
        api,
    ]
    for obj in objects_to_delete:
        test_db.session.delete(obj)
    test_db.session.commit()


def test_create_api_version_valid(mock_data):
    supplier, category, api = mock_data
    data = {
        "version": "1.0.0",
        "base_url": "https://example.com/api/v1",
        "endpoints": [
            {
                "url": "/users",
                "method": "GET",
                "description": "Get a list of users",
                "request_body": "",
                "response_body": '"users":"id": 1, "name": "John Doe"',
            }
        ],
        "headers": [{"key": "Authorization", "value": "Bearer token"}],
    }

    api_version_service.create_api_version(api.id, supplier.id, data)

    version = ApiVersion.query.filter_by(api_id=api.id, version=data["version"]).first()
    assert version is not None
    assert version.base_url == data["base_url"]
    assert version.status == "active"


def test_create_api_version_not_found(mock_data):
    supplier = mock_data[0]
    data = {"version": "1.0.0", "base_url": "https://example.com/api/v1"}

    with pytest.raises(NotFoundError, match=r"No API found with id: \d+"):
        api_version_service.create_api_version(999, supplier.id, data)


def test_create_api_version_already_exists(test_db, mock_data):
    supplier, category, api = mock_data
    data = {"version": "2.0.0", "base_url": "https://example.com/api/v1"}
    api_version = ApiVersion(
        api_id=api.id,
        version=data["version"],
        base_url=data["base_url"],
        status="active",
    )
    test_db.session.add(api_version)
    test_db.session.commit()

    with pytest.raises(BadRequestError, match=r"API version already exists"):
        api_version_service.create_api_version(api.id, supplier.id, data)
