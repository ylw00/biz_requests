# -*- coding: UTF-8 -*-
# @author: ylw
# @file: demo
# @time: 2024/12/10
# @desc:
# import sys
# import os

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))
from biz_request import BizRequest


class Tm(BizRequest):
    def __init__(self):
        super(Tm, self).__init__()
        self.init_request()

    def parse_respone(self, response_j: dict):
        response_j['aaa']

    def crawl_response(self):
        data = {'aa': 111}
        self.safe_parse(self.parse_respone, data)


if __name__ == '__main__':
    Tm().crawl_response()
