import datetime
import json
import time
import urllib.parse
import requests
import random
import string
from plugins.cookie import get_cookie

url = [
    'https://kyfw.12306.cn/otn/leftTicket/queryG',
    'https://kyfw.12306.cn/otn/leftTicket/init',
    'https://mobile.12306.cn/otsmobile/app/mgs/mgw.htm'
]


# 写一个方法, 使其返回一个24位的大小写字母加数字
def generate_sign(num: int) -> str:
    digits = string.digits
    all_chars = string.ascii_letters + digits
    sign = ''.join(random.choice(all_chars) for _ in range(num))
    return sign


def random_string(length) -> str:
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Process:
    @staticmethod
    def get_seat_info(_type) -> str:
        b = {
            "A": "高级动卧",
            "A1": "下铺",
            "A3": "上铺",
            "B": "混编硬座",
            "C": "混编硬卧",
            "D": "包厢软座",
            "E": "特等软座",
            "F": "动卧",
            "F1": "下铺",
            "F3": "上铺",
            "G": "二人软包",
            "H": "一人软包",
            "H1": "下铺",
            "H3": "上铺",
            "I": "一等卧",
            "I1": "下铺",
            "I3": "上铺",
            "J": "二等卧",
            "J1": "下铺",
            "J2": "中铺",
            "J3": "上铺",
            "K": "混编软座",
            "L": "混编软卧",
            "M": "一等座",
            "O": "二等座",
            "P": "特等座",
            "Q": "多功能座",
            "S": "二等包座",
            "0": "棚车",
            "1": "硬座",
            "2": "软座",
            "3": "硬卧",
            "31": "下铺",
            "32": "中铺",
            "33": "上铺",
            "4": "软卧",
            "41": "下铺",
            "43": "上铺",
            "5": "包厢硬卧",
            "6": "高级软卧",
            "61": "下铺",
            "63": "上铺",
            "7": "一等软座",
            "8": "二等软座",
            "9": "商务座"
        }
        return b[_type]

    def parse_ticket_info(self, ticket_info) -> list:
        parsed_info = []
        for i in range(len(ticket_info) // 10):
            item_value = ticket_info[i * 10:(i + 1) * 10]
            flag = item_value[0]
            num = int(item_value[-2:])
            price = item_value[1:6]
            # print(self.get_seat_info(flag), num, int(price) / 10)
            parsed_info.append({
                'seat_type': self.get_seat_info(flag),
                'num': num,
                'price': int(price) / 10,
            })
        return parsed_info

    def process_mobile_search(self, info) -> list:
        result = []
        for item in info['result']['ticketResult']:
            # print(self.parse_ticket_info(item['yp_info_cover']))
            result.append({
                'train_no': item['train_no'],
                'station_train_code': item['station_train_code'],
                'start_time': item['start_time'],
                'arrive_time': item['arrive_time'],
                'lishi': item['lishi'],
                'seat_info': self.parse_ticket_info(item['yp_info_cover']),
                'yp_ex': item['yp_ex'],
                'controlled_train_message': item['controlled_train_message']
            })
        return result


class SearchTicket:
    def __init__(self, begin, end, date):
        self.begin = begin
        self.end = end
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36"
        }
        self.date = date

    def search_ticket(self, date: str) -> dict:
        data = {
            'leftTicketDTO.train_date': date,
            'leftTicketDTO.from_station': self.begin,
            'leftTicketDTO.to_station': self.end,
            'purpose_codes': 'ADULT'  # purpose_codes= '0X00' 学生票 purpose_codes = 'ADULT' 成人票
        }
        headers = self.headers
        headers['cookie'] = get_cookie()
        response = requests.get(url[0], headers=headers, params=data)
        return response.json()

    def process_ticket(self):
        ticket = self.search_ticket(self.date)
        if ticket['status'] and ticket['httpstatus'] == 200:
            for item in ticket['data']['result']:
                # print(item)
                print(item.split('|'))
        else:
            print('查询失败')

    def mobile_search(self) -> dict:
        headers = self.headers
        headers['User-Agent'] = 'Dalvik/2.1.0 (Linux; U; Android 9; V1938T Build/PQ3A.190605.04081832)'
        headers['Host'] = 'mobile.12306.cn'
        headers['Cookie'] = get_cookie()
        api = 'com.cars.otsmobile.queryLeftTicketG'
        data = [{"train_date": f"{self.date}", "purpose_codes": "00",
                 "from_station": f"{self.begin}", "to_station": f"{self.end}",
                 "station_train_code": "", "start_time_begin": "0000", "start_time_end": "2400", "train_headers": "QB#",
                 "train_flag": "", "seat_type": "0", "seatBack_Type": "", "ticket_num": "", "dfpStr": "",
                 "baseDTO": {"check_code": f"{random_string(32)}",
                             "device_no": f"TEMP-{generate_sign(24)}", "h5_app_id": "60000001",
                             "h5_app_version": "5.8.1.116", "hwv": "V1938T", "mobile_no": "", "os_type": "a",
                             "time_str": f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                             "user_name": "", "version_no": "5.8.0.4"}}]
        # print(_url)
        a = {
            'c': f'{json.dumps(data).replace(' ', '')}'
        }
        # print(urllib.parse.urlencode(a).split('=')[1])
        _url = (f"https://mobile.12306.cn/otsmobile/app/mgs/mgw.htm?"
                f"operationType={api}&requestData={urllib.parse.urlencode(a).split('=')[1]}&"
                f"ts={int(time.time()) * 1000}&"
                f"sign={random_string(32)}")
        # print(_url)
        return requests.get(_url, headers=headers).json()

# print(SearchTicket('DTK', 'KZK', '2024-04-19').process_ticket())
# print(SearchTicket('DTK', 'KZK', '2024-04-19').save_cookie())
# print(SearchTicket('BJP', 'SHH', '2024-04-25').get_cookie())
# print()
#
# k = SearchTicket('DTK', 'KZK', '20240422').mobile_search()
# print(Process().process_mobile_search(k))

# print(parse_ticket_info(trains["ypInfoCover"]))
