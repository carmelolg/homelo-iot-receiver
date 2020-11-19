#!/usr/bin/python3

import json

from bson import json_util

from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from app.services.AuthService import AuthService

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()
userService = AuthService()


class SensorService(object):
    def update(self, filters, data):
        # Update sensor
        db.Sensor.update_one(filters, data);

        # update user with new home
        result = userService.update(filters['user'], {'house': filters['house']})

        return result.acknowledged

    def find(self, filters):
        query = db.Sensor.find(filters, {'_id': False}).sort("_id", -1).limit(1)

        if query.count() > 0:
            return json.loads(json_util.dumps(query[0]))
        return None
