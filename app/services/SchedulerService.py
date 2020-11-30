#!/usr/bin/python3

import time

import schedule

from app.services.SensorService import SensorService
from app.services.JwtService import JwtService

sensorService = SensorService()
jwtService = JwtService()

class SchedulerService(object):

    def alive(self):
        sensors = sensorService.find({})
        for sensor in sensors:
            isActive = jwtService.isUserActive(sensor['name'])
            print(sensor['name'], isActive)
            filters = {'user': sensor['name']}
            sensorService.update(filters, {'alive': isActive})

        print(sensors)

    def run(self):
        schedule.every(10).seconds.do(self.alive)
        while True:
            schedule.run_pending()
            time.sleep(1)
