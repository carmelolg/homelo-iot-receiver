import json
import uuid
import datetime

import jwt
from bson import json_util

from app.services.MongoService import MongoService

db = MongoService.getInstance().getDb()


class JwtService(object):

    def save(self, info):
        result = db.Token.insert_one(info)
        return result.acknowledged

    def delete(self, user):
        result = db.Token.delete_many({'user': user})
        return result.acknowledged

    def check(self, jwt):
        jwtQry = db.Token.find({'jwt': jwt}, {'_id': False}).limit(1)
        jwtDict = json.loads(json_util.dumps(jwtQry))
        if jwtDict is not None and len(jwtDict) > 0:
            return True
        else:
            return False

    def generate(self, user):
        _jwt = jwt.encode({'user': user}, str(uuid.uuid4()), algorithm='HS256').decode('utf-8')
        jwtDict = {}
        jwtDict['jwt'] = _jwt
        jwtDict['isHuman'] = True
        jwtDict['user'] = user
        now = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
        jwtDict['createdAt'] = now
        # Save new JWT
        self.save(jwtDict)
        return _jwt