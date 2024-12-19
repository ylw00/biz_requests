# -*- coding: UTF-8 -*-
# @author: ylw
# @file: headers
# @time: 2024/12/9
# @desc:
# import sys
# import os
from collections import OrderedDict
from typing import Optional, Union

from tools.cookies import CookieTools


# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class Headers(OrderedDict):
    __default_head = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    def __init__(self, headers: Optional[dict] = None, **kwargs):
        _headers = {k.lower(): v for k, v in headers.items()} if isinstance(headers, dict) else {}
        _kwargs = {k.lower(): v for k, v in kwargs.items()}
        _headers = {**self.__default_head, **_headers, **_kwargs}
        super(Headers, self).__init__(**_headers)

    def __repr__(self):
        return repr(dict(self))  # 返回字典的字符串表示

    def __str__(self):
        return str(dict(self))  # 返回字典的字符串表示

    def __getitem__(self, key: str):
        key = key.lower()
        return super(Headers, self).get(key)

    def __setitem__(self, key: str, value):
        key = key.lower()
        return super(Headers, self).__setitem__(key, value)

    def __delitem__(self, key):
        key = key.lower()
        return super(Headers, self).pop(key, None) is not None

    def get(self, __key: str):
        __key = __key.lower()
        return super(Headers, self).get(__key)

    def update(self, __m: dict, **kwargs) -> 'Headers':
        if not isinstance(__m, dict):
            return self

        m = {k.lower(): v for k, v in __m.items()}
        for key, value in m.items():
            if value is None and key in self:
                self.pop(key, None)
                del m[key]

        super(Headers, self).update(m, **kwargs)
        return self

    def copy(self: 'Headers', **kwargs) -> 'Headers':
        """
        **kwargs:
            state_stay: bools; 默认保存当前的字段状态
            value: dict; 需要新增的字段
        """
        state_stay = kwargs.get('state_stay', True)
        _d = dict(self) if state_stay else {}
        _d.update({k.lower(): v for k, v in kwargs.get('value', {}).items()})
        return Headers(_d)

    def cookie(self, as_dict=False) -> Union[str, dict, None]:
        cookie: Optional[str] = self.get('cookie')
        if as_dict is False:
            return cookie

        if not isinstance(cookie, str):
            return {}
        return CookieTools.cookie_str2dict(cookie)


if __name__ == '__main__':
    def demo():
        head = Headers()
        head.clear()
        print(head)


    demo()
