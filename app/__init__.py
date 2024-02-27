import os
from app.main import create_app
 
app = create_app(os.getenv('FLASK_ENV',"dev"))

