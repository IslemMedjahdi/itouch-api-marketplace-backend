from app.main import db


class ApiKey(db.Model):  # type: ignore

    __tablename__ = "api_key"

    key = db.Column(db.String, primary_key=True)
    api_id = db.Column(db.Integer, db.ForeignKey("api.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<ApiKey '{}'>".format(self.key)

    def __str__(self):
        return self.key
