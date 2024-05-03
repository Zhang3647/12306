from whole.Flask import app
from flask import request, make_response
from program.login import Route as LoginRoute
from program.search import Route as SearchRoute
from plugins.get_station import Station


@app.errorhandler(Exception)
def handle_generic_error():
    return "Internal Server Error", 500


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/')
def index():
    return 'hello'


@app.route('/login/<name>', methods=['GET', 'POST'])
def login(name):
    """
    判断用户登录的类型
    :param name:
    :return:
    """
    return LoginRoute().login(name, request, make_response)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    查询车票,车站,本人车票,车站大屏
    :return:
    """
    return SearchRoute().search(request)


@app.route('/update_station', methods=['GET', 'POST'])
def update_station():
    """
    更新车站信息
    :return:
    """
    return Station().process()


@app.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
    """
    返回favicon
    :return:
    """
    return 'favicon'
