import requests

from plugins.cookie import get_cookie

url = [
    'https://kyfw.12306.cn/otn/queryOrder/queryMyOrder'
]


class Order:
    def __init__(self):
        # self.cookie = get_cookie()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0.0.0 Safari/537.36',
        }

    def search_orders(self, index, start_date, end_date, _type):
        headers = self.headers
        """
        Host: kyfw.12306.cn
        Origin: https://kyfw.12306.cn
        Referer: https://kyfw.12306.cn/otn/view/personal_travel.html
        """
        headers['Host'] = 'kyfw.12306.cn'
        headers['Referer'] = 'https://kyfw.12306.cn/otn/view/train_order.html'
        headers['Origin'] = 'https://kyfw.12306.cn'
        headers['Cookie'] = get_cookie()

        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        payload = f'come_from_flag=my_order&pageIndex={index}&pageSize=8&query_where={_type}&queryStartDate={start_date}&queryEndDate={end_date}&queryType=1&sequeue_train_name='
        response = requests.post(url[0], headers=headers, data=payload)
        return response.json()

