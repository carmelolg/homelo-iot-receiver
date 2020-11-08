from flask_restplus import Resource
from datetime import datetime

class System(Resource):

    def get(self):
        return "pong"

    def time(self):
        return datetime.now()