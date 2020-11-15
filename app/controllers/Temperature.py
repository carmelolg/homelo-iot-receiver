from flask_restplus import Resource

from app.services.MetricService import MetricService

metricService = MetricService()


class Temperature(Resource):

    def get(self):
        return metricService.findLast24HData('temperature')
