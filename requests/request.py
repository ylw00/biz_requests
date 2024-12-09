# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/9
# @desc:
# import sys
# import os
from requests.adapters import HTTPAdapter
import requests as d_requests
from typing import Optional, Any, Union
from dataclasses import dataclass, field

from headers import Headers
from response import Response
from params import Method, Params
from wrapper import Wrapper


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
@dataclass
class Config:
    init_engine: bool = field(default=True)  # 初始化引擎
    dbname: str = field(default=None)  # 数据库名称
    retries: int = field(default=0)  # 请求重试次数
    delay: int = field(default=0)  # 重试间隔
    headers: dict = field(default_factory=dict)  # 初始化添加header key
    r_encoding: str = field(default=None)  # 响应编码 默认不设置


class CustomAdapter(HTTPAdapter):

    def __init__(self, debugger: bool = True):
        super(CustomAdapter, self).__init__()
        self.__debugger = debugger

    def build_response(self, req, resp):
        # 使用 BizResponse 来构建响应对象
        response = Response(req, resp, self.__debugger)
        return response


class Requests:
    def __init__(self):
        self.__config: Optional[Config] = None
        self.headers: Optional[Headers] = None
        self.session: Optional[d_requests.Session] = None

        self.reset_session({'a': '1'})

    def reset_session(self, headers: Optional[dict] = None):
        self.session = d_requests.Session()
        self.session.headers = self.headers = Headers(headers or self.__config.headers)

        # 自定义适配器
        self.session.mount('http://', CustomAdapter())
        self.session.mount('https://', CustomAdapter())

    def request(self, params_c: Params) -> Response:
        # if method not in Method:
        #     raise ValueError(f"Invalid method: `{method}`")
        with self.session.request(
                params_c.get_method().value,
                params_c.get_url(),
                params=params_c.get_params(),
                data=params_c.get_data(),
                json=params_c.get_json(),
                headers=params_c.get_headers(),
                cookies=params_c.get_cookies(),
                timeout=params_c.get_timeout()
        ) as response:
            response: Response = response
            return response

    def get(self, params_c: Params):
        params_c.set_method(Method.get)
        return self.request(params_c)

    def post(self, params_c: Params):
        params_c.set_method(Method.post)
        return self.request(params_c)




if __name__ == '__main__':
    def demo():
        requests = Requests()

        _ = requests.post('https://www.baidu.com', headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        })
        a = _.headers
        b = _.jsonp2json


    demo()
