#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:BaseException.py
@time:2021/04/26
"""
from collections import namedtuple

Error = namedtuple('Error', ['code', 'message', 'http_status_code'])


class BaseError(Exception):
    _error = Error(0, '未知错误1', 400)

    def __init__(self, message=''):
        super(BaseError, self).__init__(message)
        self.err_desc = message or self._error.message
        self.code = self._error.code
        self.http_status_code = self._error.http_status_code


class UserTokenError(BaseError):
    _error = Error(code=4001, message='token无效', http_status_code=401)
