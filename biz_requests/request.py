# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/9
# @desc:
# import sys
# import os
from requests import Session
from typing import Optional
from dataclasses import dataclass, field

from biz_http import CustomAdapterHtt1, CustomAdapterHtt2
from headers import Headers
from response import Response
from params import Method, RequestParams


@dataclass
class Config:
    init_engine: bool = field(default=True)  # 初始化引擎
    dbname: str = field(default=None)  # 数据库名称
    retries: int = field(default=0)  # 请求重试次数
    delay: int = field(default=0)  # 重试间隔
    headers: dict = field(default_factory=dict)  # 初始化添加header key
    r_encoding: str = field(default=None)  # 响应编码 默认不设置
    http2: bool = field(default=False)  # 是否使用http2


class Request:
    RP = RequestParams
    M = Method
    C = Config

    def __init__(self, config: Optional[Config] = None):
        self.__config = config or Config()

        self.headers: Optional[Headers] = None
        self.session: Optional[Session] = None

        self.reset_session()

    def reset_session(self, headers: Optional[dict] = None):
        if isinstance(self.session, Session):
            self.session.close()

        self.session = Session()
        self.session.headers = self.headers = Headers(headers)

        # 自定义适配器
        self.session.mount('http://', CustomAdapterHtt1())
        self.session.mount('https://', CustomAdapterHtt1())

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
        requests = Request(Request.C())

        _ = requests.get(requests.RP(None, "https://spa16.scrape.center/", headers={
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }))
        print(_.headers)
        print(_.r_cookie())
        print(_.cookies)


    demo()
