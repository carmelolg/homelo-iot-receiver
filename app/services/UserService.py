import json

from bson import json_util

from app.services.MongoService import MongoService
from app.services.AuthService import AuthService

db = MongoService.getInstance().getDb()
authService = AuthService()

class UserService(object):

    def findAll(self):
        query = db.User.find({}, {'_id': False, 'password': False, 'token': False}).sort("_id", -1)
        sanitized = json.loads(json_util.dumps(query))
        return sanitized

    def save(self, user):

        if 'password' not in user:
            return None

        psw = authService.encrypt_password(user['password'])
        user['password'] = psw

        result = db.User.insert_one(user)
        return result.acknowledged

    def delete(self, filters):
        result = db.User.delete_many(filters)
        return result.acknowledged
