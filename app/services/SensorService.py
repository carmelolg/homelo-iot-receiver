#!/usr/bin/python3

import json

from bson import json_util

from app.services.AuthService import AuthService
from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()
userService = AuthService()


class SensorService(object):
    def update(self, filters, data):
        # Update sensor
        result = db.Sensor.update_one(filters, {'$set': data}, True)

        ack = True
        if 'house' in filters:
            # update user with new home
            ack = userService.update(filters['name'], {'house': filters['house']})

        if ack:
            return result.acknowledged

        return False

    def find(self, filters):
        query = db.Sensor.find(filters, {'_id': False}).sort("_id", -1)

        if query.count() > 0:
            return json.loads(json_util.dumps(query))
        return None
