# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/9
# @desc:
# import sys
# import os
from requests import Session
from requests.adapters import HTTPAdapter
from hyper import HTTP20Adapter
from typing import Optional
from dataclasses import dataclass, field

from headers import Headers
from response import Response
from params import Method, RequestParams


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


class Request:
    RP = RequestParams
    M = Method

    def __init__(self):
        self.__config: Optional[Config] = None
        self.headers: Optional[Headers] = None
        self.session: Optional[Session] = None

        self.reset_session()

    def reset_session(self, headers: Optional[dict] = None):
        if isinstance(self.session, Session):
            self.session.close()

        self.session = Session()
        self.session.headers = self.headers = Headers(headers)

        # 自定义适配器
        self.session.mount('http://', CustomAdapter())
        self.session.mount('https://', CustomAdapter())

    def request(self, p: RequestParams) -> Response:
        method = p.method
        if method not in Method:
            raise ValueError(f"Invalid method: `{method}`")
        with self.session.request(
                method.value, p.url, params=p.params, data=p.data, json=p.json, headers=p.headers,
                cookies=p.cookies, timeout=p.timeout, verify=p.verify, allow_redirects=p.allow_redirects
        ) as response:
            response: Response = response
            return response

    def get(self, p: RequestParams):
        p.method = Method.get
        return self.request(p)

    def post(self, p: RequestParams):
        p.method = Method.post
        return self.request(p)


if __name__ == '__main__':
    def demo():
        requests = Request()

        _ = requests.post(requests.RP(None, 'http://www.baidu.com', headers={

        })).dataframe()


    demo()
