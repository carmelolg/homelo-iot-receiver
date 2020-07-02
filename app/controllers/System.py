from flask_restplus import Resource


class System(Resource):

    def get(self):
        return "pong"
