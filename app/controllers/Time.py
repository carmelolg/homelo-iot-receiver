from flask_restplus import Resource
from datetime import datetime

class Time(Resource):

    def get(self):
        return datetime.now().isoformat()