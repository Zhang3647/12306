import json


class GetConfig:
    def __init__(self):
        pass

    @staticmethod
    def get_station_version() -> str:
        with open('config/config.json', 'rt', encoding='utf-8') as f:
            station_version = json.load(f)['station_version']
            f.close()
        return station_version

    @staticmethod
    def get_project_path():
        with open('config/config.json', 'rt', encoding='utf-8') as f:
            project_path = json.load(f)['PATH']
            f.close()
        return project_path
