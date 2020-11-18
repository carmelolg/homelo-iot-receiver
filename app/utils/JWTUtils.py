from app.services.JwtService import JwtService

jwtService = JwtService()


class JWTUtils(object):
    def getUserFromRequest(self, request):
        authorization = request.headers.get('Authorization')
        if authorization is not None:
            auth_splitted = authorization.split()
            if len(auth_splitted) < 2:
                return None
            else:
                _jwt = auth_splitted[1]
                return jwtService.decode(_jwt)['user']
        else:
            return None
