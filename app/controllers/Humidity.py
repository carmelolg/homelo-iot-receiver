from flask_restplus import Resource

from app.services.MetricService import MetricService

metricService = MetricService()

class Humidity(Resource):

    def get(self):
        return metricService.findLast24HData('humidity')