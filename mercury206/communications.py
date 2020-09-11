# coding=utf8
"""Communications module"""

import logging
import functools
import time

import serial

from .protocol import pack_msg, unpack_msg
from .utils import pretty_hex


logger = logging.getLogger(__file__)


class CommunicationError(Exception):
    pass


class UnexpectedAddress(CommunicationError):
    pass


def open_serial(
    port='/dev/ttyUSB0', baudrate=9600, parity=serial.PARITY_NONE,
    bytesize=8, stopbits=1, timeout=0.05
):
    port = serial.Serial(
        port=port, baudrate=baudrate, parity=parity,
        bytesize=bytesize, stopbits=stopbits, timeout=timeout)
    return port


def send_command(port, address, command, *params, **kwargs):
    MAX_NUMBER_OF_BYTES = 1000
    message = pack_msg(address, command, *params, crc=kwargs.get('crc', True))
    answer = ''
    while not answer:
        port.write(message)
        logger.debug('T %s', pretty_hex(message))
        time.sleep(0.1)
        answer = port.read(MAX_NUMBER_OF_BYTES)
        logger.debug('R %s', pretty_hex(answer))
    if message + message[:4] == answer[:len(message)+4]:
        logger.debug("E %s", pretty_hex(answer[:len(message)]))
        answer = answer[len(message):]
    received_address, received_data = unpack_msg(answer)
    if received_address != address:
        raise UnexpectedAddress(received_address)
    return received_data


def command_shortcut(port, address):
    return functools.partial(send_command, port, address)
