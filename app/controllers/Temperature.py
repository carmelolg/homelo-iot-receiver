from datetime import datetime, timedelta

from flask_restplus import Resource

from app.services.HomeService import HomeService
from app.services.SensorService import SensorService

sensorService = SensorService()
homeService = HomeService()


class Temperature(Resource):

    def get(self):
        # Get all rooms
        rooms = homeService.getAllRooms()

        # Prepare response json
        all = {}

        # Prepare filters
        now = datetime.now()
        yesterday = now - timedelta(hours=5000)
        filters = {"startDate": yesterday}

        # For each room get data of last 24h
        for room in rooms:
            filters['room'] = room
            resultDict = sensorService.find(filters)
            if resultDict is not None and len(resultDict) > 0:
                result = list(map(self.innermap, resultDict))
                all[room] = result

        return all

    def innermap(self, object):
        dict = {}
        dict['temperature'] = object.get('temperature') if object.get('temperature') is not None else 0
        dict['date'] = object.get('date')
        return dict
