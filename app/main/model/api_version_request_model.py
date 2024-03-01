from app.main import db

class ApiVersionRequest(db.Model):
    __tablename__ = "api_version_request"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_id = db.Column(db.Integer, db.ForeignKey('api_version.api_id'), primary_key=True)
    api_version = db.Column(db.String, db.ForeignKey('api_version.version'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    api_key_id = db.Column(db.Integer, db.ForeignKey('api_version_key.id'), primary_key=True)
    request_at = db.Column(db.DateTime())
    request_end_at = db.Column(db.DateTime(),server_default=db.func.now())
    request_params = db.Column(db.String(255), nullable=False)
    request_query = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<ApiVersionRequest '{}'>".format(self.name)
    
    def __str__(self):
        return self.name