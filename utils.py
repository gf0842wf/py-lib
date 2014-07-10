# -*- coding: utf-8 -*-
from twisted.python import log, logfile

import sys
import time
import traceback
import types
import math


def merge_settings(orig, new):
    for name in dir(new):
        if name.upper() == name:
            setattr(orig, name, getattr(new, name))

def dump_settings(settings):
    print "settings {"
    for name in sorted(dir(settings)):
        if name.upper() == name:
            print "  %s = %r" % (name, getattr(settings, name))
    print "}"

class LogMixin(object):
    """需要在启动文件(loop循环文件)配置如下
    f = logfile.DailyLogFile("xx.log","var/log/")
    log.FileLogObserver.timeFormat = '%Y-%m-%d %H:%M:%S'
    log.startLogging(f)
    """
    def msg(self, *args, **kwargs):
        kwargs.setdefault("system", self)
        log.msg(*args, **kwargs)

    def err(self, *args, **kwargs):
        kwargs.setdefault("system", self)
        log.err(*args, **kwargs)

def strdump(s, n_hex=8, n_repr=12):
    """显示字符（十六进制 | repr）
    """
    if not s:
        return ""
    l = ["%02x" % c for c in bytearray(s[:n_hex])]
    l.extend(["|", repr(s[:n_repr])])
    return " ".join(l)

def exc_info():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = ["{}: {}\n".format(exc_type, exc_value)]
    lines.extend(traceback.format_tb(exc_traceback))
    return "".join(lines)

def cutit(s, max_length=80):
    if not isinstance(s, basestring):
        s = str(s)
    if max_length and len(s) > max_length:
        return s[:max_length] + ".(%d)." % (len(s) - max_length)
    return s

def asbool(s):
    if isinstance(s, types.StringTypes):
        return s.lower() in ("yes", "y", "true", "t", "1")
    return bool(s)

def asint(s, base=10):
    try:
        return int(s, base)
    except:
        return 0

def strtime(t=None):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

def dolog(*args):
    """适用于小项目的log输出,否则用LogMixin
    """
    filename = "xx.log"
    f = open(filename, 'a')
    
    print >>f, strtime(), level, ' '.join(map(str, args))
    f.close()
    sys.stdout.flush()

def get_angle_by_lnglat(lng1, lat1, lng2, lat2):
    """
    @param (lng1, lat1): 原点
    @param (lng2, lat2): 另一点
    @return: angle:北为0,顺时针一次到360.
    """
    GPS_ACCURACY = 0.0001 # 定义的精确度
    if abs(lng2 - lng1) < GPS_ACCURACY: # 在同一经度, 南/北
        if lat2 - lat1 > 0:
            angle = 0
        elif lat2 - lat1 < 0:
            angle = 180
    else:
        slope = (lat2 - lat1) / (lng2 - lng1)
        beta = math.atan(slope) * 180 / 3.14 # 弧度转化为角度
        if lat2 - lat1 >= -0.00001:
            if beta <= 90:
                angle = 90 - beta
            elif beta > 90:
                angle = 360 - (beta - 90)
        elif lat2 - lat1 < 0:
            if beta <= 90:
                angle = 180 + (90 - beta)
            elif beta > 90:
                angle = 90 + (180 - beta)

    return angle

def get_direction_by_angle(angel):
    """
    @param angel: 根据上面一个函数的方向角
    @return: 方位(八方位)
    """
    if (337.5 <= angel <= 360) or (360 <= angel < 22.5):
        direction = "n"
    elif 22.5 <= angel < 67.5:
        direction = "en"
    elif 67.5 <= angel < 112.5:
        direction = "e"
    elif 112.5 <= angel < 157.5:
        direction = "es"
    elif 157.5 <= angel < 202.5:
        direction = "s"
    elif 202.5 <= angel < 247.5:
        direction = "ws"
    elif 247.5 <= angel < 292.5:
        direction = "w"
    elif 292.5 <= angel < 337.5:
        direction = "wn"
    
    return direction

def get_distance_by_lnglat(lng1, lat1, lng2, lat2):
    """
    @param (lng1, lat1, lng2, lat2): 分别是两个经纬度坐标
    @return: 两点之间的距离 m
    """
    def _rad(d):
        return d * 3.1415926 / 180
    EARTH_RADIUS = 6378.137 # 地球半径
    if lat1 > lng1:
        lng1, lat1 = lat1, lng1
    if lat2 > lng2:
        lng2, lat2 = lat2, lng2
        
    radLat1 = _rad(lat1)
    radLat2 = _rad(lat2)
    a = radLat1 - radLat2
    b = _rad(lng1) - _rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2)\
                                + math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2),2)))

    s = s * EARTH_RADIUS
    s = round(s * 10000) / 10000

    return s*1000 # m


# -------------- 编码相关------------

def to_unicode(s):
    if isinstance(s, unicode):
        return s
    else:
        # 尝试utf-8
        try:
            return s.decode("utf-8")
        except UnicodeDecodeError:
            pass
        # 尝试gbk
        try:
            return s.decode("gbk")
        except UnicodeDecodeError:
            pass
        # 其他编码
        print "Err: not a utf-8 or gbk string"
        assert(1 == 0)

def to_utf8(s):
    uni_s = to_unicode(s)
    return uni_s.encode("utf-8")

def to_gbk(s):
    uni_s = to_unicode(s)
    return uni_s.encode("gbk")
            
    

def IDGenerator():
    i = 0
    wall = 1 << 31
    while True:
        i += 1
        if i > wall:
            i = 1
        yield i
