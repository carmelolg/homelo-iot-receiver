#!/usr/bin/python3
from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from datetime import datetime
from bson import json_util
import json

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()


class SensorService(object):
    def save(self, data):
        data['date'] = datetime.now()
        result = db.Detection.insert_one(data)
        return result.acknowledged

    def find(self, filters):

        #Filter management
        mongoFilters = {}

        limit = filters.get('itemsPerPage')
        limit = int(limit) if limit != "0" and int(limit) > 0 else 0

        offset = filters.get('offset')
        offset = int(offset) * limit if offset != "0" and int(offset) > 0 else 0

        room = filters.get('room')
        if room is not None:
            mongoFilters['room'] = room

        startDate = filters.get('startDate')
        if startDate is not None:
            mongoFilters['date'] = {'$gte': startDate}

        endDate = filters.get('endDate')
        if endDate is not None:
            if mongoFilters['date'] is not None:
                mongoFilters['date'].update({'$lte': endDate})
            else:
                mongoFilters['date'] = {'$lte': endDate}

        #Create query
        query = db.Detection.find(mongoFilters, {'_id': False}).sort("_id", -1).skip(offset).limit(int(limit))

        sanitized = json.loads(json_util.dumps(query))
        return sanitized
