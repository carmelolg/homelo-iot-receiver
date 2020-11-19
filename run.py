from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api

from app.controllers.Auth import Auth
from app.controllers.Home import Home
from app.controllers.HomeParams import HomeParams
from app.controllers.Humidity import Humidity
from app.controllers.Detection import Detection
from app.controllers.System import System
from app.controllers.Temperature import Temperature
from app.controllers.Sensor import Sensor
from app.services.JwtService import JwtService

app = Flask(__name__)
api = Api(app)

CORS(app)

api.add_resource(Sensor, '/sensor')
api.add_resource(Detection, '/detection')
api.add_resource(Home, '/home')
api.add_resource(Auth, '/auth')
api.add_resource(HomeParams, '/params')
api.add_resource(Humidity, '/humidity')
api.add_resource(Temperature, '/temperature')
api.add_resource(System, '/ping')

jwtService = JwtService()

@app.before_request
def intercept_request():
    if request.method == 'OPTIONS' or request.path == '/auth' or request.path == '/ping':
        return None
    else:
        authorization = request.headers.get('Authorization')
        if authorization is not None:
            auth_splitted = authorization.split()
            if len(auth_splitted) < 2:
                return jsonify({'message': 'Token is not valid'}), 401
            else:
                _jwt = auth_splitted[1]
                if jwtService.check(_jwt) is False:
                    return jsonify({'message': 'Token is not valid'}), 401
                else:
                    return None
        else:
            return jsonify({'message': 'Token is not valid'}), 401


@app.route('/')
def index():
    return "Not authorized", 401


if __name__ == '__main__':
    app.run(debug=True)
