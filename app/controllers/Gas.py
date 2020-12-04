from flask import request
from flask_restplus import Resource

from app.services.AuthService import AuthService
from app.services.MetricService import MetricService
from app.utils.JWTUtils import JWTUtils

authService = AuthService()
jwtUtils = JWTUtils()
metricService = MetricService()


class Gas(Resource):

    def get(self):
        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)

        return metricService.findLast24HData(['gas'], house)
