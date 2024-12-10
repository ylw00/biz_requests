# -*- coding: UTF-8 -*-
# @author: ylw
# @file: request
# @time: 2024/12/10
# @desc:
# import sys
# import os
from typing import Optional

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from request import Session, RequestConfig, MethodEnum
from db_engine import Engine, EngineConfig


class Request:
    def __init__(self):
        self.request: Optional[Session] = None
        self.engine: Optional[Engine] = None

    def init_request(self, retries=0, delay=0, headers=None, encoding=None, http2=False):
        self.request = Session(RequestConfig(
            retries=retries, delay=delay, headers=headers, r_encoding=encoding, http2=http2
        ))
        return self

    def init_engine(self, dbname, user, pwd, host, port, charset):
        self.engine = Engine(EngineConfig(
            dbname=dbname, user=user, password=pwd, host=host, port=port, charset=charset
        ))
        return self


class BizRequest(Request):
    def __init__(self):
        super(BizRequest, self).__init__()

    def lopp_page(self):
        ...

    def safe_parse(self):
        ...


if __name__ == '__main__':
    def demo():
        class Tm(BizRequest):
            def __init__(self):
                super(Tm, self).__init__()
                self.init_request().init_engine()

            def crawl_response(self):
                self.request.get('', headers={}).json()


    demo()
