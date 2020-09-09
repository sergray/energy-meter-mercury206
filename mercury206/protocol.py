# coding=utf8

from struct import pack, unpack

from minimalmodbus import _calculate_crc_string as modbus_crc


ADDRESS_FMT = '!I'  # unsigned integer in network order


def pack_msg(address, *args, **kwargs):
    r"""Pack power meter address and args into string,
    add modbus CRC by default

    Keyword Arguments:
    - crc: optional bool, True by default, controls addition of CRC

    Return string with bytes

    >>> from .utils import pretty_hex
    >>> pretty_hex(pack_msg(10925856, 0x28))
    '00 A6 B7 20 28 AF 70'
    >>> pretty_hex(pack_msg(10925856, 0x28, crc=False))
    '00 A6 B7 20 28'
    >>> pretty_hex(pack_msg(10925856, 0x2b))
    '00 A6 B7 20 2B EF 71'
    """
    if isinstance(address, int):
        address = pack(ADDRESS_FMT, address)
    else:
        pad_len = len(address) % 4
        address = '\x00' * pad_len + address
    params = list(args)
    for idx, arg in enumerate(params):
        if isinstance(arg, int):
            params[idx] = pack('B', arg)
    msg = address + ''.join(params)
    if kwargs.get('crc', True):
        msg += modbus_crc(msg)
    return msg


def unpack_msg(message):
    r"""Unpack message string.
    Assume the first 4 bytes carry power meter address

    Return tuple with: integer power meter address and list of bytes

    >>> unpack_msg('\x00\xA6\xB7\x20\x28')
    (10925856, [40])
    >>> unpack_msg('\x00\xA6\xB7\x20\x27\x00\x26\x56\x16\x00\x13\x70\x91\x00\x00\x00\x00\x00\x00\x00\x00\x47\x78')
    (10925856, [39, 0, 38, 86, 22, 0, 19, 112, 145, 0, 0, 0, 0, 0, 0, 0, 0, 71, 120])
    >>> unpack_msg('\x00\xA6\xB7\x20')
    (10925856, [])
    """
    address = unpack(ADDRESS_FMT, message[:4])[0]
    data = [unpack('B', c)[0] for c in message[4:]]
    return address, data
