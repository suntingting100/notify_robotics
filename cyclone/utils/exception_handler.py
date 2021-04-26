#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:exception_handler.py
@time:2021/04/26
"""
import time

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from cyclone import app, app_logger
from cyclone.exceptions.BaseException import BaseError


@app.exception_handler(BaseError)
def base_exception_handler(request: Request, exc: BaseError):
    # return Response(status_code=exc.http_status_code, content=exc.err_desc)
    return JSONResponse(status_code=exc.http_status_code,
                        content=jsonable_encoder({"code": exc.code, "message": exc.err_desc}), )


@app.exception_handler(RequestValidationError)
def request_validation_error(request: Request, exc: RequestValidationError):
    app_logger.warn('\t'.join([
        '-' * 6,
        'REQUEST:{0}:{1}'.format(request.method, request.url),
        'HEADERS:{0}'.format(dict(request.headers)),
        'URL PARAMS:{0}'.format(request.path_params),
        'REQUEST BODY:{0}'.format(exc.body),
        'ERROR:{0}'.format(exc.errors()),
        '~' * 6,
    ]))
    return JSONResponse(status_code=500, content=jsonable_encoder({"error": exc.errors(), "request_body": exc.body}))