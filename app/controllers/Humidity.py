from flask_restplus import Resource

from app.services.MetricService import MetricService

from flask import request
from app.services.AuthService import AuthService
from app.utils.JWTUtils import JWTUtils

authService = AuthService()
jwtUtils = JWTUtils()
metricService = MetricService()

class Humidity(Resource):

    def get(self):

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)

        return metricService.findLast24HData('humidity', house)