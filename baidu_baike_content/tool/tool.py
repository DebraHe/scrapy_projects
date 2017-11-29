# -*- coding: utf-8 -*-


def unicode_to_str(s, encoding='utf8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    else:
        return s

if __name__ == '__main__':
    print __file__
