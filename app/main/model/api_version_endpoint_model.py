from app.main import db

class ApiVersionEndpoint(db.Model):

    __tablename__ = "api_version_endpoint"

    api_id = db.Column(db.Integer, db.ForeignKey('api_version.api_id'),primary_key=True)
    version = db.Column(db.String,db.ForeignKey('api_version.version'),primary_key=True)
    endpoint = db.Column(db.String, primary_key=True)
    method = db.Column(db.String, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    request_body = db.Column(db.String(2048), nullable=False)
    response_body = db.Column(db.String(2048), nullable=False)

    def __repr__(self):
        return "<ApiVersionEndpoint '{}'>".format(self.endpoint)
    
    def __str__(self):
        return self.endpoint