#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:http_requests.py
@time:2021/08/16
"""

import requests
import datetime

from elasticsearch import AsyncElasticsearch
from cyclone import setting, app_logger
from cyclone.exceptions.BaseException import EsError


class RequestHandler:
    def get_http(self, url, **kwargs):
        """get 方法"""
        params = kwargs.get("params", {})
        headers = kwargs.get("headers", {})
        headers['base'] = ""
        try:
            result = requests.get(url, params=params, headers=headers)
            return result.json()
        except Exception as e:
            app_logger.error(e)

if __name__ == '__main__':
    result = RequestHandler().get_http("http://10.20.17.218:8080/job/AI_Jobs/view/AI-%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95/job/AI-dsu-auto-test-all/allure/widgets/summary.json")
    print(result)