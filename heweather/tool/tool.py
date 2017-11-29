# -*- coding: utf-8 -*-
import os
import datetime


def unicode_to_str(s, encoding='utf8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    else:
        return s


def get_the_file(filename):
    return os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/" + filename


def clean_datas(data):
    dic = data.values()[0][0]
    try:
        del dic['status']
        del dic['basic']
        del dic['suggestion']
        del dic['hourly_forecast']
        del dic['now']
        for i in dic[u'daily_forecast']:
            del i[u'vis']
            del i[u'pop']
            del i[u'astro']
            del i[u'pres']
    except:
        pass
    return dic


def get_date():
    begin = datetime.date(2017, 9, 14)
    end = datetime.date(2017, 9, 21)
    return [str(begin + datetime.timedelta(days=i)) for i in range((end - begin).days+1)]


if __name__ == '__main__':
    get_date()
    print __file__
