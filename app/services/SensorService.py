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
        now = datetime.now()
        #current_date = now.isoformat()
        data['date'] = now
        result = db.Detection.insert_one(data)
        return result.acknowledged

    def find(self, filters):

        #Filter management
        limit = filters.get('itemsPerPage')
        limit = limit if limit != "0" and limit > 0 else 0

        startDate = filters.get('startDate')
        endDate = filters.get('endDate')

        #Create query
        query = db.Detection.find({}, {'_id': False}).sort("_id", -1).limit(int(limit))

        sanitized = json.loads(json_util.dumps(query))
        return sanitized
