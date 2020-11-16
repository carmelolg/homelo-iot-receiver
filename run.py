
from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS

from app.controllers.System import System
from app.controllers.Sensor import Sensor
from app.controllers.Humidity import Humidity
from app.controllers.Temperature import Temperature
from app.controllers.Home import Home
from app.controllers.HomeParams import HomeParams
from app.controllers.Auth import Auth
from app.services.JwtService import JwtService

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Sensor, '/sensor')
api.add_resource(Home, '/home')
api.add_resource(Auth, '/auth')
api.add_resource(HomeParams, '/params')
api.add_resource(Humidity, '/humidity')
api.add_resource(Temperature, '/temperature')
api.add_resource(System, '/ping')

jwtService = JwtService()

@app.before_request
def intercept_request():
    if request.path == '/auth':
        return None
    elif request.headers.get('jwt') is None or jwtService.check(request.headers.get('jwt')) is False:
        return jsonify({'message': 'Token is not valid'}), 401
    else:
        return None

@app.route('/')
def index():
    return "Not authorized", 401


if __name__ == '__main__':
    app.run(debug=True)
