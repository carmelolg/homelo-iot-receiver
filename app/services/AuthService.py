import json
from bson import json_util
from passlib.context import CryptContext

from app.services.JwtService import JwtService
from app.services.MongoService import MongoService

db = MongoService.getInstance().getDb()
jwtService = JwtService()
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


class AuthService(object):

    def logout(self, user):
        filters = {'user': user}
        update = {"$set": {'token': None}}
        # Delete token from user
        db.User.update_one(filters, update)
        # Delete jwt token
        return jwtService.delete(user)

    def update(self, user, data):
        result = db.User.update_one({'user': user}, {'$set': data})
        return result.acknowledged

    def auth(self, user, password):
        # Find user
        userQry = db.User.find({'user': user}, {'_id': False}).limit(1)
        userDict = json.loads(json_util.dumps(userQry))

        if userDict is not None and len(userDict) > 0:
            userFound = userDict[0]
            check = self._auth(userFound, password)
            if check:
                # Delete JWT if present
                jwtService.delete(user)
                # Generate JWT
                _jwt = jwtService.generate(user)

                # Update user
                filters = {'user': user}
                update = {"$set": {'token': _jwt}}
                # Update token for user
                db.User.update_one(filters, update);


                loggedUserDict = {}
                loggedUserDict['jwt'] = _jwt
                loggedUserDict['status'] = 'ok'

                # Return response
                return loggedUserDict
            else:
                return None
        else:
            return None

    def getHouse(self, user):
        filters = {'user': user}

        #Create query
        query = db.User.find(filters, {'_id': False}).sort("_id", -1).limit(1)[0]
        sanitized = json.loads(json_util.dumps(query))
        if(sanitized['house'] is not None and len(sanitized['house']) > 0):
            return sanitized['house']
        else:
            return ""


    def _auth(self, userInfo, password):
        return self.check_encrypted_password(password, userInfo['password'])

    def encrypt_password(self, password):
        return pwd_context.encrypt(password)

    def check_encrypted_password(self, password, hashed):
        return pwd_context.verify(password, hashed)

    def generateToken(self, user):
        return jwtService.generate(user)
