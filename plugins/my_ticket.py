# import threading
# import time

import requests
from plugins.cookie import get_cookie
# from plugins.login import picture

url = [
    "https://kyfw.12306.cn/otn/psr/query",
    'https://kyfw.12306.cn/passport/web/create-verifyqr64',
    'https://kyfw.12306.cn/otn/psr/checkVerifyqr'
]


class Verify:
    def __init__(self):
        self.cookie = get_cookie()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0.0.0 Safari/537.36',
            'Cookie': self.cookie
        }

    def create_base64_picture(self):
        headers = self.headers
        """
        Host: kyfw.12306.cn
        Origin: https://kyfw.12306.cn
        Referer: https://kyfw.12306.cn/otn/view/personal_travel.html
        """
        headers['Host'] = 'kyfw.12306.cn'
        headers['Referer'] = 'https://kyfw.12306.cn/otn/view/personal_travel.html'
        headers['Origin'] = 'https://kyfw.12306.cn'

        data = "appid=otn&authType=itinerary"

        response = requests.get(url[1], headers=headers, data=data).json()
        # threading.Thread(target=picture, args=(response.json(),)).start()
        return response.json()

    def check_verify(self, uuid):
        headers = self.headers
        headers['Host'] = 'kyfw.12306.cn'
        headers['Referer'] = 'https://kyfw.12306.cn/otn/view/personal_travel.html'
        headers['Origin'] = 'https://kyfw.12306.cn'

        data = {
            'uuid': uuid,
            'appid': 'otn'
        }
        print("请于1分钟内完成验证")
        response = requests.get(url[2], headers=headers, data=data).json()
        if response['data'] == '0':
            return {'code': '0', 'msg': "等待用户进行验证"}
        elif response['data'] == '1':
            return {'code': '1', 'msg': "等待用户完成验证"}
        elif response['data'] == '2':
            return {'code': '2', 'msg': "验证成功"}
        elif response['data'] == '3':
            return {'code': '3', 'msg': "验证超时, 请重新验证"}

        return {'code': '1', 'msg': "用户验证超时, 请重新验证"}


class Search:
    def __init__(self):
        self.cookie = get_cookie()

    def search_my_ticket(self, form_date, end_date, page_index=1, order_num=''):
        """
        用于查询用户本人车票, 如未验证则调用Verify类进行验证
        :param form_date:
        :param end_date:
        :param page_index:
        :param order_num:
        :return:
                code: 0 验证成功
                      1 用户未扫描二维码或已超时
                      3 二维码已失效
                      msg: 提示信息
        """
        payload = (f'from_date={form_date}&end_date={end_date}&'
                   f'order_num={order_num}&pageIndex={page_index}&titcket_type=1')
        headers = {
            'Host': 'kyfw.12306.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0.0.0 Safari/537.36',
            'Referer': 'https://kyfw.12306.cn/otn/view/personal_travel.html',
            'Origin': 'https://kyfw.12306.cn',
            'Cookie': self.cookie
        }

        response = requests.request("POST", url[0], headers=headers, data=payload).json()

        if response['status']:
            return {'code': '0', 'msg': '查询成功', 'data': response['data']['psr']}
        else:
            return {'code': '1', 'msg': "用户未进行验证, 请先进行验证"}
