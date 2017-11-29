# -*- coding:utf-8 -*-
'''
正式的代码：解析schema为csv文件
'''
import codecs
import csv
import json

import os
import uuid

_csv = {}  # 通过type字段得到的csv文件名 以及  通过没有type字段得到的该dict的字段名
_header = {}  # 存放每一个csv文件的表头
_content = {}   # 存放每一个csv文件的内容
_final_content = {}  # 去重过后的csv内容

# 初始化关系表
rel_csv_f = 'relationship.csv'
_content[rel_csv_f] = []
_final_content[rel_csv_f] = []
_header[rel_csv_f] = {
    'subject:START_ID': 1,
    'value:END_ID': 1,
    'property:TYPE': 1,
    'label': 1,
}


def get_csv_name(dict_test, type_k='@type', field='all_json'):
    """
    获取csv文件名
    :param dict_test: 传入一个数据类型，测试是否为dict
    :param type_k: 想要查找的字段，此处为@type
    :param field: 该数据的上一级字段名称
    :return: 无
    """
    if isinstance(dict_test, dict):
        if type_k not in dict_test:
            if not _csv.get(field):
                _csv[field] = []
            if field not in _csv.get(field):
                _csv[field].append(field)
            get_initial_header_and_content(dict_test, field)
        for k, v in dict_test.items():
            if k != type_k:
                get_csv_name(v, type_k, k)
            else:
                if v[0]:
                    if not _csv.get(v[0]):
                        _csv[v[0]] = []
                    if field not in _csv.get(v[0]):
                        _csv[v[0]].append(field)
                    get_initial_header_and_content(dict_test, v[0])
    elif isinstance(dict_test, list):
        for item in dict_test:
            get_csv_name(item, type_k, field)


def get_initial_header_and_content(dict_test, type_k):
    """
    初始化csv表的表头和内容
    :param dict_test: 传入一个dict
    :param type_k: csv名字
    :return: 无
    """
    csv_f = '{}.csv'.format(type_k.encode('utf8'))
    if csv_f not in _header:
        _header[csv_f] = {
            'kgid:ID': 1,
            ':LABEL': 1,
        }
        _content[csv_f] = []
        _final_content[csv_f] = []
    for k in dict_test:
        if k != u'@id' and k != u'@type':
            _header[csv_f][k.encode('utf8')] = 1


def get_field_value(dict_test, type_k):
    def get_field_value_in(dict_test_in, type_k_in, default):
        """
        获取嵌套字典中某一字段的值
        :param dict_test: 传入一个dict
        :param type_k: 想要查找的字段
        :param default: 查找不到默认输出的值
        :return:该字段对应的值
        """
        if isinstance(dict_test_in, dict):
            for k, v in dict_test_in.items():
                if k == type_k_in:
                    yield v
                elif isinstance(v, dict):
                    ret = get_field_value_in(v, type_k_in, default)
                    if ret is not default:
                        yield ret
                elif isinstance(v, list):
                    for item in v:
                        ret = get_field_value_in(item, type_k_in, default)
                        if ret is not default:
                            yield ret
        yield default

    result_list = []
    results = get_field_value_in(dict_test, type_k, (x for x in range(0, 1)))
    for result in results:
        if isinstance(result, dict) or isinstance(result, list):
            result_list.append(result)
        try:
            result_gen = result.next()
            if isinstance(result_gen, dict) or isinstance(result_gen, list):
                result_list.append(result_gen)
        except:
            continue
    return result_list


def get_id(dict_test):
    """
    获取独一无二的ID
    :param dict_test: 一个值
    :return: 根据值获取的唯一ID
    """
    value = str(uuid.uuid3(uuid.UUID('0123456789abcdef0123456789abcdef'), str(dict_test)))
    return value


def get_str_content(field_value, field):
    """
    获取符合schema标准的值
    :param field_value: 一个dict
    :param field: 获取dict值的字段
    :return:
    """
    try:
        value = field_value.get(field, u'')
        if isinstance(value, list) and value and type(value[0]) != dict:
            value = u';'.join(value)
        elif isinstance(value, int) or isinstance(value, float):
            value = str(value).encode('utf-8')
        value = value.encode('utf8')
    except:
        value = ''
    return value


def get_each_content(dict_test, csv_f, _csv_field, add_rel=1, _id='', label='', not_turn = 1):
    """
    填充每一条数据
    :param dict_test: 传入一个dict
    :param csv_f: csv文件名
    :param _csv_field:csv字段名
    :param add_ref: 是否添加进rel文件
    :param _id: 本条json的ID
    :param label: 标签
    :param not_turn: 是否反转rel
    :return:
    """
    content_l = []
    for field in _header.get(csv_f).keys():
        if field == 'kgid:ID':
            field = '@id'
        elif field == ':LABEL':
            field = '@type'

        field = field.decode('utf8')
        value = get_str_content(dict_test, field)

        if field == '@id' and not value:
            value = get_id(dict_test)
        elif field == '@type' and not value:
            value = _csv_field + ';Thing'
        content_l.append(value)
        if add_rel == 1:
            if field == '@id':
                if not_turn:
                    _content[rel_csv_f].append([_id, _csv_field, value, label])
                else:
                    _content[rel_csv_f].append([value, _csv_field, _id, label])
    _content[csv_f].append(content_l)


