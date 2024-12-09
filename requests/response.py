# -*- coding: UTF-8 -*-
# @author: ylw
# @file: response
# @time: 2024/12/9
# @desc:
# import sys
# import os
import pandas as pd
from typing import Any
from requests.models import Response as DResponse
from json import loads as json_loads

from wrapper import Wrapper
from headers import Headers
from cookie import extract_cookies_to_jar


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


class ResponseEncoding:
    @staticmethod
    def _parse_content_type_header(header):
        tokens = header.split(";")
        content_type, params = tokens[0].strip(), tokens[1:]
        params_dict = {}
        items_to_strip = "\"' "

        for param in params:
            param = param.strip()
            if param:
                key, value = param, True
                index_of_equals = param.find("=")
                if index_of_equals != -1:
                    key = param[:index_of_equals].strip(items_to_strip)
                    value = param[index_of_equals + 1:].strip(items_to_strip)
                params_dict[key.lower()] = value
        return content_type, params_dict

    def get_encoding_from_headers(self, headers):
        content_type = headers.get("content-type")

        if not content_type:
            return None

        content_type, params = self._parse_content_type_header(content_type)

        if "charset" in params:
            return params["charset"].strip("'\"")

        if "text" in content_type:
            return "ISO-8859-1"

        if "application/json" in content_type:
            return "utf-8"


class Response(DResponse):
    response_encoding = ResponseEncoding()

    def __init__(self, req, resp: DResponse, debugger: bool = False):
        super(Response, self).__init__()
        self.status_code = getattr(resp, "status", None)
        self.headers: Headers = Headers(dict(getattr(resp, "headers", {}).items()))

        self.encoding = self.response_encoding.get_encoding_from_headers(resp.headers)
        self.raw = resp
        self.reason = self.raw.reason
        self.url = req.url.decode("utf-8") if isinstance(req.url, bytes) else req.url

        extract_cookies_to_jar(self.cookies, req, resp)

        self.request = req
        self.connection = self

        self.__debugger = debugger

    @property
    def text(self) -> str:
        return super(Response, self).text

    def json(self, *args, **kwargs) -> Any:
        return super(Response, self).json()

    @property
    def jsonp2json(self):
        _text = self.text
        return json_loads(self.text[_text.find('{'):_text.rfind('}') + 1])

    def dataframe(self, *args, **kwargs):
        return pd.DataFrame(self.content, *args, **kwargs)


if __name__ == '__main__':
    from requests.adapters import HTTPAdapter
    import requests


    def demo():
        class CustomAdapter(HTTPAdapter):
            def build_response(self, req, resp):
                # 使用 CustomResponse 来构建响应对象
                response = Response(req, resp)
                return response

        session = requests.Session()
        session.mount('http://', CustomAdapter())  # 为 http 请求安装自定义适配器
        session.mount('https://', CustomAdapter())  # 为 https 请求安装自定义适配器

        print(session.request('get', 'https://www.baidu.com', headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }).dataframe())


    demo()
