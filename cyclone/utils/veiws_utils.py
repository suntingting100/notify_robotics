# -*- coding: UTF-8 -*-

import random
import time

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse


def normal_json_response(message, code=20000, data=''):
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder({"code": code, "message": message, "data": data}))
