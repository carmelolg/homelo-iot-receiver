from flask import request
from flask_restplus import Resource

from app.services.UserService import UserService

userService = UserService()


class User(Resource):

    # Find all
    def get(self):
        return userService.findAll()

    # Save new user
    def post(self):
        user = request.get_json()
        saved = userService.save(user)
        if saved is not None:
            return "ok", 200
        else:
            return "ko", 500

    # Delete a use
    def delete(self):
        filters = request.args.to_dict()
        return userService.delete(filters)
