#  -*- coding: utf-8 -*-

from array import array
from operator import xor, add

def xor8(s):
    return reduce(xor, array('B', s))

def xor16(s):
    return reduce(xor, array('H', s))

def xor32(s):
    return reduce(xor, array('L', s))

def sum8(s):
    return reduce(add, array('B', s)) & 0xff

def sum16(s, bigendian=False):
    a = array('H', s)
    if bigendian:
        a.byteswap()
    return reduce(add, a) & 0xffff

def sum32(s, bigendian=False):
    a = array('L', s)
    if bigendian:
        a.byteswap()
    return reduce(add, a) & 0xffffffff
