# -*- coding: utf-8 -*-
from langconv import *


def unicode_to_str(s, encoding='utf8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    else:
        return s


def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line


if __name__ == '__main__':
    print __file__
