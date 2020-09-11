# coding=utf8

from struct import pack, unpack
from typing import Union, Sequence

from minimalmodbus import _calculate_crc_string as modbus_crc


ADDRESS_FMT = '!I'  # unsigned integer in network order


def pack_msg(address: Union[int, bytes], *args: Sequence[int], **kwargs) -> bytes:
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
    >>> pretty_hex(pack_msg(b'123'))
    '00 31 32 33 04 9E'
    >>> pack_msg('123')
    Traceback (most recent call last):
        ...
    TypeError: address must be an integer or bytes
    >>> pack_msg(b'12345')
    Traceback (most recent call last):
        ...
    ValueError: address length exceeds 4 bytes
    """
    if isinstance(address, int):
        address = pack(ADDRESS_FMT, address)
    elif isinstance(address, bytes):
        if len(address) > 4:
            raise ValueError('address length exceeds 4 bytes')
        pad_len = 4 - len(address)
        address = b'\x00' * pad_len + address
    else:
        raise TypeError('address must be an integer or bytes')
    params = bytes(args)
    msg = (address + params).decode('latin1')
    if kwargs.get('crc', True):
        msg += modbus_crc(msg)
    return msg.encode('latin1')


def unpack_msg(message: bytes):
    r"""Unpack message string.
    Assume the first 4 bytes carry power meter address

    Return tuple with: integer power meter address and list of bytes

    >>> unpack_msg(b'\x00\xA6\xB7\x20\x28')
    (10925856, [40])
    >>> unpack_msg(b'\x00\xA6\xB7\x20\x27\x00\x26\x56\x16\x00\x13\x70\x91\x00\x00\x00\x00\x00\x00\x00\x00\x47\x78')
    (10925856, [39, 0, 38, 86, 22, 0, 19, 112, 145, 0, 0, 0, 0, 0, 0, 0, 0, 71, 120])
    >>> unpack_msg(b'\x00\xA6\xB7\x20')
    (10925856, [])
    """
    address = unpack(ADDRESS_FMT, message[:4])[0]
    data = list(message[4:])
    return address, data
