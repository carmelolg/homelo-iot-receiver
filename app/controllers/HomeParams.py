from flask_restplus import Resource

from flask import request
from app.services.HomeService import HomeService
from app.services.AuthService import AuthService
from app.utils.JWTUtils import JWTUtils

authService = AuthService()
jwtUtils = JWTUtils()
homeService = HomeService();

class HomeParams(Resource):
    
    def get(self):

        user = jwtUtils.getUserFromRequest(request)
        house = authService.getHouse(user)

        return homeService.getAllParams(house)
