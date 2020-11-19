from flask import request
from flask_restplus import Resource

from app.utils.JWTUtils import JWTUtils
from app.services.AuthService import AuthService
from app.services.DetectionService import DetectionService

detectionService = DetectionService()
jwtUtils = JWTUtils()
authService = AuthService()

class Detection(Resource):
    
    def get(self):
        filters = request.args.to_dict()

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)
        filters['house'] = house

        return detectionService.find(filters)

    def post(self):

        req_data = request.get_json()
        print("Dati rilevati: ", req_data)

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)
        req_data['house'] = house

        check = detectionService.save(req_data)

        if check:
            return "ok", 200
        else:
            return "ko", 500
