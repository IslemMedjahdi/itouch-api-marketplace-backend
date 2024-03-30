import pytest

# import unittest
from unittest.mock import Mock

# from app.main.core import ServicesInitializer
from app.main.model.api_category_model import ApiCategory

# from app.main.model.api_model import ApiModel
# from .fixtures.category.add_category import add_category
from app.main.core.services.api_service import ApiService
from app.main.core.lib.impl.media_manager_impl import MediaManagerImpl
from app.main.utils.exceptions import BadRequestError


from app.main.utils.exceptions import NotFoundError

# ApiService = ServicesInitializer.an_api_service()


@pytest.fixture(scope="module")
def test_category(test_db):
    category = ApiCategory(
        name="Test category", description="Test category Description", created_by=1
    )
    test_db.session.add(category)
    test_db.session.commit()
    yield category
    test_db.session.delete(category)
    test_db.session.commit()


@pytest.fixture(scope="module")
def api_service(test_db, test_category):
    mock_chargily_api = Mock()
    mock_chargily_api.create_product.return_value = "product_id"
    mock_chargily_api.create_price.side_effect = ["price_id_1", "price_id_2"]
    return ApiService(media_manager=MediaManagerImpl(), chargily_api=mock_chargily_api)


def test_create_api(api_service, test_category):
    category_id = test_category.id
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": category_id,
        "plans": [
            {
                "name": "Basic Plan",
                "price": 10,
                "description": "Basic plan description",
                "max_requests": 1000,
                "duration": 30,
            },
            {
                "name": "Premium Plan",
                "price": 20,
                "description": "Premium plan description",
                "max_requests": 5000,
                "duration": 90,
            },
        ],
    }
    user_id = 1

    # Act
    api_service.create_api(data, user_id)

    # Assert
    api_service.chargily_api.create_product.assert_called_once_with(
        data["name"], data["description"]
    )
    assert api_service.chargily_api.create_price.call_count == 2
    api_service.chargily_api.create_price.assert_any_call(
        "product_id", data["plans"][0]["price"]
    )
    api_service.chargily_api.create_price.assert_any_call(
        "product_id", data["plans"][1]["price"]
    )


def test_create_api_category_not_found(api_service):
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": 999,  # Non-existent category ID
        "plans": [],
    }
    user_id = 1

    # Act & Assert
    with pytest.raises(NotFoundError):
        api_service.create_api(data, user_id)


def test_create_api_duplicate_plan_names(api_service, test_category):
    category_id = test_category.id
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": category_id,
        "plans": [
            {
                "name": "Basic Plan",
                "price": 10,
                "description": "Basic plan description",
                "max_requests": 1000,
                "duration": 30,
            },
            {
                "name": "Basic Plan",  # Duplicate plan name
                "price": 20,
                "description": "Premium plan description",
                "max_requests": 5000,
                "duration": 90,
            },
        ],
    }
    user_id = 1

    # Act & Assert
    with pytest.raises(BadRequestError):
        api_service.create_api(data, user_id)


def test_create_api_negative_plan_price(api_service, test_category):
    category_id = test_category.id
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": category_id,
        "plans": [
            {
                "name": "Basic Plan",
                "price": -10,  # Negative price
                "description": "Basic plan description",
                "max_requests": 1000,
                "duration": 30,
            },
        ],
    }
    user_id = 1

    # Act & Assert
    with pytest.raises(BadRequestError, match=r"Price cannot be negative"):
        api_service.create_api(data, user_id)


def test_create_api_negative_max_requests(api_service, test_category):
    category_id = test_category.id
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": category_id,
        "plans": [
            {
                "name": "Basic Plan",
                "price": 10,
                "description": "Basic plan description",
                "max_requests": -1000,  # Negative max_requests
                "duration": 30,
            },
        ],
    }
    user_id = 1

    # Act & Assert
    with pytest.raises(BadRequestError, match=r"Max requests cannot be negative"):
        api_service.create_api(data, user_id)


def test_create_api_negative_duration(api_service, test_category):
    category_id = test_category.id
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": category_id,
        "plans": [
            {
                "name": "Basic Plan",
                "price": 10,
                "description": "Basic plan description",
                "max_requests": 1000,
                "duration": -30,  # Negative duration
            },
        ],
    }
    user_id = 1

    # Act & Assert
    with pytest.raises(BadRequestError, match=r"Duration cannot be negative"):
        api_service.create_api(data, user_id)


def test_create_api_chargily_product_creation_failed(
    api_service, test_category, monkeypatch
):
    category_id = test_category.id
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": category_id,
        "plans": [],
    }
    user_id = 1

    # Mock the chargily_api.create_product method to return None
    monkeypatch.setattr(api_service.chargily_api, "create_product", lambda *args: None)

    # Act & Assert
    with pytest.raises(
        BadRequestError, match=r"Failed to create product in chargily API"
    ):
        api_service.create_api(data, user_id)


def test_create_api_chargily_price_creation_failed(
    api_service, test_category, monkeypatch
):
    category_id = test_category.id
    data = {
        "name": "Test API",
        "description": "This is a test API",
        "category_id": category_id,
        "plans": [
            {
                "name": "Basic Plan",
                "price": 10,
                "description": "Basic plan description",
                "max_requests": 1000,
                "duration": 30,
            },
        ],
    }
    user_id = 1

    # Mock the chargily_api.create_price method to return None
    monkeypatch.setattr(api_service.chargily_api, "create_price", lambda *args: None)

    # Act & Assert
    with pytest.raises(
        BadRequestError, match=r"Failed to create price in chargily API"
    ):
        api_service.create_api(data, user_id)
