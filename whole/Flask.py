from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

import config.config


class Config(object):
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 调度器开关
    # job存储位置
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(
            url=fr"sqlite:///{config.config.GetConfig().get_project_path()}\data\scheduler.db")
    }
    # 线程池配置
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 10}
    }


app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
