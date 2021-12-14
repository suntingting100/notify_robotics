#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:feishu_app_tools.py
@time:2021/12/07
"""
import os
import traceback
from time import sleep

import requests

from cyclone import setting, get_root_path
from cyclone.app_setting import MODULE_NAME
from cyclone import app_logger
from cyclone.exceptions.BaseException import SendFeiShuError
from cyclone.utils.veiws_utils import normal_json_response


class FeiShuApp:
    def __init__(self):
        self.base_url = "https://open.feishu.cn"
        self.app_id = setting.app_id
        self.app_secret = setting.app_secret
        self.access_token = self.get_access_token()
        self.header = {"Authorization": "Bearer %s" % self.access_token}
        self.message_template = self.get_message_template()

    def get_message_template(self):
        f = open(get_root_path() + MODULE_NAME + os.sep + "config" + os.sep + "feishu_message.json",
                 encoding='utf-8')
        t_msg = f.read()
        f.close()
        return t_msg

    def get_access_token(self):
        uri = "/open-apis/auth/v3/app_access_token/internal/"
        params = {"app_id": self.app_id, "app_secret": self.app_secret}
        res = requests.post(self.base_url + uri, json=params)
        access_token = res.json()['app_access_token']
        return access_token

    def get_user_email(self, user_id):
        uri = "/open-apis/contact/v3/users/"
        params = {"user_id_type": "user_id"}
        res = requests.get(self.base_url + uri + user_id, params=params, headers=self.header)
        return res.json()['data']['user']['email']

    def get_chat_id_by_name(self, name):
        uri = "/open-apis/im/v1/chats/search"
        params = {"query": name}
        try:
            res = requests.get(self.base_url + uri, params=params, headers=self.header)
            chat_id = res.json()['data']['items'][0]['chat_id']
            return chat_id
        except Exception as e:
            app_logger.error("url: %s\tname:%s" % (self.base_url + uri, name))
            app_logger.error(traceback.format_exc())
            raise SendFeiShuError()

    def send_message_by_name(self, name, result, content, link=None):
        uri = "/open-apis/im/v1/messages?receive_id_type=email"
        email = name + "@cyclone-robotics.com"
        params = {"receive_id": email,
                  "content": self.message_template.replace("@@EMAIL@@", email)
                      .replace("@@LINK@@", "http://10.20.17.218:8080/" if link is None else link)
                      .replace("@@CONTENT@@", content)
                      .replace("@@COLOR@@", "green" if result == "success" else "red"),
                  "msg_type": "interactive"}
        res = requests.post(self.base_url + uri, json=params, headers=self.header)
        return res.json()

    def send_message_by_chat(self, line, user, build_job, result, content, artifact, link=None,
                             chat_id="oc_8beab9c240f458cdc3f4879ac5f35e22"):
        uri = "/open-apis/im/v1/messages?receive_id_type=chat_id"
        email = user + "@cyclone-robotics.com"

        params = {"receive_id": chat_id,
                  "content": self.message_template.replace("@@EMAIL@@", email) \
                      .replace("@@LINE@@", line) \
                      .replace("@@ARTIFACT@@", artifact) \
                      .replace("@@BUILD_JOB@@", build_job) \
                      .replace("@@LINK@@", "http://10.20.17.218:8080/" if link is None else link) \
                      .replace("@@CONTENT@@", content) \
                      .replace("@@COLOR@@", "green" if result == "success" else "red"),
                  "msg_type": "interactive"}
        try:
            res = requests.post(self.base_url + uri, json=params, headers=self.header)
            if res.json()['code'] == 0:
                return normal_json_response("飞书发送成功！")
            raise SendFeiShuError(message=res.json())
        except Exception as e:
            app_logger.error("user:%s\tresult:%s\tcontent:%s\tlink:%s" % (user, result, content, link))
            app_logger.error(traceback.format_exc())
            raise SendFeiShuError()


if __name__ == '__main__':
    app = FeiShuApp()
    # print(app.access_token)
    # chat = "oc_8beab9c240f458cdc3f4879ac5f35e22"
    # content = "\\n构建类型：ci \\n代码工程：ai-studio \\n构建时长：10 \\n构建结果：success"
    # app.send_message_by_chat("AI", "wei.yang", "ai-studio", 'success', content, 'v1.0.0', link='http://www.baidu.com')
    app.send_message_by_name("wei.yang", 'failed', '失败了')
    l = app.get_chat_id_by_name('QA自动化监控报警消息群')
    print(l)
    pass
