from flask_restplus import Resource
from flask import request
from app.services.HomeService import HomeService
from app.services.AuthService import AuthService
from app.utils.JWTUtils import JWTUtils

homeService = HomeService()
authService = AuthService()
jwtUtils = JWTUtils()

class Home(Resource):

    def get(self):

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)
        if len(house) > 0:
            return homeService.find(house)
        else:
            return None