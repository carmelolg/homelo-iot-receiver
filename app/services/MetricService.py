#!/usr/bin/python3
from datetime import datetime, timedelta

from app.services.HomeService import HomeService
from app.services.DetectionService import DetectionService

homeService = HomeService()
detectionService = DetectionService()

class MetricService(object):

    metric = ''

    def findLast24HData(self, metric, code):

        # Set current metric
        self.metric = metric

        # Get all rooms
        rooms = homeService.getAllRooms(code)

        # Prepare response json
        all = {}

        # Prepare filters
        now = datetime.now()
        yesterday = now - timedelta(hours=24)
        filters = {"startDate": yesterday}

        # For each room get data of last 24h
        for room in rooms:
            filters['room'] = room
            filters['house'] = code
            resultDict = detectionService.find(filters, [("_id", 1)])
            if resultDict is not None and len(resultDict) > 0:
                result = list(map(self.innermap, resultDict))
                all[room] = result

        return all

    def innermap(self, object):
        dict = {}
        dict['value'] = object.get(self.metric) if object.get(self.metric) is not None else 0
        dict['date'] = object.get('date')
        return dict
