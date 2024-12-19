# -*- coding: UTF-8 -*-
# @author: ylw
# @file: cookies
# @time: 2024/12/10
# @desc:
# import sys
# import os

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))


class CookieTools:

    @staticmethod
    def cookie_dict2str(dict_cookie: dict) -> str:
        return ';'.join([f'{k}={v}' for k, v in dict_cookie.items()])

    @staticmethod
    def cookie_str2dict(str_cookie: str) -> dict:
        ck_dict = {}
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
