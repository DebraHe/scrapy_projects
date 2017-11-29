# -*- coding:utf-8 -*-
import requests
import json
singer_url = 'http://music.163.com/api/song/media?id=' + str(472976637)
web_data = requests.get(singer_url)
lyric_json = json.loads(web_data.content)
lyric = lyric_json['lyric']
print lyric