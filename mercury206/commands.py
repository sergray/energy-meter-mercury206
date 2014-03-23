# coding=utf8
from communications import send_command, command_shortcut
from utils import digitize

__all__ = ['connect', 'display_readings', 'instant_vcp']


def connect(port, address):
    "Первые две команды установления соединения"
    command = command_shortcut(port, address)
    _ = command(0x28)
    _ = command(0x2F, crc=False)


def display_readings(port, address, cmd=0x27):
    """Возвращает список показаний потреблённой энергии в кВт/ч по 3 тарифам
    с момента последнего сброса"""
    data = send_command(port, address, cmd)
    return [digitize(data[idx:idx+4]) / 100.0 for idx in range(1, 13, 4)]


def instant_vcp(port, address, cmd=0x63):
    """Возвращает список с текущими показаниями напряжения (В),
    тока (А), потребляемой мощности (кВт/ч)"""
    data = send_command(port, address, cmd)
    voltage = digitize(data[1:3]) / 10.
    current = digitize(data[3:5]) / 100.
    power = digitize(data[5:8]) / 1000.
    return [voltage, current, power]
