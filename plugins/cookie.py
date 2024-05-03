import requests
from config.config import GetConfig

url = [
    'https://kyfw.12306.cn/otn/leftTicket/init'
]

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}


def get_cookie() -> str:
    with open(f'{GetConfig().get_project_path()}\\resource\\cookie.txt', 'rt', encoding='utf-8') as f:
        cookie = f.read()
        f.close()
    return cookie


def new_cookie() -> str:
    response = requests.get(url[0], headers=headers)
    cookie = (f'route={response.cookies.get("route")};'
              f'BIGipServerotn={response.cookies.get("BIGipServerotn")};'
              f'JSESSIONID={response.cookies.get("JSESSIONID")};')
    with open(f'{GetConfig().get_project_path()}\\resource\\cookie.txt', 'wt', encoding='utf-8') as f:
        f.write(cookie)
    return cookie


def save_cookie(_new_cookie):
    with open(f'{GetConfig().get_project_path()}\\resource\\cookie.txt', 'wt', encoding='utf-8') as f:
        f.write(_new_cookie)
