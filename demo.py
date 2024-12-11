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
        self.set_request()

    @staticmethod
    def parse_respone(response_j: dict):
        return response_j['aa']

    def crawl_response(self):
        data = {'aa': 111}
        # data = self.request.get('https://www.baidu.com').json()

        print(self.safe_parse(self.parse_respone, data))
        print(self.safe_parse(self.parse_respone, {'aa': 11111}))


if __name__ == '__main__':
    Tm().crawl_response()
