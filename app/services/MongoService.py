#!/usr/bin/python3
from pymongo import MongoClient

from app.utils.Constants import Constants


class MongoService(object):
    __instance = None

    @staticmethod
    def getInstance():
        if MongoService.__instance is None:
            MongoService()
        return MongoService.__instance

    def getDb(self):
        client = MongoClient(Constants.getInstance().mongoUrl)
        return client[Constants.dbName]

    def __init__(self):
        if MongoService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MongoService.__instance = self
