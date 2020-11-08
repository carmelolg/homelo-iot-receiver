
from flask import Flask
from flask_restful import Api

from app.controllers.System import System
from app.controllers.Sensor import Sensor
from app.controllers.Time import Time

app = Flask(__name__)
api = Api(app)

api.add_resource(Sensor, '/sensor')
api.add_resource(System, '/ping')
api.add_resource(Time, '/time')


@app.route('/')
def index():
    return "Not authorized", 401


if __name__ == '__main__':
    app.run(debug=True)
