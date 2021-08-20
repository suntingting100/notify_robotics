#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:es_controller.py
@time:2021/08/16
"""

import asyncio
from elasticsearch import AsyncElasticsearch
from cyclone import setting, app_logger
from cyclone.exceptions.BaseException import EsError


class EsController:
    def __init__(self):
        self.es = AsyncElasticsearch(
            ['http://%s:%s@%s:%s' % (setting.es_user, setting.es_passwd, setting.es_host, setting.es_port)])

    async def insert_index(self, index, json_body):
        try:
            res = await self.es.index(index=index, body=json_body, request_timeout=5)
            app_logger.info(res)
            await self.es.close()
        except Exception as e:
            app_logger.error(e)
            return EsError

    async def delete_index_by_query(self, index, query):
        try:
            res = await self.es.delete_by_query(index=index, body=query)
            print(res)
            await self.es.close()
        except Exception as e:
            app_logger.error(e)
            return EsError


if __name__ == '__main__':
    index = 'monitor'
    # json_body = {"query": {"bool": {"must": [{"match_all": {}}]}}}
    json_body = {"query": {
        "bool": {"must": [{"query_string": {"default_field": "alert_date", "query": "*"}}], "must_not": [],
                 "should": []}}}
    esc = EsController()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    futures = asyncio.ensure_future(esc.delete_index_by_query(index, json_body))
    loop.run_until_complete(futures)
    body = futures.result()
