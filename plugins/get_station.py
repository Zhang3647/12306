import json
import re

import requests
from config.config import GetConfig
from data.databse import DB

url = [
    'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
]


class Station:
    def __init__(self):
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36"
        }

        self.version = GetConfig.get_station_version()
        # self.version = '1.9302'

    def synchronization(self):
        response = requests.get(url[0], headers=self.headers, params={
            "station_version": self.version
        })
        return response.text

    def extract(self):
        response = self.synchronization()
        response = response.replace("var station_names ='", '')
        return response[:-2]

    def process(self):
        response = self.extract()
        response = re.findall(r'@(.*?)\|\|\|', response)
        print('共有{}个车站'.format(len(response)))
        response = [i.split("|") for i in response]
        # 保存处理好的信息
        # self.save_station(response)
        self.create_station_dict(json.dumps(response))
        return response

    @staticmethod
    def save_station(response):
        with open('resource/station.txt', 'wt', encoding='utf-8') as f:
            f.write(json.dumps(response).encode('utf8').decode('unicode_escape'))

    @staticmethod
    def create_station_dict(response):
        station_info = json.loads(response)
        station_dict = {}
        db = DB(f'{GetConfig().get_project_path()}\\data\\station_code.db')
        db.delete("delete from station", ())
        # db = DB(f'..\\data\\station_code.db')
        for item in station_info:
            # station_dict[item[1]] = item[2]
            db.insert('insert into station(station_name, station_code, city) values(?, ?, ?)',
                      (item[1], item[2], item[-1]))
        # with open('resource/station_dict.txt', 'wt', encoding='utf-8') as f:
        #     f.write(json.dumps(station_dict).encode('utf8').decode('unicode_escape'))
        return {"code": 200, "msg": "success"}

    @staticmethod
    def check_station_code(keyword, _type='station'):
        db = DB(f'{GetConfig().get_project_path()}\\data\\station_code.db')
        if _type == 'station':
            response = db.select('select * from station where station_name like ?', (f"%{keyword}%",))
        else:
            response = db.select('select * from station where city like ?', (f"%{keyword}%",))
        return response

# print(Station().extract())
# print(Station().process())
# print(Station().check_station_code('董家'))
# print(Station().create_station_dict())
