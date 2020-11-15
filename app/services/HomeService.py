#!/usr/bin/python3
import json

from bson import json_util

from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()


class HomeService(object):

    def find(self):

        #Create query
        query = db.Home.find({}, {'_id': False}).sort("_id", -1)

        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def getAllParams(self):
        # Create query for retrieve all house rooms
        homeQuery = db.Home.find({}, {'_id': False}).sort("_id", -1).limit(1)[0]
        homeDict = json.loads(json_util.dumps(homeQuery))

        rooms = homeDict.get('rooms')
        allParams = {"data": []}

        # For each room get the last sensor data and put on response
        for room in rooms:
            result = db.Detection.find({"room": room}, {'_id': False}).sort("_id", -1)
            resultDict = json.loads(json_util.dumps(result))
            if resultDict is not None and len(resultDict) > 0:
                allParams.get('data').append(resultDict[0])

        return allParams

