#!/usr/bin/python3
import json

from bson import json_util

from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from app.services.DetectionService import DetectionService

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()
sensorService = DetectionService()

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

        #Create query
        query = db.Home.find(filters, {'_id': False}).sort("_id", -1).limit(1)[0]

        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def findAll(self):

        #Create query
        query = db.Home.find({}, {'_id': False}).sort("_id", -1)

        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def getAllParams(self, code):
        # Create query for retrieve all house rooms
        rooms = self.find(code).get('rooms')

        allParams = {"data": []}

        # For each room get the last sensor data and put on response
        for room in rooms:
            resultDict = sensorService.findByRoom(code, room)
            if resultDict is not None and len(resultDict) > 0:
                allParams.get('data').append(resultDict[0])

        return allParams

    def getAllRooms(self, code):
        return self.find(code).get('rooms')

