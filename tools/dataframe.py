# -*- coding: UTF-8 -*-
# @author: ylw
# @file: dataframe
# @time: 2024/12/10
# @desc:
# import sys
# import os
import io
from zipfile import ZipFile
from pandas import read_excel, read_csv, DataFrame
from numpy import nan as np_nan
from enum import Enum
from dataclasses import dataclass, field
from base64 import b64decode
from typing import Union, List

from tools.wrapper import Wrapper

# F_PATH = os.path.dirname(__file__)
# sys.path.append(os.path.join(F_PATH, '..'))
# sys.path.append(os.path.join(F_PATH, '../..'))

class ContentType(Enum):
    xlsx_content = 'xlsx_content'
    xlsx_zip = 'xlsx_zip'
    xlsx_base64 = 'xlsx_base64'

    csv_content = 'csv_content'
    csv_zip = 'csv_zip'
    csv_base64 = 'csv_base64'


# class ContentEncoding(Enum):
#     ...


@dataclass
class Content2DataframeParams:
    content: Union[bytes, str] = field(default=b'')
    c_type: ContentType = field(default=None)  # content 类型
    encoding: Union[str, List[str]] = field(default='utf-8')
    dtype: Union[dict] = field(default=None)
    sheet_name: Union[str, int, List[str], List[int]] = field(default=0)
    header: int = field(default=0)
    file_name: Union[str, List[str]] = field(default=None)  # 只针对于 zip 压缩文件
    engine: str = field(default='openpyxl')  # pandas操作引擎


def non2None(df: DataFrame, *, fields: str = None) -> DataFrame:
    """
    替换 nan 为 None
    """
    if fields is None:
        df.replace({np_nan: None}, inplace=True)
    else:
        df[fields].replace({np_nan: None}, inplace=True)
    return df


class Content2DataFrame:
    def __init__(self, non2none: bool = False):
        self._non2none = non2none

    @staticmethod
    def _parse_base64(content: str) -> bytes:
        """将 Base64 编码的内容解码为字节流"""
        return b64decode(content)

    @staticmethod
    @Wrapper.wrapper_suppress_resource_warnings
    def read_xlsx(content: Union[bytes, io.BytesIO], sheet_name=0, header=0, **kwargs) -> DataFrame:

        df: DataFrame = read_excel(content, sheet_name=sheet_name, header=header, **kwargs)
        return df

    @staticmethod
    def read_csv(content: Union[bytes, io.BytesIO], encoding='utf-8', **kwargs) -> DataFrame:
        """读取 csv 内容"""
        return read_csv(content, encoding=encoding, **kwargs)

    @staticmethod
    def extract_zip(zip_content: bytes, file_name: Union[str, List[str]]) -> bytes:
        """解压 zip 文件中的内容并返回内部文件的字节流"""
        with ZipFile(io.BytesIO(zip_content), 'r') as zip_file:
            # 假设我们只处理第一个文件
            file_name = zip_file.namelist()[0]
            return zip_file.read(file_name)

    def content_to_dataframe(self, p: Content2DataframeParams) -> DataFrame:
        """根据 ContentType 转换内容为 DataFrame"""
        c_type = p.c_type
        content = p.content
        sheet_name = p.sheet_name
        header = p.header
        encoding = p.encoding
        engine = p.engine

        if c_type == ContentType.xlsx_content:  # 直接读取原始的 xlsx 内容
            return self.read_xlsx(io.BytesIO(content), sheet_name, header, engine=engine)

        if c_type == ContentType.xlsx_base64:  # 读取解码后的 xlsx 内容
            decoded_content = self._parse_base64(content)
            return self.read_xlsx(io.BytesIO(decoded_content))

        if c_type == ContentType.xlsx_zip:  # 解压并读取 xlsx 文件
            zip_content = self.extract_zip(content)
            return self.read_xlsx(io.BytesIO(zip_content))

        if c_type == ContentType.csv_content:
            return self.read_csv(io.BytesIO(content), encoding)  # 直接读取原始的 csv 内容

        if c_type == ContentType.csv_base64:
            decoded_content = self._parse_base64(content)
            return self.read_csv(io.BytesIO(decoded_content), encoding)  # 读取解码后的 csv 内容

        if c_type == ContentType.csv_zip:
            zip_content = self.extract_zip(content)
            return self.read_csv(io.BytesIO(zip_content), encoding)  # 解压并读取 csv 文件

        raise ValueError(f"Unsupported content type: {c_type}")


if __name__ == '__main__':
    print(**Content2DataframeParams())
