# -*- coding: utf-8 -*-
import urllib2


def unicode_to_str(s, encoding='utf8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    else:
        return s


def drop_bom(s):
    # drop BOM header
    drop_bom_str = urllib2.quote(s.strip().encode('utf-8'))
    if drop_bom_str[:9] == '%EF%BB%BF':
        drop_bom_str = drop_bom_str[9:]
    return drop_bom_str


def drop_mark(s):
    s = s.replace('<p>', '').replace('</p>', '').replace('<br>', '\n').replace('<em>', '').replace('</em>', '').replace('<sub>', '').replace('</sub>', '')
    return s


if __name__ == '__main__':
    print __file__
