import time

import requests
import string
import random

"""
这部分用的是智行的接口
"""

url = [
    "https://m.suanya.com/restapi/soa2/24635/getScreenStationData"
]


def random_num(num: int) -> str:
    all_chars = string.digits
    sign = ''.join(random.choice(all_chars) for _ in range(num))
    return sign


class StationScreen:
    def __init__(self, station):
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36"
        }

        self.station = station

    def get_station_screen(self, screen_flag=0) -> dict:
        """
        获取车站的屏幕信息
        返回值中invalidWaitingScreens为停止检票的车次信息, stationWaitingScreens为正在检票和正在候车的车次信息
        :return:
        """
        headers = self.headers
        # headers['origin'] = f"https://m.ctrip.com"
        # headers['referer'] = "https://m.ctrip.com/"
        # headers['cookieorigin'] = 'https://m.ctrip.com'
        # headers['host'] = "m.suanya.com"
        # headers['x-requested-with'] = 'com.yipiao'

        random_str = random_num(20)
        params = {
            "_fxpcqlniredt": f"{random_str}",
            "x-traceID": f"{random_str}-{int(time.time()) * 1000}-{random_num(7)}"
        }
        data = {"stationName": f"{self.station}", "screenFlag": screen_flag,
                "authentication": {"partnerName": "ZhiXing", "source": "", "platform": "APP"},
                "head": {"cid": f"{random_str}", "ctok": "", "cver": "1005.006", "lang": "01", "sid": "8888",
                         "syscode": "32", "auth": "", "xsid": "", "extension": []}}

        response = requests.post(url[0], headers=headers, params=params, json=data)
        return response.json()
#
#
# if __name__ == '__main__':
#     print(StationScreen("董家口").get_station_screen())
