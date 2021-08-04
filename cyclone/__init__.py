#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:__init__.py
@time:2021/04/16
"""
import os
import sys
import logging
from fastapi import FastAPI
from fastapi.logger import logger as app_logger
from logging.handlers import RotatingFileHandler
from cyclone.app_setting import AppBaseSetting, get_root_path

# 获取基础配置
setting = AppBaseSetting()

app = FastAPI()
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

LOG_PATH = get_root_path() + "logs"
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

formatter = logging.Formatter(
    "[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s", "%Y-%m-%d %H:%M:%S")
handler = RotatingFileHandler(get_root_path() + '/logs/server.log', backupCount=0)
logging.getLogger().setLevel(logging.NOTSET)
app_logger.addHandler(handler)
handler.setFormatter(formatter)

# 注册异常拦截
from cyclone.utils.exception_handler import *

# 注册接口地址
from cyclone.controller.notify_send import app
from cyclone.controller.alert_reporter import app


if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app_logger.handlers = gunicorn_logger.handlers
    app_logger.setLevel(gunicorn_logger.level)
