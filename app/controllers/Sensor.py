from flask_restplus import Resource
from flask import request

from services.SensorService import SensorService

SensorService
sensorService = SensorService()


class SensorItem:
    def __init__(self, date, temperature):
        self.date = date
        self.temperature = temperature


class Sensor(Resource):

    def post(self):
        req_data = request.get_json()
        print("Dati rilevati: ", req_data)

        check = sensorService.save(req_data)

        if check:
            return "ok", 200
        else:
            return "ko", 500
