# coding=utf8
"Console scripts entries"


import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

from . import config
from .communications import open_serial
from . import commands



def sample_config():
    "Create sample INI file"
    config.create_sample_config()
    return 0


def display_readings():
    "Display meter readings"
    settings = config.get_settings()
    port = open_serial(settings['device'])
    readings = commands.display_readings(port, settings['address'])
    print("{} kWh;{} kWh;{} kWh".format(*readings))
    return 0


def instant_vcp():
    "Display instant voltage, current and power consumption"
    settings = config.get_settings()
    port = open_serial(settings['device'])
    voltage, current, power = commands.instant_vcp(port, settings['address'])
    print("{0} V;{1} A;{2} kW".format(voltage, current, power))
    return 0
