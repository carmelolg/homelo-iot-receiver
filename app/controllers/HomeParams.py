from flask_restplus import Resource

from app.services.HomeService import HomeService

homeService = HomeService();

class HomeParams(Resource):
    
    def get(self):
        return homeService.getAllParams();
