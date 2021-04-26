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


class JsonBody(BaseModel):
    receiver: str = None
    sender: str = None
    token: str
    title: str
    content: str
    link: str = None


@app.post("/sendMessage")
def send_message(json_body: JsonBody):
    print("send")
    raise UserTokenError
