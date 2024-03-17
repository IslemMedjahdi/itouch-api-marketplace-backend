from typing import Dict, List
from app.main.model.discussion_model import Discussion
from app.main.model.discussion_answer_model import DiscussionAnswer
from app.main import db
from app.main.utils.exceptions import NotFoundException
from app.main.model.api_model import ApiModel


class DiscussionService:
    @staticmethod
    def get_all_by_api_id(api_id: int) -> List[Discussion]:
        if ApiModel.query.filter_by(id=api_id).first() is None:
            raise NotFoundException("No API found with id: {}".format(api_id))
        discussions = Discussion.query.filter_by(api_id=api_id).all()
        return discussions

    @staticmethod
    def get_by_id(discussion_id: int) -> Discussion:
        discussion = Discussion.query.filter_by(id=discussion_id).first()
        if not discussion:
            raise NotFoundException(
                "No discussion found with id: {}".format(discussion_id)
            )
        return discussion

    @staticmethod
    def create_new_discussion(api_id: int, data: Dict, user_id) -> Discussion:
        if ApiModel.query.filter_by(id=api_id).first() is None:
            raise NotFoundException("No API found with id: {}".format(api_id))
        new_discussion = Discussion(
            title=data["title"],
            question=data["question"],
            user_id=user_id,
            api_id=api_id,
        )
        db.session.add(new_discussion)
        db.session.commit()
        return new_discussion

    @staticmethod
    def delete_discussion(discussion_id: int):
        if Discussion.query.filter_by(id=discussion_id).first() is None:
            raise NotFoundException(
                "No discussion found with id: {}".format(discussion_id)
            )
        discussion = Discussion.query.filter_by(id=discussion_id).first()
        db.session.delete(discussion)
        db.session.commit()
        return discussion

    @staticmethod
    def create_new_answer(discussion_id, data: Dict, user_id: int):
        if Discussion.query.filter_by(id=discussion_id).first() is None:
            raise NotFoundException(
                "No discussion found with id: {}".format(discussion_id)
            )

        new_answer = DiscussionAnswer(
            discussion_id=discussion_id,
            user_id=user_id,
            answer=data["answer"],
        )
        db.session.add(new_answer)
        db.session.commit()
        return new_answer

    @staticmethod
    def get_answer_by_id(answer_id: int) -> DiscussionAnswer:
        answer = DiscussionAnswer.query.filter_by(id=answer_id).first()
        if not answer:
            raise NotFoundException("No answer found with id: {}".format(answer_id))

        return answer

    @staticmethod
    def delete_answer(answer_id: int) -> DiscussionAnswer:
        answer = DiscussionAnswer.query.filter_by(id=answer_id).first()
        if not answer:
            raise NotFoundException("No answer found with id: {}".format(answer_id))
        db.session.delete(answer)
        db.session.commit()
        return answer
