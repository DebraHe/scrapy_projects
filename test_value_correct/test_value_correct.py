# -*- coding:utf-8 -*-
import mysql.connector as MySQLdb


def conn_mysql():
    conn = MySQLdb.connect(
        host='127.0.0.1', user='root', passwd='123456',
        db='hyao', port=3306, charset='utf8')
    return conn


def get_values():
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select DISTINCT series_id from result_stata"
    cursor.execute(sql)
    series_id_prices_dict = {}
    for row in cursor.fetchall():
        series_id = row[0]
        series_id_prices_dict[series_id] = []
        sql_in = "select price from result_stata where series_id='{}'".format(series_id.encode('utf-8'))
        cursor.execute(sql_in)
        for price_row in cursor.fetchall():
            series_id_prices_dict[series_id].append(price_row[0])
    return series_id_prices_dict


series_id_prices_dict = get_values()
for series_id, price_list in series_id_prices_dict.items():
    price_list = [float(item) for item in price_list]
    max_value = max(price_list)
    min_value = min(price_list)
    range_value = max_value - min_value  # 极差
    range_percent = max_value/min_value
    print range_value, range_percent