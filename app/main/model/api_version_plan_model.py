from app.main import db

class ApiVersionPlan(db.Model):

    __tablename__ = "api_version_plan"

    api_id = db.Column(db.Integer, db.ForeignKey('api_version.api_id'),primary_key=True)
    api_version = db.Column(db.String, db.ForeignKey('api_version.version'),primary_key=True)
    name = db.Column(db.String, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer)
    max_requests = db.Column(db.Integer)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return "<ApiVersionPlan '{}'>".format(self.name)
    
    def __str__(self):
        return self.name