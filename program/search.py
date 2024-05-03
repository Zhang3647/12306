import re
from plugins.get_station import Station
from plugins.station_screen import StationScreen
from plugins.search_ticket import SearchTicket
from plugins.my_ticket import Search, Verify
from plugins.search_orders_ticket import Order


class Route:
    @staticmethod
    def search(request):
        _type = request.args.get('type')
        if _type == 'StationScreen':
            station = request.args.get('station')
            if station is not None:
                result = Station().check_station_code(station)
                flag = request.args.get('flag')
                if len(result) != 0:
                    if flag is None:
                        return {'code': '0', 'data': StationScreen(result[0][1]).get_station_screen()}
                    else:
                        return {'code': '0', 'data': StationScreen(result[0][1]).get_station_screen(int(flag))}
                else:
                    return {'code': '1', 'data': []}
            else:
                return {'code': '1', 'data': []}
        elif _type == 'Station':
            station_type = request.args.get('station_type')
            if station_type is not None:
                station = request.args.get('station')
                result = Station().check_station_code(station, station_type)
                if result:
                    return {'code': '0', 'data': result}
                else:
                    return {'code': '1', 'data': []}
            else:
                return {'code': '-1', 'msg': 'station_type error'}
        elif _type == 'ticket':
            begin = request.args.get('begin')
            end = request.args.get('end')
            date = request.args.get('date')
            # ticket_type = request.args.get('ticket_type')
            if begin is not None and end is not None and date is not None:  # and ticket_type is not None
                for item in [begin, end]:
                    result = Station().check_station_code(item)
                    if len(result) == 0:
                        return {'code': '1', 'msg': 'station error'}
                if len(re.findall(r'\d{4}-\d{2}-\d{2}', date)) == 0:
                    return {'code': '1', 'msg': 'date error'}
                return {'code': '0', 'data': SearchTicket(begin, end, date).mobile_search()}
            else:
                return {'code': '-1', 'msg': 'params error'}
        elif _type == 'MyQuery':
            _type = request.args.get('operation')
            if _type is not None:
                if _type == 'search':
                    from_date = request.args.get('from_date')
                    to_date = request.args.get('to_date')
                    page_index = request.args.get('page_index')
                    order_num = request.args.get('order_num')
                    if from_date is not None and to_date is not None:
                        return {'code': '0',
                                'data': Search().search_my_ticket(from_date, to_date, page_index, order_num)}
                    else:
                        return {'code': '1', 'msg': 'params error'}
                elif _type == 'verify':
                    _uuid = request.args.get('uuid')
                    if _uuid is not None:
                        return {'code': '0', 'data': Verify().check_verify(_uuid)}
                    else:
                        return {'code': '1', 'msg': 'params error'}
                elif _type == 'create':
                    return {'code': '0', 'data': Verify().create_base64_picture()}
                else:
                    return {'code': '-1', 'msg': 'operation error'}
            else:
                return {'code': '-1', 'msg': 'operation error'}

        elif _type == 'Order':
            index = request.args.get('index')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            _type = request.args.get('status')
            return {'code': '0', 'data': Order().search_orders(index, start_date, end_date, _type)}

        else:
            return {'code': '-1', 'msg': 'type error'}
