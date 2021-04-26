#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:send_feishu_message.py
@time:2021/04/26
"""
import os
import traceback
import requests

from cyclone import get_root_path
from cyclone import app_logger
from cyclone.app_setting import MODULE_NAME
from cyclone.exceptions.BaseException import SendFeiShuError

BASE_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/"


def send_feishu_interactive_card(title, content, link, button=None, token='fa64da3f-14cf-46d2-9094-29228d2a1541'):
    """
    发送飞书卡片通知，需要提供机器人token
    :param title: 卡片标题
    :param content: 卡片内容
    :param button: 卡片的按钮
    :param link: 按钮跳转的超链接
    :param token: 机器人的webhook
    :return:
    """
    from cyclone.utils.veiws_utils import normal_json_response
    header = {"Content-Type": "application/json"}
    f = open(get_root_path() + MODULE_NAME + os.sep + "config" + os.sep + "feishu_interactive_card.json",
             encoding='utf-8')
    t_msg = f.read()
    f.close()
    if button is None and link is not None:
        button = link.split("/")[4]
    msg = t_msg.replace("@@TITLE@@", title) \
        .replace("@@CONTENT@@", content) \
        .replace("@@LINK@@", link + "allure") \
        .replace("@@BUTTON@@", button)
    try:
        res = requests.post(BASE_URL + token, headers=header, data=msg.encode('utf-8'))
        if 'StatusCode' in res.text and res.json()['StatusCode'] == 0:
            return normal_json_response("飞书发送成功！")
        raise SendFeiShuError(message=res.json())
    except SendFeiShuError as e:
        app_logger.error("title:%s\tcontent:%s\tlink:%s\tbutton:%s\ttoken:%s" % (title, content, link, button, token))
        app_logger.error(traceback.format_exc())
        raise e
    except Exception as e:
        app_logger.error("title:%s\tcontent:%s\tlink:%s\tbutton:%s\ttoken:%s" % (title, content, link, button, token))
        app_logger.error(traceback.format_exc())
        raise SendFeiShuError()


def send_feishu_rich_text(title, content, link, link_text=None, at=None, token='fa64da3f-14cf-46d2-9094-29228d2a1541'):
    from cyclone.utils.veiws_utils import normal_json_response
    header = {"Content-Type": "application/json"}
    f = open(get_root_path() + MODULE_NAME + os.sep + "config" + os.sep + "feishu_post_text.json",
             encoding='utf-8')
    t_msg = f.read()
    f.close()
    if link_text is None and link is not None:
        link_text = link.split("/")[4]
    msg = t_msg.replace("@@TITLE@@", title) \
        .replace("@@CONTENT@@", content) \
        .replace("@@LINK@@", link + "allure") \
        .replace("@@BUTTON@@", link_text)
    try:
        res = requests.post(BASE_URL + token, headers=header, data=msg.encode('utf-8'))
        if 'StatusCode' in res.text and res.json()['StatusCode'] == 0:
            return normal_json_response("飞书发送成功！")
        raise SendFeiShuError(message=res.json())
    except SendFeiShuError as e:
        app_logger.error(
            "title:%s\tcontent:%s\tlink:%s\tbutton:%s\tat:%s\ttoken:%s" % (title, content, link, link_text, at, token))
        app_logger.error(traceback.format_exc())
        raise e
    except Exception as e:
        app_logger.error(
            "title:%s\tcontent:%s\tlink:%s\tbutton:%s\tat:%s\ttoken:%s" % (title, content, link, link_text, at, token))
        app_logger.error(traceback.format_exc())
        raise SendFeiShuError()


if __name__ == '__main__':
    send_feishu_rich_text(title="title", content="content\\n fasfds\\n dfhgf\\n jghjwtrw3 utyuu", link="https://open.feishu.cn/open-apis/bot/v2/hook/",
                          token="fa64da3f-14cf-46d2-9094-29228d2a1541")
    pass
