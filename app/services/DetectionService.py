#!/usr/bin/python3
import pytz

from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from datetime import datetime
from bson import json_util
import dateutil.parser
import json

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()


class DetectionService(object):
    def save(self, data):
        data['date'] = datetime.now(pytz.timezone("Europe/Rome"))
        result = db.Detection.insert_one(data)
        return result.acknowledged

    def find(self, filters, optionalSort=[("_id", -1)]):

        # Filter management
        mongoFilters = {}

        limit = filters.get('itemsPerPage')
        limit = int(limit) if limit is not None and limit != "0" and int(limit) > 0 else 0

        offset = filters.get('offset')
        offset = int(offset) * limit if offset is not None and offset != "0" and int(offset) > 0 else 0

        room = filters.get('room')
        if room is not None:
            mongoFilters['room'] = room

        mongoFilters['date'] = {'$gte': dateutil.parser.parse('01-01-1970')}
        startDate = filters.get('startDate')
        if startDate is not None:
            startDate = startDate if isinstance(startDate, datetime) else dateutil.parser.parse(startDate)
            mongoFilters['date'] = {'$gte': startDate}

        endDate = filters.get('endDate')
        if endDate is not None:
            if mongoFilters['date'] is not None:
                endDate = endDate if isinstance(endDate, datetime) else dateutil.parser.parse(endDate)
                mongoFilters['date'].update({'$lte': endDate})
            else:
                endDate = endDate if isinstance(endDate, datetime) else dateutil.parser.parse(endDate)
                mongoFilters['date'] = {'$lte': endDate}

        # Create query
        query = db.Detection.find(mongoFilters, {'_id': False}).sort(optionalSort).skip(offset).limit(int(limit))

        result = dict()
        result['data'] = json.loads(json_util.dumps(query))
        result['page'] = offset
        result['total'] = db.Detection.count(mongoFilters)

        # sanitized = json.loads(json_util.dumps(query))
        return result

    def findByRoom(self, room):
        result = db.Detection.find({"room": room}, {'_id': False}).sort("_id", -1)
        return json.loads(json_util.dumps(result))
