# -*- coding: UTF-8 -*-
# @author: ylw
# @file: biz_session
# @time: 2024/12/9
# @desc:
# import sys
# import os
from requests import Session as RSession
from typing import Optional
from dataclasses import dataclass, field

from http1 import CustomAdapterHtt1  # , CustomAdapterHtt2
from headers import Headers
from response import Response
from params import MethodEnum, RequestParams


@dataclass
class RequestConfig:
    # init_engine: bool = field(default=True)  # 初始化引擎
    # dbname: str = field(default=None)  # 数据库名称
    retries: int = field(default=0)  # 请求重试次数
    delay: int = field(default=0)  # 重试间隔
    headers: dict = field(default_factory=dict)  # 初始化添加header key
    r_encoding: str = field(default=None)  # 响应编码 默认不设置
    http2: bool = field(default=False)  # 是否使用http2


class Session:
    RP = RequestParams
    RC = RequestConfig
    M = MethodEnum

    def __init__(self, config: Optional[RequestConfig] = None):
        self.__config = config or RequestConfig()

        self.headers: Optional[Headers] = None
        self.session: Optional[RSession] = None

        self.reset_session()

    def reset_session(self, headers: Optional[dict] = None):
        if isinstance(self.session, RSession):
            self.session.close()

        self.session = RSession()
        self.session.headers = self.headers = Headers(headers)

        # 自定义适配器
        self.session.mount('http://', CustomAdapterHtt1())
        self.session.mount('https://', CustomAdapterHtt1())

    def request(
            self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None,
            allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None,
            retries=0, delay=0,
    ) -> Response:
        with self.session.request(
                method, url, params, data, headers, cookies, files, auth, timeout,
                allow_redirects, proxies, hooks, stream, verify, cert, json
        ) as response:
            response: Response = response
            return response

    def get(
            self, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None,
            allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None,
            retries=0, delay=0,
    ):
        return self.request(
            'get', url, params, data, headers, cookies, files, auth, timeout,
            allow_redirects, proxies, hooks, stream, verify, cert, json, retries, delay
        )

    def post(
            self, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None,
            allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None,
            retries=0, delay=0,
    ):
        return self.request(
            'post', url, params, data, headers, cookies, files, auth, timeout,
            allow_redirects, proxies, hooks, stream, verify, cert, json, retries, delay
        )


if __name__ == '__main__':
    def demo():
        requests = Session(Session.C())

        _ = requests.get(requests.RP(None, "https://spa16.scrape.center/", headers={
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }))
        print(_.headers)
        print(_.resp_cookie())
        print(_.cookies)


    demo()
