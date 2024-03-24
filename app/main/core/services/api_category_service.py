from typing import Dict, List
from app.main.model.api_category_model import ApiCategory
from app.main import db


class ApiCategoryService:
    def create_category(self, data: Dict, user_id: str) -> ApiCategory:
        new_category = ApiCategory(
            name=data["name"],
            description=data["description"],
            created_by=user_id,
        )
        db.session.add(new_category)
        db.session.commit()
        return new_category

    def get_all_categories(self) -> List[ApiCategory]:
        return ApiCategory.query.all()
