# -*- coding: UTF-8 -*-
# @author: ylw
# @file: http1
# @time: 2024/12/10
# @desc:
# import sys
# import os
from requests.adapters import HTTPAdapter
# from hyper.contrib import HTTP20Adapter

from .response import ResponseSetAttr
# from hyper_development.hyper.contrib import HTTP20Adapter
# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


class CustomAdapterHtt1(HTTPAdapter):

    def __init__(self, debugger: bool = True):
        super(CustomAdapterHtt1, self).__init__()
        self.__debugger = debugger

    def build_response(self, req, resp):  # request, resp
        return ResponseSetAttr(self, req, resp)


# class FakeOriginalResponse(object):  # pragma: no cover
#     def __init__(self, headers):
#         self._headers = headers
#
#     def get_all(self, name, default=None):
#         values = []
#
#         for n, v in self._headers:
#             if n == name.lower():
#                 values.append(v)
#
#         if not values:
#             return default
#
#         return values
#
#     def getheaders(self, name):
#         return self.get_all(name, [])


# class CustomAdapterHtt2(HTTP20Adapter):
#     def __init__(self, debugger: bool = True):
#         super(CustomAdapterHtt2, self).__init__()
#         self.__debugger = debugger
#
#     def build_response(self, request, resp):
#         response = ResponseSetAttr(self, request, resp)
#         response.__debugger = self.__debugger
#
#         resp.release_conn = lambda: None
#
#         response.raw._original_response = orig = FakeOriginalResponse(None)
#         orig.version = 20
#         orig.status = resp.status
#         orig.reason = resp.reason
#         orig.msg = FakeOriginalResponse(resp.headers.iter_raw())
#
#         return response


if __name__ == '__main__':
    pass
