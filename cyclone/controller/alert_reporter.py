#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:alert_reporter.py
@time:2021/08/04
"""
import json

from pydantic.class_validators import Optional
from pydantic.main import BaseModel

from cyclone import app
from cyclone.exceptions.BaseException import *
from cyclone.module import send_feishu_message
from cyclone import app_logger


class Labels(BaseModel):
    alertname: str
    app: str
    env: str
    instance: str
    job: str
    line: str
    result: str
    severity: str
    suite: str
    url: str
    xtime: str


class Annotations(BaseModel):
    summary: str


class JsonBody(BaseModel):
    status: str
    commonLabels: Optional[Labels]
    commonAnnotations: Optional[Annotations]


@app.post("/alertReporter")
def alert_reporter(token: str, json_body: JsonBody):
    app_logger.info(token)
    app_logger.info(json_body)
    title = "线上监控-%s" % json_body.commonLabels.app
    content = "%s于%s发出告警：%s" % (
        json_body.commonLabels.suite, json_body.commonLabels.xtime,
        json_body.commonAnnotations.summary)
    link = json_body.commonLabels.url
    button = json_body.commonLabels.alertname
    res = send_feishu_message.send_feishu_interactive_card(title, content, link=link, button=button, token=token)
    return res


if __name__ == '__main__':
    pass
