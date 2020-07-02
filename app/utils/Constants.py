#!/usr/bin/python3
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

class Constants(object):
    mongoUrl = os.environ.get('MONGO_URL', None)
    dbName = os.environ.get('MONGO_DB_NAME', None)

    __instance = None

    @staticmethod
    def getInstance():
        if Constants.__instance is None:
            Constants()
        return Constants.__instance

    def __init__(self):
        if Constants.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Constants.__instance = self
