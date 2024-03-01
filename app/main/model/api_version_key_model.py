from app.main import db

class ApiVersionKey(db.Model):

    __tablename__ = "api_version_key"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api_version.api_id'), primary_key=True)
    api_version = db.Column(db.String, db.ForeignKey('api_version.version'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    expires_at = db.Column(db.DateTime(), nullable=False)
    max_requests = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<ApiVersionKey '{}'>".format(self.name)
    
    def __str__(self):
        return self.name
