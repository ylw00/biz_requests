# -*- coding: UTF-8 -*-
from __future__ import annotations

from typing import Dict, Optional


class CookieTools:

    @staticmethod
    def cookie_dict2str(dict_cookie: Dict[str, str]) -> str:
        return ';'.join([f'{k}={v}' for k, v in dict_cookie.items()])

    @staticmethod
    def cookie_str2dict(str_cookie: Optional[str]) -> Dict[str, str]:
        if not isinstance(str_cookie, str):
            return {}

        ck_dict: Dict[str, str] = {}
        str_cookie_split = []
        for i in str_cookie.split(';'):
            for j in i.split(','):
                str_cookie_split.append(j.strip())
        for ck in str_cookie_split:
            if 'Max-Age=' in ck or 'Path=/' in ck or 'HttpOnly' in ck:
                continue

            resulut = ck.split('=', 1)
            if len(resulut) != 2:
                continue
            key, value = resulut
            ck_dict[key] = value
        return ck_dict


if __name__ == '__main__':
    pass
