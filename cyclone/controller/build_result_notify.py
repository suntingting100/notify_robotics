#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:build_result_notify.py
@time:2021/12/13
"""
import traceback

from pydantic.main import BaseModel
from cyclone import app
from cyclone import app_logger
from cyclone.exceptions.BaseException import *
from cyclone.utils.feishu_app_tools import FeiShuApp
from cyclone.orms.ci_info_orm import CiInfo
from cyclone.orms.job_result_orm import JobResult
from cyclone.utils.save_db import SaveDB


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
        content = "\\n**构建结果：**\\n%s \\n\\n**构建详情：**\\n构建时长：%s" % (
            json_body.build_info.build_result,
            json_body.build_info.duration_time)
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

        content = content + build_type
        if json_body.message_type == 'department':
            chart_id = feishu_app.get_chat_id_by_name(json_body.department_name)
            res = feishu_app.send_message_by_chat(json_body.line, json_body.user, json_body.build_info.build_job,
                                                  json_body.build_info.build_result, content, json_body.build_info.artifact,
                                                  json_body.build_info.build_url, chart_id)
        elif json_body.message_type == 'user':
            res = feishu_app.send_message_by_name(json_body.line, json_body.user, json_body.build_info.build_job,
                                                  json_body.build_info.build_result, content,
                                                  json_body.build_info.artifact,
                                                  json_body.build_info.build_url)
        build_result = JobResult(line=json_body.line, user=json_body.user, job_name=json_body.build_info.build_job,
                                 build_number=json_body.build_info.build_number, env=json_body.build_info.env,
                                 ci=str(json_body.build_info.ci), cd=str(json_body.build_info.cd),
                                 test=str(json_body.build_info.test), duration_time=json_body.build_info.duration_time,
                                 status=json_body.build_info.build_result, branch=json_body.project_info.branch)
        ci_info = CiInfo(project=json_body.project_info.project, build_Number=json_body.build_info.build_number,
                         tag=json_body.build_info.artifact, branch=json_body.project_info.branch,
                         ci_status=json_body.build_info.build_result)
        try:
            db_client = SaveDB()
            if json_body.build_info.ci:
                db_client.save_to_db(ci_info.__tablename__, ci_info)
            db_client.save_to_db(build_result.__tablename__, build_result)
        except Exception as e:
            feishu_app.send_message_by_name('yunpeng.liu', 'failed', '保存数据库失败，快检查！')
            app_logger.error(traceback.format_exc())
            raise SaveDBError
        return res
    except SendFeiShuError as e:
        raise e
    except Exception:
        raise SendFeiShuError
