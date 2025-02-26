# -*- coding: UTF-8 -*-
# @author: ylw
# @file: response
# @time: 2024/12/9
# @desc:
import pandas as pd
from json import loads as json_loads
from typing import Optional, Union
from requests.models import Response
from requests.utils import get_encoding_from_headers
from requests.cookies import extract_cookies_to_jar

from .headers import Headers
from tools.wrapper import Wrapper
from tools.cookies import CookieTools
from tools.dataframe import Content2DfParamsConfig, content2df, non2none


def decode_bytes(value):
    return value.decode() if isinstance(value, bytes) else value


class BizResponse(Response):
    """
    在这里拓展返回数据类型/封装
    """
    headers: Optional[Headers] = None

    def __init__(self, debugger: bool = False):
        super(BizResponse, self).__init__()
        self.__debugger = debugger
        self.__text: Optional[str] = None

    def head_scookie(self, as_dict: bool = True) -> Union[str, dict]:
        """ 返回response.headers['set-cookie'] """
        _ck = self.headers.get('set-cookie')
        if as_dict:
            return CookieTools.cookie_str2dict(_ck)
        return _ck

    def set_encoding(self, encodeing: str) -> 'BizResponse':
        """设置文本编码, 并返回self, 支持链式调用"""
        self.encoding = encodeing
        self.__text = None
        return self

    @property
    def text(self) -> str:
        if not hasattr(self, '__text'):
            self.__text = super().text
        return self.__text

    @Wrapper.log_text_if_exception
    def json(self, *args, **kwargs) -> dict:
        return super(BizResponse, self).json()

    @Wrapper.log_text_if_exception
    def jsonp(self) -> dict:
        """jsonp 转 json"""
        _text = self.text
        return json_loads(_text[_text.find('{'):_text.rfind('}') + 1])

    @Wrapper.log_text_if_exception
    def dataframe(self, c_type: str, **kwargs) -> pd.DataFrame:
        """
        二进制报表类型下载
        :param c_type: ContentTypeEnum
            xlsx_content | xlsx_zip | xlsx_base64
            csv_content | csv_zip | csv_base64
        """
        __non2none = kwargs.pop('non2none', False)
        df = content2df(c_type, self.text if 'base64' in c_type else self.content, Content2DfParamsConfig(
            encoding=kwargs.get('encoding', 'utf-8'),
            thousands=kwargs.get('thousands', None),
            dtype=kwargs.get('dtype', None),
            sheet_name=kwargs.get('sheet_name', 0),
            header=kwargs.get('header', 0),
            file_name=kwargs.get('file_name', None),
            engine=kwargs.get('engine', 'openpyxl'),
        ))
        return non2none(df) if __non2none else df


def ResponseSetAttr(self, req, resp) -> BizResponse:
    response = BizResponse()

    response.status_code = getattr(resp, "status", None)
    response.headers = Headers({decode_bytes(k): decode_bytes(v) for k, v in getattr(resp, "headers", {}).items()})

    response.encoding = get_encoding_from_headers(response.headers)
    response.raw = resp
    response.reason = response.raw.reason

    response.url = req.url.decode("utf-8") if isinstance(req.url, bytes) else req.url
    extract_cookies_to_jar(response.cookies, req, resp)

    response.request = req
    response.connection = self
    return response


if __name__ == '__main__':
    from requests.adapters import HTTPAdapter
    import requests


    def demo():
        class CustomAdapter(HTTPAdapter):
            def __init__(self, debugger: bool = True):
                super(CustomAdapter, self).__init__()
                self.__debugger = debugger

            def build_response(self, req, resp):
                # 使用 CustomResponse 来构建响应对象
                response = ResponseSetAttr(self, req, resp)
                return response

        session = requests.Session()
        session.mount('http://', CustomAdapter())  # 为 http 请求安装自定义适配器
        session.mount('https://', CustomAdapter())  # 为 https 请求安装自定义适配器

        print(session.request('get', 'https://www.baidu.com', headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }).encoding)


    demo()
