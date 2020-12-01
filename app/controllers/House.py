from flask_restplus import Resource

from app.services.HomeService import HomeService

homeService = HomeService()


class House(Resource):

    def get(self):
        return homeService.findAll()
