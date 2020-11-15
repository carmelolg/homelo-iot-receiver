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
