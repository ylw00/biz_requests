# -*- coding: UTF-8 -*-
# @author: ylw
# @file: requests_params
# @time: 2024/12/9
# @desc:
# import sys
# import os
from enum import Enum
from dataclasses import dataclass
from typing import Union, Optional, Dict, Tuple


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class MethodEnum(Enum):
    POST = 'POST'
    GET = 'GET'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    post = POST
    get = GET
    put = PUT
    delete = DELETE
    patch = PATCH


@dataclass
class SessionParams:
    method: Optional[MethodEnum] = None
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    params: Optional[Union[Dict, bytes]] = None
    data: Optional[Union[Dict, list, Tuple, bytes, object]] = None
    json: Optional[object] = None
    cookies: Optional[dict] = None
    files: Optional[dict] = None
    auth: Optional[Union[Tuple[str, str], callable]] = None
    timeout: Optional[Union[float, Tuple[float, float]]] = None
    allow_redirects: Optional[bool] = None
    proxies: Optional[Dict[str, str]] = None
    stream: Optional[bool] = None
    verify: Optional[Union[bool, str]] = None
    cert: Optional[Union[str, Tuple[str, str]]] = None


if __name__ == '__main__':
    def demo():
        aa = SessionParams()
        aa.method = 111
        print(aa.method)


    demo()
