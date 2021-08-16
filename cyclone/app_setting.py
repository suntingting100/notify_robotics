#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:app_setting.py
@time:2021/04/16
"""
import os

from pydantic import BaseSettings

MODULE_NAME = 'cyclone'


def get_root_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path.removesuffix(MODULE_NAME)
    return root_path


class AppBaseSetting(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 8080
    log_level: str = 'info'
    jenkins_base_url = ""
    es_host: str = '10.20.17.176'
    es_port: int = 30092
    es_user: str = 'elastic'
    es_passwd: str = 'Sxs2tHD312j431WPGi850CXk'
    es_index: str = 'monitor'

    class Config:
        env_file = get_root_path() + "/.env"
        env_file_encoding = "utf-8"
