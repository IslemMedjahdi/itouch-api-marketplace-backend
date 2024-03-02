from flask_restx import Namespace, fields

class ApiDto:
    api = Namespace('Api', description='api related operations')
