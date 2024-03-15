from typing import Dict, List
from app.main.model.discussion_model import Discussion
from app.main.model.discussion_answer_model import DiscussionAnswer
from app.main import db


class DiscussionService:
    @staticmethod
    def get_all_by_api_id(api_id: int) -> List[Discussion]:
        discussions = Discussion.query.filter_by(api_id=api_id).all()
        return discussions

    @staticmethod
    def get_by_id(discussion_id: int) -> Discussion:
        return Discussion.query.filter_by(id=discussion_id).first()

    @staticmethod
    def create_new_discussion(api_id: int, data: Dict) -> Discussion:
        new_discussion = Discussion(
            title=data["title"],
            question=data["question"],
            user_id=1,  # TODO get user id from token
            api_id=api_id,
        )
        db.session.add(new_discussion)
        db.session.commit()
        return new_discussion

    @staticmethod
    def delete_discussion(discussion_id: int):
        discussion = Discussion.query.filter_by(id=discussion_id).first()
        db.session.delete(discussion)
        db.session.commit()
        return discussion

    @staticmethod
    def create_new_answer(discussion_id, data: Dict):
        new_answer = DiscussionAnswer(
            discussion_id=discussion_id,
            user_id=1,  # TODO get user id from token
            answer=data["answer"],
        )
        db.session.add(new_answer)
        db.session.commit()
        return new_answer

    @staticmethod
    def get_answer_by_id(answer_id: int) -> DiscussionAnswer:
        return DiscussionAnswer.query.filter_by(id=answer_id).first()

    @staticmethod
    def delete_answer(answer_id: int):
        answer = DiscussionAnswer.query.filter_by(id=answer_id).first()
        db.session.delete(answer)
        db.session.commit()
        return answer
