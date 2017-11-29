# -*- coding: utf-8 -*-
import uuid


def unicode_to_str(s, encoding='utf8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    else:
        return s


def get_uuid(id_type, id_name):
    return str(uuid.uuid3(uuid.UUID('0123456789abcdef0123456789abcdef'), id_type + id_name.encode('utf8')))


if __name__ == '__main__':
    print __file__
