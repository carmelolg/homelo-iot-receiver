
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from app.controllers.System import System
from app.controllers.Sensor import Sensor
from app.controllers.Humidity import Humidity
from app.controllers.Temperature import Temperature
from app.controllers.Home import Home
from app.controllers.HomeParams import HomeParams

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Sensor, '/sensor')
api.add_resource(Home, '/home')
api.add_resource(HomeParams, '/params')
api.add_resource(Humidity, '/humidity')
api.add_resource(Temperature, '/temperature')
api.add_resource(System, '/ping')


@app.route('/')
def index():
    return "Not authorized", 401


if __name__ == '__main__':
    app.run(debug=True)
