
from app.main import db, flask_bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(60))
    lastname = db.Column(db.String(60))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())
    # role can be user or admin or supplier
    role = db.Column(db.String(20), default='user')
    # status can be pending, active, suspended, or deleted
    status = db.Column(db.String(20), default='pending')

    @property
    def password(self):
        raise AttributeError('password: write-only field')
    
    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return "<User '{}'>".format(self.username)