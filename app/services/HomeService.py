#!/usr/bin/python3
import json

from bson import json_util

from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from app.services.DetectionService import DetectionService
from app.services.SensorService import SensorService

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()
detectionService = DetectionService()
sensorService = SensorService()


class HomeService(object):

    def save(self, filters, data):
        # Update sensor
        result = db.Home.update_one(filters, {'$set': data}, True)
        return result.acknowledged

    def delete(self, filters):
        # Update sensor
        result = db.Home.delete_many(filters)
        return result.acknowledged

    def find(self, code):

        filters = dict()
        if code is not None:
            filters['code'] = code

        # Create query
        query = db.Home.find(filters, {'_id': False}).sort("_id", -1).limit(1)[0]

        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def findAll(self):

        # Create query
        query = db.Home.find({}, {'_id': False}).sort("_id", -1)

        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def getAllParams(self, code):
        # Create query for retrieve all house rooms
        rooms = self.find(code).get('rooms')

        allParams = {"data": []}

        # For each room get the last sensor data and put on response
        for room in rooms:

            sensors = sensorService.find({'house': code, 'room': room})

            params = dict()
            filters = dict()
            filters['house'] = code
            filters['room'] = room
            filters['limit'] = 1

            if sensors is not None and len(sensors) > 0:
                for sensor in sensors:
                    if sensor['temperature']:
                        filters['metrics'] = ['temperature', 'heatIndex', 'humidity']
                        detectionResults = detectionService.find(filters)
                        if detectionResults is not None and detectionResults['data'] is not None and len(
                                detectionResults['data']) > 0:
                            detectionResult = detectionResults['data'][0]
                            params['temperature'] = detectionResult['temperature']
                            params['humidity'] = detectionResult['humidity']
                            params['heatIndex'] = detectionResult['heatIndex']
                            params['date'] = detectionResult['date']
                    if sensor['movement']:
                        filters['metrics'] = ['movement']
                        detectionResults = detectionService.find(filters)
                        if detectionResults is not None and detectionResults['data'] is not None and len(
                                detectionResults['data']) > 0:
                            detectionResult = detectionResults['data'][0]
                            params['movement'] = detectionResult['movement']
                            params['date'] = detectionResult['date']
                    if sensor['gas']:
                        filters['metrics'] = ['gas']
                        detectionResults = detectionService.find(filters)
                        if detectionResults is not None and detectionResults['data'] is not None and len(
                                detectionResults['data']) > 0:
                            detectionResult = detectionResults['data'][0]
                            params['gas'] = detectionResult['gas']
                            params['date'] = detectionResult['date']

                params['house'] = code
                params['room'] = room
                allParams.get('data').append(params)

            # resultDict = detectionService.findByRoom(code, room)
            # if resultDict is not None and len(resultDict) > 0:
            #    allParams.get('data').append(resultDict[0])

        return allParams

    def getAllRooms(self, code):
        return self.find(code).get('rooms')
