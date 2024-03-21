from app.main import db
from sqlalchemy import UniqueConstraint


class AnswerVote(db.Model):
    __tablename__ = "answer_vote"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    answer_id = db.Column(
        db.Integer, db.ForeignKey("discussion_answer.id"), nullable=False
    )
    vote = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (UniqueConstraint("user_id", "answer_id", name="user_answer_uc"),)

    def __repr__(self):
        return "<AnswerVote '{}'>".format(self.id)

    def __str__(self):
        return self.id
