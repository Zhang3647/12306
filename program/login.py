from plugins.login import Login, Owner


class Route:
    @staticmethod
    def login(name, request, make_response):
        if name == '12306':
            return Login.route(request, make_response)
        elif name == 'owner':
            verify = Owner(request).login()
            if verify['code'] == '0':
                del verify['token']
                response = make_response({'code': '0', 'data': verify}, 200)
                return response
            else:
                return verify
        else:
            return {'code': '-1', 'msg': 'login type error'}
