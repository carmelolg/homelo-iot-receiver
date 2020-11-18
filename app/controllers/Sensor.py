from flask import request
from flask_restplus import Resource

from app.utils.JWTUtils import JWTUtils
from app.services.AuthService import AuthService
from app.services.SensorService import SensorService

sensorService = SensorService()
jwtUtils = JWTUtils()
authService = AuthService()

class SensorItem:
    def __init__(self, date, temperature):
        self.date = date
        self.temperature = temperature

class Sensor(Resource):
    
    def get(self):
        filters = request.args.to_dict()

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)
        filters['house'] = house

        return sensorService.find(filters)

    def post(self):
        req_data = request.get_json()
        print("Dati rilevati: ", req_data)

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)
        req_data['house'] = house

        check = sensorService.save(req_data)

        if check:
            return "ok", 200
        else:
            return "ko", 500
