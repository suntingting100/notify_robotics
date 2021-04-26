#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:app_setting.py
@time:2021/04/16
"""
import os

from pydantic import BaseSettings

MODULE_NAME = "cyclone"


def get_root_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find(MODULE_NAME, 20)]
    return root_path


class AppBaseSetting(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 8080
    log_level: str = 'info'
    jenkins_base_url = ""

    class Config:
        env_file = get_root_path() + "/.env"
        env_file_encoding = "utf-8"
