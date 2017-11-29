# -*- coding: utf-8 -*-
import codecs
big_dict = {}
small_dict = {}
with codecs.open('done.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        big_dict[line.strip()] = 1
with codecs.open('notyet.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        small_dict[line.strip()] = 1
print len(big_dict)
print len(small_dict)
for k in small_dict:
    if k not in big_dict:
        print k
