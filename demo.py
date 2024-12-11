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
    def demo():
        requests = Tm().request

        _ = requests.get("https://spa16.scrape.center/", headers={
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }, delay=3, retries=2)
        print(_.headers)
        print(_.resp_cookie())
        print(_.cookies)


    demo()


    Tm().crawl_response()
