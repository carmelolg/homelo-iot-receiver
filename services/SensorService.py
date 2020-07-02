#!/usr/bin/python3
from services.MongoService import MongoService
from utils.JSONEncoder import JSONEncoder

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()


class SensorService(object):
    def save(self, json):
        result = db.Detection.insert_one(json)
        return result.acknowledged
