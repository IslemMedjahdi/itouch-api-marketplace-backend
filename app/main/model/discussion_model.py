from app.main import db


class Discussion(db.Model):
    __tablename__ = "discussion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    api_id = db.Column(
        db.Integer, db.ForeignKey("api.id"), primary_key=True, nullable=False
    )
    answers = db.relationship("DiscussionAnswer")
    user = db.relationship("User", backref="discussions")

    def __repr__(self):
        return "<Discussion '{}'>".format(self.id)

    def __str__(self):
        return self.id
