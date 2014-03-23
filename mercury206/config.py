# coding=utf8
"Configuration settings"
from __future__ import print_function
import os
import sys
import logging

import ConfigParser


CONFIG_PATH_ENV = 'MERCURY_CONFIG'
CONFIG_DEVICE_ENV = 'MERCURY_SERIAL_DEVICE'
CONFIG_ADDRESS_ENV = 'MERCURY_ADDRESS'


logger = logging.getLogger(__file__)


try:
    CONFIG_PATH = os.environ[CONFIG_PATH_ENV]
except KeyError:
    CONFIG_PATH = os.path.join(
        os.environ.get('HOME', os.getcwd()), '.mercury206', 'config.ini')


def create_sample_config(path=CONFIG_PATH):
    "Create sample INI file with required parameters and empty values"
    dirpath = os.path.dirname(path)
    if not os.path.isdir(dirpath):
        os.makedirs(dirpath)
    cfg = ConfigParser.ConfigParser()
    for section in ['serial', 'mercury']:
        if not cfg.has_section(section):
            cfg.add_section(section)
    cfg.set('serial', 'device', '')
    cfg.set('mercury', 'address', 0)
    with open(path, 'w') as config_file:
        cfg.write(config_file)


def settings_from_config(path=CONFIG_PATH):
    "Return dictionary with settings from INI file"
    if not os.path.exists(path):
        raise RuntimeError('missing config %r' % path)
    cfg = ConfigParser.ConfigParser()
    cfg.read(path)
    return {
        'device': cfg.get('serial', 'device'),
        'address': cfg.getint('mercury', 'address')
    }


def settings_from_environ():
    "Return dictionary with settings from environment variables"
    return {
        'device': os.environ[CONFIG_DEVICE_ENV],
        'address': int(os.environ[CONFIG_ADDRESS_ENV]),
    }


if __name__ == '__main__':
    create_sample_config()
    logger.info('created %r config', CONFIG_PATH)
    sys.exit(0)


try:
    settings = settings_from_environ()
    logger.debug('env settings %r', settings)
except KeyError:
    try:
        settings = settings_from_config()
        logger.debug('ini %r settings %r', CONFIG_PATH, settings)
    except (RuntimeError, ConfigParser.NoSectionError) as exc:
        logger.debug(repr(exc))
        settings = None
        print("""Ошибка чтения настроек! Необходимо задать \
переменные окружения {} и {},\nили создать файл настроек {}: \
python {}""".format(CONFIG_DEVICE_ENV, CONFIG_ADDRESS_ENV,
            CONFIG_PATH, __file__), file=sys.stderr)
        sys.exit(1)
