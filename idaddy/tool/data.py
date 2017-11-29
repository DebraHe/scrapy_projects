# -*- coding: utf-8 -*-
import re


def clean(text):
    rep = {
        '\\': '\\\\',
        '"': "'",
        '\r': '',
        '\t': '',
        '\n': '',
        '\0': '',
        ' ': ''
    }
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    result = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return result
