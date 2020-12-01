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

    def post(self):
        req_data = request.get_json()

        home_id = req_data['code']
        filters = dict()
        filters['code'] = home_id

        check = homeService.save(filters, req_data)

        if check:
            return "ok", 200
        else:
            return "ko", 500

    def delete(self):

        filters = request.args.to_dict()

        check = homeService.delete(filters)

        if check:
            return "ok", 200
        else:
            return "ko", 500
