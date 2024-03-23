from typing import Dict, List
from app.main.model.api_category_model import ApiCategory
from app.main import db


class ApiCategoryService:
    @staticmethod
    def create_category(data: Dict, user_id: str) -> ApiCategory:
        new_category = ApiCategory(
            name=data["name"],
            description=data["description"],
            created_by=user_id,
        )
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def get_all_categories() -> List[ApiCategory]:
        return ApiCategory.query.all()
