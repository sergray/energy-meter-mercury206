# coding=utf8
"Console scripts entries"
from __future__ import print_function

import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

import config
from communications import open_serial
from commands import display_readings, instant_vcp



def sample_config():
    "Create sample INI file"
    config.create_sample_config()
    return 0


def display_readings():
    "Display meter readings"
    settings = config.get_settings()
    port = open_serial(settings['device'])
    readings = display_readings(port, settings['address'])
    print("{} kWh;{} kWh;{} kWh".format(*readings))
    return 0


def instant_vcp():
    "Display instant voltage, current and power consumption"
    settings = config.get_settings()
    port = open_serial(settings['device'])
    voltage, current, power = instant_vcp(port, settings['address'])
    print("{0} V;{1} A;{2} kW".format(voltage, current, power))
    return 0
