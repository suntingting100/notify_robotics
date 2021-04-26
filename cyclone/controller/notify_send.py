#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:notify_send.py
@time:2021/04/26
"""
from pydantic.main import BaseModel

from cyclone import app
from cyclone.exceptions.BaseException import *
from cyclone.module import send_feishu_message


class JsonBody(BaseModel):
    message_type: str = 'card'
    receiver: str
    title: str
    content: str
    at: str = None
    link: str = None
    link_text: str = None


@app.post("/sendMessage")
def send_message(json_body: JsonBody):
    try:
        if json_body.message_type == 'card':
            res = send_feishu_message.send_feishu_interactive_card(json_body.title, json_body.content, json_body.link,
                                                                   json_body.link_text, json_body.receiver)
            return res
        elif json_body.message_type == 'rich':
            res = send_feishu_message.send_feishu_rich_text(json_body.title, json_body.content, json_body.link,
                                                            json_body.link_text, json_body.at, json_body.receiver)
            return res
        raise SendFeiShuError(message="不支持的message type！")
    except Exception:
        raise SendFeiShuError
