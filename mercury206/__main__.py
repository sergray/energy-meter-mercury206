# coding=utf8
"""Вывод текущих показаний счетчика"""
from __future__ import print_function

from config import settings
from communications import open_serial
from commands import display_readings


port = open_serial(settings['device'])
readings = display_readings(port, settings['address'])

for reading in readings:
    print("{} кВт*ч".format(reading))
