# -*- coding:utf-8 -*-

'''
把所有具有相同文件名的文件融合成一个文件
例:
ret1/1.json
ret2/1.json
融合成一个1.json
'''

import os


def merge_files_with_same_name(ret_dir, merged_dir):
    hosts = [
        'ubuntu@106.75.92.218',
        'ubuntu@106.75.97.244',
        'ubuntu@106.75.97.154',
        'ubuntu@106.75.98.168',
        'ubuntu@106.75.104.214',
        'ubuntu@106.75.97.184',
        'ubuntu@106.75.98.24',
        'ubuntu@106.75.97.198',
        'ubuntu@106.75.97.190',
        'ubuntu@106.75.104.181',

    ]

    result = {}
    for h in hosts:
        filename = ret_dir + h + '-result'
        for item in os.walk(filename):
            if item[2]:
                for file in item[2]:
                    # os.path.join(item[0], file)
                    if file not in result:
                        result[file] = [os.path.join(item[0], file)]
                    else:
                        result[file].append(os.path.join(item[0], file))
            if item[1]:
                for file in item[1]:
                    # shixin = os.path.join(os.path.join(item[0], file), 'shixin.json')
                    # zhixing = os.path.join(os.path.join(item[0], file), 'zhixing.json')
                    wenshu = os.path.join(os.path.join(item[0], file), 'wenshu_detail.json')
                    # if 'shixin.json' not in result:
                    #     result['shixin.json'] = [shixin]
                    # else:
                    #     result['shixin.json'].append(shixin)
                    # if 'zhixing.json' not in result:
                    #     result['zhixing.json'] = [zhixing]
                    # else:
                    #     result['zhixing.json'].append(zhixing)
                    if 'wenshu_detail.json' not in result:
                        result['wenshu_detail.json'] = [wenshu]
                    else:
                        result['wenshu_detail.json'].append(wenshu)
    for k, v in result.items():
        s = ''
        for _ in v:
            try:
                with open(_) as f:
                    s = s + f.read()
            except:
                print _
        l = s.strip().split('\n')
        s = '\n'.join(list(set(l)))
        filename_result = '{}/{}'.format(merged_dir, k)
        with open(filename_result, 'w') as f:
            f.write(s)


if __name__ == '__main__':

        ret_dir = '/Users/debrahe/Desktop/result/'
        merged_dir = '/Users/debrahe/Desktop/all_data/'
        merge_files_with_same_name(ret_dir, merged_dir)
