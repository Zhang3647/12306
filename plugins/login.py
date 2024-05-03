import base64
import random
import string
from io import BytesIO
from PIL import Image
import requests

import config.config
from plugins.cookie import get_cookie, save_cookie
from requests import utils
from data.databse import DB

url = [
    "https://kyfw.12306.cn/passport/web/create-qr64",
    "https://kyfw.12306.cn/passport/web/checkqr",
    "https://kyfw.12306.cn/passport/web/auth/uamtk",
    "https://kyfw.12306.cn/otn/login/userLogin",
    "https://kyfw.12306.cn/otn/uamauthclient"
]


def picture(r):
    img_data = base64.b64decode(r['image'])  # 解码时只要内容部分
    image = Image.open(BytesIO(img_data))
    image.show()


def get_random_str(_len=12):
    _str = string.ascii_letters + string.digits
    randstr = ''.join(random.choice(_str) for _ in range(_len))
    return randstr


class Login:
    def __init__(self):
        self._headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36"
        }
        self.requests = None

    @staticmethod
    def route(request, make_response):
        _type = request.args.get('type')
        if _type == 'get_picture':
            response = make_response(Login().get_base64_picture(), '200')
            response.headers['Content-Type'] = 'application/json;charset=utf-8'
            return response
        elif _type == 'check_login':
            if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
                _uuid = request.get_json()
                response = make_response(Login().check_login(_uuid['uuid']), '200')
                response.headers['Content-Type'] = 'application/json;charset=utf-8'
                return _uuid
            else:
                response = make_response({'code': '-1', 'msg': "请求方式或参数不正确"}, '200')
                response.headers['Content-Type'] = 'application/json;charset=utf-8'
                return response
        else:
            response = make_response({'code': '-1', 'msg': "接口类型不正确"}, '200')
            response.headers['Content-Type'] = 'application/json;charset=utf-8'
            return response

    def get_base64_picture(self):
        headers = self._headers
        headers['Referer'] = 'https://kyfw.12306.cn/otn/resources/login.html'
        headers['Origin'] = 'https://kyfw.12306.cn'
        headers['cookie'] = get_cookie()
        return requests.get(url[0], headers=headers, params={'appid': 'otn'}).json()

    def check_login(self, uuid) -> dict:
        """
        检查用户是否登录
        :return:
                code: 0 用户未扫描
                      1 用户已扫描
                      2 用户已登录
                      3 二维码已失效
                msg: 提示信息
        """
        self.requests = requests.session()
        headers = self._headers
        headers['Referer'] = 'https://kyfw.12306.cn/otn/resources/login.html'
        headers['Origin'] = 'https://kyfw.12306.cn'
        # headers['cookie'] = get_cookie()
        data = {
            'uuid': uuid,
            'appid': "otn"
        }
        r = self.requests.post(url[1], headers=headers, data=data).json()
        if r['result_code'] == '0':
            return {'code': '0', 'msg': '正在等待用户扫描二维码'}
        elif r['result_code'] == '1':
            return {'code': '1', 'msg': '二维码已扫描，正在等待用户确认'}
        elif r['result_code'] == '2':
            self.get_js_session_id()
            self.get_tk(self.check_uamtk())
            requests_cookie = self.get_key()
            save_cookie(requests_cookie)
            return {'code': '2', 'msg': '登录成功', 'cookie': requests_cookie}
        elif r['result_code'] == '3':
            return {'code': '3', 'msg': '二维码已失效'}
        return {'code': '4', 'msg': '用户未扫描二维码或已超时'}

    def get_js_session_id(self):
        headers = self._headers
        headers['Referer'] = 'https://kyfw.12306.cn/otn/resources/login.html'
        headers['Host'] = 'kyfw.12306.cn'
        self.requests.get(url[3])

    def check_uamtk(self):
        headers = self._headers
        headers['Referer'] = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        headers['Origin'] = 'https://kyfw.12306.cn'
        headers['Host'] = 'kyfw.12306.cn'
        return self.requests.post(url[2], data={'appid': 'otn'}).json()['newapptk']

    def get_tk(self, apptk):
        headers = self._headers
        headers['Referer'] = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        headers['Origin'] = 'https://kyfw.12306.cn'
        headers['Host'] = 'kyfw.12306.cn'

        return self.requests.post(url[4], headers=headers, data={'tk': apptk}).json()['username']

    def get_key(self):
        """
        根据tk获取key,然后返回cookie
        :return:
        """
        headers = self._headers
        headers['Referer'] = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        headers['Host'] = 'kyfw.12306.cn'
        self.requests.cookies.clear("kyfw.12306.cn", "/passport", name='uamtk')
        # headers['cookie'] = cookie
        self.requests.get(url[3])
        self.requests.get(url[3])
        dict_cookies = requests.utils.dict_from_cookiejar(self.requests.cookies)
        cookie = ''
        for key, value in dict_cookies.items():
            cookie += key + '=' + value + ';'
        # print(cookie)
        return cookie


class Owner:
    def __init__(self, request):
        self.request = request

    def login(self):
        pwd = self.request.args.get('pwd')
        user_id = self.request.args.get('user_id')
        if pwd is not None and user_id is not None:
            name = f'{config.config.GetConfig().get_project_path()}\\data\\user_info.db'
            result = DB(name).select(
                'select count(*) from user where user_id=? and pwd=?', (user_id, pwd))
            if result[0][0] == 1:
                login_info = {
                    'token': get_random_str(36)
                }
                DB('name').update('update user set token=? where user_id=?', (login_info['token'], user_id))
                return {'code': '0', 'msg': '登录成功', 'login_info': login_info}
            else:
                return {'code': '-1', 'msg': '用户名或密码错误'}
        else:
            return {'code': '-1', 'msg': '参数不正确'}

# print(Login().check_login())
# pdata = {rint(Login().get_picture_base64())
# print(Login().get_apptk(Login().get_picture_base64()['apptk']))
# print(Login().check_login(Login().get_picture_base64()))
# print(Login().get_key(Login().get_apptk("oymZsusv40NpJ6n//OKSmjPKpqG69eE76rZV-kIQ45y1y0")))
