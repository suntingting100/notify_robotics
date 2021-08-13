#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:alert_reporter.py
@time:2021/08/04
"""
import json
import os

from fastapi import Path
from fastapi.encoders import jsonable_encoder

from pydantic.class_validators import Optional, List
from pydantic.main import BaseModel

from cyclone import app, get_root_path
from cyclone.app_setting import MODULE_NAME
from cyclone.exceptions.BaseException import *
from cyclone.module import send_feishu_message
from cyclone import app_logger


class AlertLabels(BaseModel):
    alertname: str
    app: Optional[str]
    env: Optional[str]
    instance: Optional[str]
    job: Optional[str]
    line: Optional[str]
    severity: Optional[str]
    suite: Optional[str]
    url: Optional[str]


class AlertAnnotation(BaseModel):
    summary: Optional[str]


class Alerts(BaseModel):
    labels: Optional[AlertLabels]
    annotations: Optional[AlertAnnotation]


class Labels(BaseModel):
    alertname: str
    app: Optional[str]
    env: Optional[str]
    instance: Optional[str]
    job: Optional[str]
    line: Optional[str]
    severity: Optional[str]
    suite: Optional[str]
    url: Optional[str]


class Annotations(BaseModel):
    summary: str


class JsonBody(BaseModel):
    status: str
    alerts: Optional[List[Alerts]]
    commonLabels: Optional[Labels]
    commonAnnotations: Optional[Annotations]


@app.post("/alertReporter/{line}")
def alert_reporter(json_body: JsonBody, line: str = Path(None, title='业务线')):
    json_compatible_item_data = jsonable_encoder(json_body)
    app_logger.info(json_compatible_item_data)

    token_file = get_root_path() + MODULE_NAME + os.sep + "config" + os.sep + "token.json"
    with open(token_file) as f:
        json_object = json.load(f)
    try:
        token = json_object[line]
    except KeyError as e:
        raise LineNotFoundError
    app_logger.info(json_body)
    title = "线上监控-%s" % json_body.commonLabels.app
    content = ''
    link = "http://10.20.17.124:9093/#/alerts"
    button = 'alert manager'
    if json_body.commonLabels.suite is not None and json_body.status == 'firing':
        content = "%s %s告警：%s" % (json_body.commonLabels.suite, '发出', json_body.commonAnnotations.summary)
    elif json_body.commonLabels.suite is not None and json_body.status == 'resolved':
        content = "%s 解除告警" % json_body.commonLabels.suite
    else:
        for a in json_body.alerts:
            content += "%s 发出告警：%s [测试报告](%s)" % (a.labels.suite, a.annotations.summary, a.labels.url) + "\\n\\n"
    if json_body.commonLabels.url is not None:
        link = json_body.commonLabels.url
        button = json_body.commonLabels.alertname
    res = send_feishu_message.send_feishu_interactive_card(title, content, link=link, button=button, token=token)
    app_logger.info(res)
    return res


if __name__ == '__main__':
    pass
