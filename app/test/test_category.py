# import pytest
from app.main.core import ServicesInitializer
from app.main.model.api_category_model import ApiCategory
from .fixtures.category.add_category import add_category


# from app.main.utils.exceptions import NotFoundError

ApiCategoryService = ServicesInitializer.an_api_category_service()


def test_get_all_categories(test_db):
    new_category = add_category(
        db=test_db,
        name="New Category",
        description="New Category description",
        user_id=1,
    )
    categories = ApiCategoryService.get_all_categories()
    assert len(categories) == 1
    assert categories[0].id == new_category.id


def test_create_new_category(test_db):
    data = {"name": "New Category", "description": "New description"}
    new_category = ApiCategoryService.create_category(data, 1)
    assert new_category.name == data["name"]
    assert new_category.description == data["description"]
    category = ApiCategory.query.get(new_category.id)
    assert category is not None
