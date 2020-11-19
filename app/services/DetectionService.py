#!/usr/bin/python3

from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from datetime import datetime
from bson import json_util
import json


jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()


class DetectionService(object):
    def save(self, data):
        data['date'] = datetime.now()
        result = db.Detection.insert_one(data)
        return result.acknowledged

    def find(self, filters):

        #Filter management
        mongoFilters = {}

        limit = filters.get('itemsPerPage')
        limit = int(limit) if limit is not None and limit != "0" and int(limit) > 0 else 0

        offset = filters.get('offset')
        offset = int(offset) * limit if offset is not None and offset != "0" and int(offset) > 0 else 0

        room = filters.get('room')
        if room is not None:
            mongoFilters['room'] = room

        startDate = filters.get('startDate')
        if startDate is not None:
            mongoFilters['date'] = {'$gte': datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S")}

        endDate = filters.get('endDate')
        if endDate is not None:
            if mongoFilters['date'] is not None:
                mongoFilters['date'].update({'$lte': datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")})
            else:
                mongoFilters['date'] = {'$lte': datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")}

        #Create query
        print(mongoFilters)
        query = db.Detection.find(mongoFilters, {'_id': False}).sort("_id", -1).skip(offset).limit(int(limit))

        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def findByRoom(self, room):
        result = db.Detection.find({"room": room}, {'_id': False}).sort("_id", -1)
        return json.loads(json_util.dumps(result))

