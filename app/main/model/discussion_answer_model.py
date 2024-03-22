from app.main import db


class DiscussionAnswer(db.Model):  # type: ignore
    __tablename__ = "discussion_answer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discussion_id = db.Column(
        db.Integer, db.ForeignKey("discussion.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    answer = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship("User", backref="answers")
    votes = db.relationship("AnswerVote", lazy="dynamic")

    @property
    def votes_count(self):
        return (
            self.votes.filter_by(vote="up").count()
            - self.votes.filter_by(vote="down").count()
        )

    def __repr__(self):
        return "<DiscussionAnswer '{}'>".format(self.id)

    def __str__(self):
        return self.id
