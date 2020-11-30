from flask import request
from flask_restplus import Resource

from app.services.AuthService import AuthService
from app.utils.JWTUtils import JWTUtils
from app.services.SensorService import SensorService

sensorService = SensorService()
jwtUtils = JWTUtils()
authService = AuthService()

class Sensor(Resource):
    
    def get(self):
        filters = request.args.to_dict()

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)
        filters['house'] = house

        return sensorService.find(filters)

    def post(self):

        req_data = request.get_json()

        device_name = req_data['name']
        device_house = req_data['house']
        filters = dict()
        filters['name'] = device_name
        filters['house'] = device_house

        check = sensorService.update(filters, req_data)

        if check:
            return "ok", 200
        else:
            return "ko", 500
