#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:jira_controller.py
@time:2021/08/20
"""
import base64
import json
import os
import time
from datetime import datetime

from cyclone import setting
from jira import JIRA
from cyclone.app_setting import MODULE_NAME
from cyclone import get_root_path


class JiraController:
    def __init__(self):
        # token = base64.b64encode(("%s:%s" % (setting.jira_user, setting.jira_apikey)).encode()).decode()
        self.jira = JIRA(setting.jira_site, basic_auth=(setting.jira_user, setting.jira_apikey))
        self.config_path = get_root_path() + MODULE_NAME + os.sep + "config" + os.sep + "jira_issue_assignee.json"

    def get_issues(self, issue_id):
        return self.jira.issue(issue_id).fields

    def create_issue_by_project_key(self, project, env, user_id, summary, description=None):
        issue_dict = {
            'project': {'key': project},
            'summary': summary,
            'priority': {'name': 'P0'},
            # 'description': description,
            'issuetype': {'id': '10203'},
            # 'customfield_10094': {'value': '稳定性问题'},
            # 'customfield_10096': {'value': '生产环境'},
            # 'customfield_10097': {'value': '系统挂起/停服/不可用'},
            'labels': [
                env
            ],
            'assignee': {'id': user_id},
            'customfield_10103': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000+0800')
        }
        issue = self.jira.create_issue(issue_dict)
        # self.jira.create_issue_link('Relates', 'TEST-19', issue.key)
        return issue

    def create_issue_by_business_line(self, line, env, user_id, summary, description=None):
        with open(self.config_path) as f:
            json_body = json.load(f)
            project = json_body[line]['project']
            summary = '[%s] %s' % (line, summary)
        issue = self.create_issue_by_project_key(project, env, user_id, summary, description)
        return issue

    def search_user_id(self, user):
        params = {'query': user}
        json_res = self.jira._get_json(path='user/search', params=params)
        return json_res[0]['accountId']

    def search_user_by_business_line(self, line):
        with open(self.config_path) as f:
            json_body = json.load(f)
            user = json_body[line]['assignee']
        return self.search_user_id(user)


if __name__ == '__main__':
    jira = JiraController()
    id = jira.search_user_id('wei.yang')
    # f = jira.get_issues('TEST-23')
    # f = jira.search_user_by_business_line("ai")
    # f = jira.create_issue_by_business_line('ai', id, 'test', 'test')
    j = {"project": "TEST", "env": "test", "user_id": id, "summary": "test", "description": "test"}
    f = jira.create_issue_by_project_key(**j)
    # params = {'query': 'le.xu'}
    # f = jira.jira._get_json(path='user/search', params=params)
    print(f)
    # n = datetime.now()
    # print(n.strftime('%Y-%m-%dT%H:%M:%S.000+0800'))
    pass
