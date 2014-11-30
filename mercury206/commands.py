# coding=utf8
from communications import send_command, command_shortcut
from utils import digitize, digitized_triple

__all__ = [
    'connect', 'display_readings', 'instant_vcp',
    'monthly_active_energy', 'monthly_reactive_energy',
]


def connect(port, address):
    "Первые две команды установления соединения"
    command = command_shortcut(port, address)
    _ = command(0x28)
    _ = command(0x2F, crc=False)


def display_readings(port, address, cmd=0x27, *args):
    """Возвращает список показаний потреблённой энергии в кВт/ч по 3 тарифам
    с момента последнего сброса"""
    data = send_command(port, address, cmd, *args)
    return digitized_triple(data)


def instant_vcp(port, address, cmd=0x63):
    """Возвращает список с текущими показаниями напряжения (В),
    тока (А), потребляемой мощности (кВт/ч)"""
    data = send_command(port, address, cmd)
    voltage = digitize(data[1:3]) / 10.
    current = digitize(data[3:5]) / 100.
    power = digitize(data[5:8]) / 1000.
    return [voltage, current, power]


def monthly_active_energy(port, address, month):
    """Возвращает список показаний активной энергии в кВт/ч по 3 тарифам
    для заданного месяца

    - month: целое число от 0 до 12"""
    return display_readings(port, address, 0x32, month)


def monthly_reactive_energy(port, address, month):
    """Возвращает список показаний реактивной энергии в кВт/ч по 3 тарифам
    для заданного месяца

    - month: целое число от 0 до 12"""
    return display_readings(port, address, 0x38, month)
