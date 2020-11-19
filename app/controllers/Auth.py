from flask_restplus import Resource
from flask import request
from app.services.AuthService import AuthService
import json
from bson import json_util

authService = AuthService()

class Auth(Resource):

    # Logout
    def get(self):
        filters = request.args
        user = filters.get('username')
        authService.logout(user)

    # Login
    def post(self):
        filters = request.args
        user = filters.get('username')
        password = filters.get('password')

        login = authService.auth(user, password)

        if login is not None:
            return json.loads(json_util.dumps(login))
        else:
            return "Not authorized", 401

    # Generate psw
    def put(self):
        filters = request.args
        password = filters.get('password')
        return authService.encrypt_password(password)

