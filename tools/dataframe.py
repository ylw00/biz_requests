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
from typing import Union, List, Dict

from tools.wrapper import Wrapper

content_2_df: 'Content2df'


class ContentTypeEnum(Enum):
    xlsx_content = 'xlsx_content'
    xlsx_zip = 'xlsx_zip'
    xlsx_base64 = 'xlsx_base64'

    csv_content = 'csv_content'
    csv_zip = 'csv_zip'
    csv_base64 = 'csv_base64'


@dataclass
class Content2DfParamsConfig:
    c_type: Union[str, ContentTypeEnum] = field(default=None)  # content 类型
    content: Union[bytes, str] = field(default=b'')
    encoding: Union[str, List[str]] = field(default='utf-8')
    dtype: Union[dict] = field(default=None)
    sheet_name: Union[str, int, List[str], List[int]] = field(default=0)
    header: int = field(default=0)
    file_name: Union[str, List[str]] = field(default=None)  # 只针对于 zip 压缩文件
    engine: str = field(default='openpyxl')  # pandas操作引擎


def df_concat(*dfs):
    """配合zip文件处理方法 合并多个zip中的excel文件"""
    return concat(dfs, axis=0)


def non2None(df: DataFrame, *, fields: str = None) -> DataFrame:
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
    def _extract_zip(zip_content: bytes, file_name: Union[str, List[str]]) -> Union[bytes, Dict[str, bytes]]:
        """解压 zip 文件中的内容并返回内部文件的字节流"""
        extracted_files = {}

        with ZipFile(BytesIO(zip_content), 'r') as zip_file:
            zip_file_list = zip_file.namelist()
            if len(zip_file_list):
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

    @staticmethod
    @Wrapper.ignore_resource_warnings
    def read_xlsx(content: Union[bytes, BytesIO], sheet_name=0, header=0, **kwargs) -> DataFrame:
        return read_excel(content, sheet_name=sheet_name, header=header, **kwargs)

    @staticmethod
    def read_csv(content: Union[bytes, BytesIO], sheet_name=0, header=0, encoding='utf-8', **kwargs) -> DataFrame:
        return read_csv(content, sheet_name=sheet_name, header=header, encoding=encoding, **kwargs)



    def xlsx_content(self, content, sheet_name, header, engine, **kwargs) -> DataFrame:
        """处理字节 XLSX 内容"""
        return self.read_xlsx(BytesIO(content), sheet_name, header, engine=engine, **kwargs)

    def xlsx_base64(self, content, sheet_name, header, engine, **kwargs) -> DataFrame:
        """处理 base64 编码的 XLSX 内容"""
        decoded_content = self._parse_base64(content)
        return self.read_xlsx(BytesIO(decoded_content), sheet_name, header, engine=engine, **kwargs)

    def xlsx_zip(self, content, file_name, sheet_name, header, engine, **kwargs) -> DataFrame:
        """处理压缩的 XLSX 文件"""
        zip_content = self._extract_zip(content, file_name)
        if not zip_content:
            return DataFrame()
        if isinstance(zip_content, bytes):
            return self.read_xlsx(BytesIO(zip_content), sheet_name, header, engine=engine, **kwargs)
        return df_concat(*[
            self.read_xlsx(BytesIO(c), sheet_name, header, engine=engine, **kwargs)
            for c in zip_content.values()
        ])

    def csv_content(self, content, sheet_name, header, encoding, engine, **kwargs) -> DataFrame:
        """处理字节 CSV 内容"""
        return self.read_csv(BytesIO(content), sheet_name, header, encoding, engine=engine, **kwargs)

    def csv_base64(self, content, sheet_name, header, encoding, engine, **kwargs) -> DataFrame:
        """处理 base64 编码的 CSV 内容"""
        decoded_content = self._parse_base64(content)
        return self.read_csv(BytesIO(decoded_content), sheet_name, header, encoding, engine=engine, **kwargs)

    def csv_zip(self, content, file_name, sheet_name, header, encoding, engine, **kwargs) -> DataFrame:
        """处理压缩的 CSV 文件"""
        zip_content = self._extract_zip(content, file_name)
        if not zip_content:
            return DataFrame()
        if isinstance(zip_content, bytes):
            return self.read_csv(BytesIO(zip_content), sheet_name, header, encoding, engine=engine, **kwargs)
        return df_concat(*[
            self.read_csv(BytesIO(c), sheet_name, header, encoding, engine=engine, **kwargs)
            for c in zip_content.values()
        ])


def content2df(c_type: str, content: Union[bytes, str], p: Content2DfParamsConfig, **kwargs) -> DataFrame:
    """根据 ContentType 转换内容为 DataFrame"""
    global content_2_df
    content_2_df = content_2_df or Content2df()
    header = p.header
    encoding = p.encoding
    engine = p.engine
    sheet_name = p.sheet_name
    file_name = p.file_name

    # 根据 content_type 调用相应的处理函数
    if c_type == ContentTypeEnum.xlsx_content.value:
        return content_2_df.xlsx_content(content, sheet_name, header, engine, **kwargs)

    if c_type == ContentTypeEnum.xlsx_base64.value:
        return content_2_df.xlsx_base64(content, sheet_name, header, engine, **kwargs)

    if c_type == ContentTypeEnum.xlsx_zip.value:
        return content_2_df.xlsx_zip(content, file_name, sheet_name, header, engine, **kwargs)

    if c_type == ContentTypeEnum.csv_content.value:
        return content_2_df.csv_content(content, sheet_name, header, encoding, engine, **kwargs)

    if c_type == ContentTypeEnum.csv_base64.value:
        return content_2_df.csv_base64(content, sheet_name, header, encoding, engine, **kwargs)

    if c_type == ContentTypeEnum.csv_zip.value:
        return content_2_df.csv_zip(content, file_name, sheet_name, header, encoding, engine, **kwargs)

    raise ValueError(f"Unsupported content type: {c_type}")


if __name__ == '__main__':
    def run_func(**kwargs):

        cdp = Content2DfParamsConfig(header=kwargs.get('header'))
        print(cdp)

    run_func()