def get_content(dict_test):
    """
    得到csv内容
    :param dict_test: 传入的json
    :return:
    """
    global _id
    _id = dict_test.get('@id')
    for _csv_name, _csv_fields in _csv.items():
        csv_f = '{}.csv'.format(_csv_name.encode('utf8'))
        for _csv_field in _csv_fields:
            if _csv_field == 'all_json':
                get_each_content(dict_test, csv_f, _csv_field, add_rel=0)
            else:
                field_values = get_field_value(dict_test, _csv_field)
                for field_value in field_values:
                    if isinstance(field_value, list):
                        for item in field_value:
                            get_each_content(item, csv_f, _csv_field, _id=_id)
                    elif isinstance(field_value, dict):
                        get_each_content(field_value, csv_f, _csv_field, _id=_id)


def duplicate_removal():
    """
    对_content进行去重操作，去重后的结果存入_final_content
    :return:
    """
    _final_content[rel_csv_f] = [list(t) for t in set([tuple(d) for d in _content.get(rel_csv_f)])]
    for csv_name, content in _content.items():
        try:
            _id_index = _header[csv_name].keys().index('kgid:ID')
            result_dict = {}
            for item in content:
                if item[_id_index] not in result_dict:
                    result_dict[item[_id_index]] = []
                result_dict[item[_id_index]].append(item)
            for _id, final in result_dict.items():
                if len(final) == 1:
                   _final_content[csv_name].append(final[0])
                else:
                    str_len_list = [len(str(index)) for index in final]
                    _final_content[csv_name].append(final[str_len_list.index(max(str_len_list))])
        except:
            continue


def write2csv(csv_dir):
    """
    写入csv
    :param csv_dir: csv路径
    :return:
    """
    for file in _header.keys():
        with codecs.open(os.path.join(csv_dir, file), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(_header.get(file).keys())
            writer.writerows(_final_content.get(file))


def need_special_operation(dict_test, _id, fields=[], operation=0):
    """
    需要特殊处理的操作
    :param dict_test: 传入一个dict
    :param _id: json的ID
    :param fields: 不规则字段列表
    :param operation: 进行何种操作
    :return:
    """
    if operation == 0:
        for field in fields:
            del dict_test[field]
        return dict_test
    else:
        for field in fields:
            if field == 'character':
                csv_f = '{}.csv'.format(field.encode('utf8'))
                field_values = get_field_value(dict_test, field)
                _csv[field] = [field]
                try:
                    temp_dict = field_values[0][0].copy()
                    del temp_dict['actor']
                    get_initial_header_and_content(temp_dict, field)

                    for field_value in field_values:
                        if isinstance(field_value, list):
                            for item in field_value:
                                get_each_content(item, csv_f, field, _id=item.get('actor').get('@id'), not_turn=0)
                                get_each_content(item.get('actor'), 'Person.csv', 'actor', _id=_id)
                except:
                    continue
            if field == 'award':
                csv_name = 'Award'
                csv_f = '{}.csv'.format(csv_name)
                field_values = get_field_value(dict_test, field)
                _csv[csv_name] = [field]
                try:
                    temp_dict = field_values[0][0].copy()
                    get_initial_header_and_content(temp_dict, csv_name)

                    for field_value in field_values:
                        if isinstance(field_value, list):
                            for item in field_value:
                                get_each_content(item, csv_f, field, _id=_id)
                                for winner in item.get('winners'):
                                    get_each_content(winner, 'Person.csv', 'Person', add_rel=0)
                                    _content[rel_csv_f].append([item.get('@id'), 'winners', winner.get('@id'), item.get('label')])
                except:
                    continue

# kg_movie_collection


if __name__ == '__main__':
    filename = 'doc/kg_movie_collection.json'
    # 不规则字段列表
    irregular_fields = ['character', 'award']

    print "get_csv_ing"
    # 得到csv文件及表头
    with open(filename) as f:
        for _ in f.readlines():
            d = json.loads(_.strip())
            get_csv_name(need_special_operation(d, d.get('@id'), irregular_fields, operation=0))

    print "fill_regular_content"
    # 填充规则的csv文件及表头
    with open(filename) as f:
        for _ in f.readlines():
            d = json.loads(_.strip())
            get_content(need_special_operation(d, d.get('@id'), irregular_fields, operation=0))

    print "fill_irregular_content"
    # 填充不规则的csv文件及表头
    with open(filename) as f:
        for _ in f.readlines():
            d = json.loads(_.strip())
            need_special_operation(d, d.get('@id'), irregular_fields, operation=1)

    print "duplicate_removal"
    duplicate_removal()

    if not os.path.exists('csv'):
        os.mkdir('csv')
    print "write2csv"
    write2csv('csv')