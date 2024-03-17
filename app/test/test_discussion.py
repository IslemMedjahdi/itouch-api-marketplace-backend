import pytest
from app.main.service.discussion_service import DiscussionService
from app.main.model.discussion_model import Discussion
from app.main.model.discussion_answer_model import DiscussionAnswer
from app.main.utils.exceptions import NotFoundException


def test_get_all_by_api_id():
    api_id = 1
    add_discussion(api_id=api_id, title="Test Discussion", question="Test Question")
    discussions = DiscussionService.get_all_by_api_id(api_id)
    assert len(discussions) == 1
    assert discussions[0].api_id == api_id


def test_get_by_id_not_found():
    with pytest.raises(NotFoundException):
        DiscussionService.get_by_id(999)


def test_get_by_id():
    discussion = add_discussion(
        api_id=1, title="Test Discussion", question="Test Question"
    )
    fetched_discussion = DiscussionService.get_by_id(discussion.id)
    assert fetched_discussion.id == discussion.id


def test_create_new_discussion():
    api_id = 1
    data = {"title": "New Discussion", "question": "New Question"}
    new_discussion = DiscussionService.create_new_discussion(api_id, data)
    assert new_discussion.title == data["title"]
    assert new_discussion.question == data["question"]


def test_delete_discussion():
    discussion = add_discussion(
        api_id=1, title="Test Discussion", question="Test Question"
    )
    deleted_discussion = DiscussionService.delete_discussion(discussion.id)
    assert deleted_discussion.id == discussion.id
    assert Discussion.query.get(deleted_discussion.id) is None


def test_create_new_answer():
    discussion = add_discussion(
        api_id=1, title="Test Discussion", question="Test Question"
    )
    data = {"answer": "Test Answer"}
    new_answer = DiscussionService.create_new_answer(discussion.id, data)
    assert new_answer.answer == data["answer"]
    assert new_answer.discussion_id == discussion.id


def test_get_answer_by_id():
    discussion = add_discussion(
        api_id=1, title="Test Discussion", question="Test Question"
    )
    answer = add_answer(discussion_id=discussion.id, answer="Test Answer")
    fetched_answer = DiscussionService.get_answer_by_id(answer.id)
    assert fetched_answer.id == answer.id


def test_delete_answer():
    discussion = add_discussion(
        api_id=1, title="Test Discussion", question="Test Question"
    )
    answer = add_answer(discussion_id=discussion.id, answer="Test Answer")
    deleted_answer = DiscussionService.delete_answer(answer.id)
    assert deleted_answer.id == answer.id
    assert DiscussionAnswer.query.get(deleted_answer.id) is None
