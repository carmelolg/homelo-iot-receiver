from flask_restplus import Resource

from app.services.HomeService import HomeService

homeService = HomeService();

class Home(Resource):

    def get(self):
        return homeService.find();
