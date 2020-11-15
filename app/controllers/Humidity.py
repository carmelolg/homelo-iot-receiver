from datetime import timedelta, datetime

import json
from flask_restplus import Resource

from app.services.SensorService import SensorService
from app.services.HomeService import HomeService

sensorService = SensorService()
homeService = HomeService()


class Humidity(Resource):

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
        dict['humidity'] = object.get('humidity') if object.get('humidity') is not None else 0
        dict['date'] = object.get('date')
        return dict