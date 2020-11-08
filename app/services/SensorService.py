#!/usr/bin/python3
from app.services.MongoService import MongoService
from app.utils.JSONEncoder import JSONEncoder
from datetime import datetime

jsonEncoder = JSONEncoder()
db = MongoService.getInstance().getDb()

class SensorService(object):
    def save(self, data):
        now = datetime.now()
        current_date = now.isoformat()
        data['date'] = current_date
        result = db.Detection.insert_one(data)
        return result.acknowledged
