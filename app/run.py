
from flask import Flask
from flask_restful import Api

import sys
sys.path.insert(1, '/controllers')


from controllers.System import System
from controllers.Sensor import Sensor


app = Flask(__name__)
api = Api(app)

api.add_resource(Sensor, '/sensor')
api.add_resource(System, '/ping')


@app.route('/')
def index():
    return "Not authorized", 401


if __name__ == '__main__':
    app.run(debug=True)
