#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:build_result_notify.py
@time:2021/12/13
"""
from pydantic.main import BaseModel
from cyclone import app
from cyclone.exceptions.BaseException import *
from cyclone.utils.feishu_app_tools import FeiShuApp


class BuildInfo(BaseModel):
    build_job: str
    build_number: int
    build_url: str = None
    env: str = None
    ci: bool
    cd: bool
    test: bool
    build_result: str
    duration_time: float
    artifact: str = None
    test_report: str = None


class ProjectInfo(BaseModel):
    project: str
    branch: str = None


class JsonBody(BaseModel):
    """
    message_type: 消息类型
    receiver: 群机器人token
    title: 消息标题
    content: 消息内容
    """
    line: str
    user: str
    message_type: str = "department"
    project_info: ProjectInfo = None
    build_info: BuildInfo = None
    department_name: str = "机器人测试"


@app.post("/buildResult")
def send_message(json_body: JsonBody):
    feishu_app = FeiShuApp()
    try:
        content = "\\n构建时长：%s \\n构建结果：%s" % (
            json_body.build_info.duration_time,
            json_body.build_info.build_result)
        build_type = "\\n构建类型："
        if json_body.build_info.ci:
            build_type = build_type + " ci "
            content = "%s\\n代码工程：%s" % (content, json_body.project_info.project)
        if json_body.build_info.cd:
            build_type = build_type + " cd "
            content = "%s\\n部署环境：%s" % (content, json_body.build_info.env)
        if json_body.build_info.test:
            build_type = build_type + " test "
            content = "%s\\n测试结果：%s" % (content, json_body.build_info.test_report)

        content = build_type + content
        print(content)
        chart_id = feishu_app.get_chat_id_by_name(json_body.department_name)
        res = feishu_app.send_message_by_chat(json_body.line, json_body.user, json_body.build_info.build_job,
                                              json_body.build_info.build_result, content, json_body.build_info.artifact,
                                              json_body.build_info.build_url, chart_id)
        return res
    except SendFeiShuError as e:
        raise e
    except Exception:
        raise SendFeiShuError
