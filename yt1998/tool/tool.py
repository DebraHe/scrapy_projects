# -*- coding: utf-8 -
import datetime


def get_today():
    today = datetime.date.today()
    ISOFOMAT = "%Y-%m-%d"
    return today.strftime(ISOFOMAT)
