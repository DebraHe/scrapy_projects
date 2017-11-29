# -*- coding: utf-8 -*-
import uuid


def get_uuid(douban_id):
    return str(uuid.uuid3(uuid.UUID('0123456789abcdef0123456789abcdef'), douban_id.encode('utf8')))


def drop_point_in_name(name):
    return name.replace(u'·', '').strip()


if __name__ == '__main__':
    print __file__
