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
        return jwtService.delete(user)

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

                loggedUserDict = {}
                loggedUserDict['jwt'] = _jwt
                loggedUserDict['status'] = 'ok'

                # Return response
                return loggedUserDict
            else:
                return None
        else:
            return None

    def _auth(self, userInfo, password):
        return self.check_encrypted_password(password, userInfo['password'])

    def encrypt_password(self, password):
        return pwd_context.encrypt(password)

    def check_encrypted_password(self, password, hashed):
        return pwd_context.verify(password, hashed)
