# -*- coding: UTF-8 -*-
# @author: ylw
# @file: dataframe
# @time: 2024/12/10
# @desc:
# import sys
# import os
from io import BytesIO
from zipfile import ZipFile
from pandas import read_excel, read_csv, DataFrame, concat
from numpy import nan as np_nan
from enum import Enum
from dataclasses import dataclass, field
from base64 import b64decode
from typing import Optional, Union, List, Dict

from tools.wrapper import Wrapper

__content2df: Optional['Content2df'] = None


class ContentTypeEnum(Enum):
    xlsx_content = 'xlsx_content'
    xlsx_zip = 'xlsx_zip'
    xlsx_base64 = 'xlsx_base64'

    csv_content = 'csv_content'
    csv_zip = 'csv_zip'
    csv_base64 = 'csv_base64'


@dataclass
class Content2DfParamsConfig:
    encoding: Union[str, List[str]] = field(default='utf-8')
    dtype: Union[dict] = field(default=None)
    sheet_name: Union[str, int, List[str], List[int]] = field(default=0)
    header: int = field(default=0)
    file_name: Union[str, List[str]] = field(default=None)  # 只针对于 zip 压缩文件
    engine: str = field(default='openpyxl')  # pandas操作引擎


def df_concat(*dfs):
    """配合zip文件处理方法 合并多个zip中的excel文件"""
    return concat(dfs, axis=0)


def non2none(df: DataFrame, *, fields: str = None) -> DataFrame:
    """
    替换 nan 为 None
    """
    if fields is None:
        df.replace({np_nan: None}, inplace=True)
    else:
        df[fields].replace({np_nan: None}, inplace=True)
    return df


class Content2df:
    @staticmethod
    def _parse_base64(content: str) -> bytes:
        """将 Base64 编码的内容解码为字节流"""
        return b64decode(content)

    @staticmethod
    @Wrapper.ignore_resource_warnings
    def read_xlsx(content: bytes, **kwargs) -> DataFrame:
        if 'PK' not in str(content[:2]).upper():
            kwargs['engine'] = None  # 非压缩文件使用 openpyxl 会报错

        return read_excel(BytesIO(content), **kwargs)

    @staticmethod
    def read_csv(content: Union[bytes, BytesIO], encoding='utf-8', **kwargs) -> DataFrame:
        return read_csv(content, encoding=encoding, **kwargs)

    @staticmethod
    def extract_zip(zip_content: bytes, file_name: Union[str, List[str]]) -> Union[bytes, Dict[str, bytes]]:
        """解压 zip 文件中的内容并返回内部文件的字节流"""
        extracted_files = {}

        with ZipFile(BytesIO(zip_content), 'r') as zip_file:
            zip_file_list = zip_file.namelist()
            if len(zip_file_list) == 0:
                return b''
            f_list = [file_name] if isinstance(file_name, str) else (file_name or zip_file_list)
            for f in f_list:
                if f not in zip_file_list:  # 检查文件是否存在
                    raise FileNotFoundError(f"File {f} not found in the ZIP archive.")
                with zip_file.open(f) as file:
                    extracted_files[f] = file.read()

        if len(f_list) == 1:  # 如果只请求一个文件，直接返回文件内容字节流
            return extracted_files[f_list[0]]
        return extracted_files  # 返回多个文件时，返回一个字典

    def xlsx_content(self, content, **kwargs):
        """处理字节 XLSX 内容"""
        return self.read_xlsx(content, **kwargs)

    def xlsx_base64(self, content, **kwargs):
        """处理 base64 编码的 XLSX 内容"""
        decoded_content = self._parse_base64(content)
        return self.read_xlsx(decoded_content, **kwargs)

    def xlsx_zip(self, content, file_name, **kwargs):
        """处理压缩的 XLSX 文件"""
        zip_content = self.extract_zip(content, file_name)
        if not zip_content:
            return DataFrame()
        if isinstance(zip_content, bytes):
            return self.read_xlsx(zip_content, **kwargs)
        return df_concat(*[self.read_xlsx(c, **kwargs) for c in zip_content.values()])

    def csv_content(self, content, encoding='utf-8', **kwargs):
        """处理字节 CSV 内容"""
        return self.read_csv(BytesIO(content), encoding=encoding, **kwargs)

    def csv_base64(self, content, encoding='utf-8', **kwargs):
        """处理 base64 编码的 CSV 内容"""
        decoded_content = self._parse_base64(content)
        return self.read_csv(BytesIO(decoded_content), encoding=encoding, **kwargs)

    def csv_zip(self, content, encoding, file_name, **kwargs):
        """处理压缩的 CSV 文件"""
        zip_content = self.extract_zip(content, file_name)
        if not zip_content:
            return DataFrame()
        if isinstance(zip_content, bytes):
            return self.read_csv(BytesIO(zip_content), encoding=encoding, **kwargs)
        return df_concat(*[
            self.read_csv(BytesIO(c), encoding=encoding, **kwargs)
            for c in zip_content.values()
        ])


def content2df(c_type: str, content: Union[bytes, str], p: Content2DfParamsConfig) -> DataFrame:
    """根据 ContentType 转换内容为 DataFrame"""
    global __content2df
    __content2df = __content2df or Content2df()
    config_data = p.__dict__
    encoding = config_data.pop('encoding', None)
    file_name = config_data.pop('file_name', None)

    # 根据 content_type 调用相应的处理函数
    # excel
    if c_type == ContentTypeEnum.xlsx_content.value:
        return __content2df.xlsx_content(content, **config_data)

    if c_type == ContentTypeEnum.xlsx_base64.value:
        return __content2df.xlsx_base64(content, **config_data)

    if c_type == ContentTypeEnum.xlsx_zip.value:
        return __content2df.xlsx_zip(content, file_name, **config_data)

    # csv
    if c_type == ContentTypeEnum.csv_content.value:
        return __content2df.csv_content(content, encoding, **config_data)

    if c_type == ContentTypeEnum.csv_base64.value:
        return __content2df.csv_base64(content, encoding, **config_data)

    if c_type == ContentTypeEnum.csv_zip.value:
        return __content2df.csv_zip(content, encoding, file_name, **config_data)

    raise ValueError(f"Unsupported content type: {c_type}")


if __name__ == '__main__':
    def run_func(**kwargs):
        print(kwargs)


    run_func(**Content2DfParamsConfig().__dict__)
