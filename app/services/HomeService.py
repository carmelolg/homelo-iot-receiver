#!/usr/bin/python3
import json

from bson import json_util

from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from app.services.SensorService import SensorService

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()
sensorService = SensorService()

class HomeService(object):

    def find(self):

        #Create query
        query = db.Home.find({}, {'_id': False}).sort("_id", -1).limit(1)[0]

        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def getAllParams(self):
        # Create query for retrieve all house rooms
        rooms = self.find().get('rooms')

        allParams = {"data": []}

        # For each room get the last sensor data and put on response
        for room in rooms:
            resultDict = sensorService.findByRoom(room)
            if resultDict is not None and len(resultDict) > 0:
                allParams.get('data').append(resultDict[0])

        return allParams

    def getAllRooms(self):
        return self.find().get('rooms')

