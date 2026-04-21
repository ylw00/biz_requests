# BizRequests

`BizRequests` 是一个面向业务脚本的同步 HTTP 请求封装库，调用风格尽量贴近 `requests`，用于减少业务取数、报表下载、响应解析和异常日志处理中的重复代码。

当前版本已经将底层请求内核替换为 `curl_cffi.requests`。上层 API、调用方式、返回对象辅助方法和异常日志行为保持兼容，同时保留浏览器指纹伪装、JA3/Akamai 指纹和 HTTP/2 能力。

## 推荐入口

新代码统一使用正式包入口：

```python
from biz_requests import BizRequest, Session, Headers, Wrapper
```

旧脚本仍可继续使用：

```python
from biz_request import BizRequest, Session, Headers, Wrapper
```

`biz_request.py` 现在只是兼容转发层，真实实现已经迁移到 `core.py`。旧入口会优先转发到 `biz_requests.core.BizRequest`，避免同一进程里混用新旧入口时出现两个不同的 `BizRequest` 类对象。

## 特性

- `Session.get/post/request` 保持 requests 风格调用。
- 请求级和全局级 `retries/delay/encoding/headers/http2` 配置。
- 基于 `curl_cffi` 的 `impersonate/ja3/akamai/extra_fp/http_version` 指纹能力。
- `BizResponse.json()` 解析失败时自动记录 `response.text`。
- `BizResponse.jsonp()` 支持 JSONP 返回值解析。
- `BizResponse.dataframe()` 支持二进制报表和 base64 报表转 `pandas.DataFrame`。
- `BizResponse.head_scookie()` 直接解析响应头里的 `set-cookie`。
- `Headers` 忽略 key 大小写，并提供 `copy()`、`cookie()` 辅助方法。
- `Wrapper.retry_until_done()`、`safe_parse()` 等业务脚本常用工具。
- 可选 MySQL/SQLAlchemy 工具封装。

## 安装依赖

```bash
pip install -r requirements.txt
```

核心依赖：

```text
python>=3.9
curl_cffi>=0.7.0
loguru>=0.7.2
pandas>=1.3.5
SQLAlchemy>=1.4.7
```

如果只使用 HTTP 请求能力，数据库相关依赖可以按需安装。

## 快速开始

`BizRequest` 不能直接实例化，需要继承后使用。

```python
from biz_requests import BizRequest


class DemoRequest(BizRequest):
    def __init__(self) -> None:
        super().__init__()
        self.init_request(
            retries=2,
            delay=1,
            headers={"user-agent": "Mozilla/5.0"},
            http2=True,
            impersonate="chrome",
        )


biz = DemoRequest()
resp = biz.request.get("https://example.com", timeout=10)

print(resp.status_code)
print(resp.text)
print(resp.headers)
```

## 请求 API

### 初始化请求会话

```python
self.init_request(
    retries=0,
    delay=0,
    encoding=None,
    headers=None,
    http2=False,
    impersonate=None,
    ja3=None,
    akamai=None,
    extra_fp=None,
)
```

参数说明：

- `retries`: 默认重试次数。
- `delay`: 默认重试间隔，单位秒。
- `encoding`: 默认响应文本编码。
- `headers`: 默认请求头，会被封装为 `Headers`。
- `http2`: 是否默认启用 HTTP/2。
- `impersonate`: curl_cffi 浏览器指纹，例如 `"chrome"`。
- `ja3`: 自定义 JA3 TLS 指纹。
- `akamai`: 自定义 Akamai HTTP/2 指纹。
- `extra_fp`: curl_cffi 的额外指纹配置。

### 发起请求

```python
resp = biz.request.get(
    "https://example.com/api",
    params={"page": 1},
    headers={"accept": "application/json"},
    timeout=10,
    retries=2,
    delay=1,
)

resp = biz.request.post(
    "https://example.com/api",
    json={"name": "biz_requests"},
    timeout=10,
)
```

也支持 `SessionParams`：

```python
from biz_requests.request.params import MethodEnum, SessionParams

resp = biz.request.request(SessionParams(
    method=MethodEnum.GET,
    url="https://example.com/api",
    headers={"accept": "application/json"},
    timeout=10,
))
```

## 响应 API

### JSON

```python
data = resp.json()
```

解析失败会自动记录当前 `response.text`，再抛出原异常。

### JSONP

```python
data = resp.jsonp()
```

支持类似 `callback({"ok": true})` 的返回值。

### Cookie

```python
cookie_dict = resp.head_scookie()
cookie_text = resp.head_scookie(as_dict=False)
```

默认返回解析后的字典。

### 编码

```python
data = resp.set_encoding("utf-8").json()
```

`set_encoding()` 返回 `self`，支持链式调用。

### DataFrame

```python
df = resp.dataframe("xlsx_content")
df = resp.dataframe("csv_base64", encoding="utf-8", non2none=True)
```

支持的 `c_type`：

- `xlsx_content`: 字节转 xlsx
- `xlsx_zip`: zip 字节包转 xlsx
- `xlsx_base64`: base64 转 xlsx
- `csv_content`: 字节转 csv
- `csv_zip`: zip 字节包转 csv
- `csv_base64`: base64 转 csv

## Headers

`Headers` 对 key 大小写不敏感。

```python
from biz_requests import Headers

headers = Headers({"User-Agent": "Mozilla/5.0", "Cookie": "a=1; b=2"})

print(headers["user-agent"])
print(headers["USER-AGENT"])
print(headers.cookie(as_dict=True))

new_headers = headers.copy(value={"accept": "application/json"})
```

## Wrapper 工具

```python
from biz_requests import Wrapper


@Wrapper.retry_until_done(retries=5, delay=6, desc="报表导出")
def wait_report():
    ...
```

`BizRequest` 也提供了两个静态方法：

```python
result = biz.safe_retry_until_done(callback_func, retries=3, delay=3)
result = biz.safe_parse(callback_func, response)
```

## Demo

运行本地 demo：

```bash
python demo.py
```

当前 `demo.py` 使用本地 `HTTPServer`，不依赖外网，覆盖：

- `BizRequest` 子类初始化
- `Session.get/post/request`
- `SessionParams + MethodEnum`
- 默认 headers 透传
- `BizResponse.json/jsonp/head_scookie`
- `Headers` 大小写兼容和 cookie 解析
- `safe_retry_until_done`

成功输出示例：

```text
All demo tests passed.
GET: {'ok': True, 'method': 'GET', 'path': '/json', 'x_demo': 'biz_requests'}
POST: {'ok': True, 'method': 'POST', 'body': '{"name":"curl_cffi"}'}
JSONP: {'ok': True, 'type': 'jsonp'}
```

## 2026-04-21 更新

- 底层请求内核从 `requests` 替换为 `curl_cffi.requests`。
- 移除请求链路对 `requests.HTTPAdapter` 的依赖。
- 新增 `curl_cffi` 指纹参数透传：`impersonate`、`ja3`、`akamai`、`extra_fp`。
- `http2=True` 时默认使用 `CurlHttpVersion.V2_0`。
- 保留原 `BizResponse` 辅助方法和返回格式。
- 明确 `biz_requests` 为正式包入口。
- 将 `BizRequest` 真实实现迁移到 `core.py`。
- `biz_request.py` 调整为旧脚本兼容转发层，继续支持 `from biz_request import ...`。
- 旧入口会转发到正式包实现，避免新旧入口混用造成类对象不一致。
- 修正包导入和旧式脚本导入兼容性。
- 新增 `requirements.txt`。
- 将 `demo.py` 改为稳定的本地回归测试脚本。

## 项目结构

```text
__init__.py             # 正式公开 API 入口
core.py                 # BizRequest 业务入口基类
biz_request.py          # 旧脚本兼容转发层
request/session.py      # curl_cffi 请求会话封装
request/response.py     # BizResponse 响应封装
request/headers.py      # Headers 封装
request/params.py       # SessionParams / MethodEnum
tools/wrapper.py        # 重试、日志装饰器
tools/dataframe.py      # 报表内容转 DataFrame
tools/cookies.py        # Cookie 工具
db_engine/              # 可选数据库工具
demo.py                 # 本地回归测试
```
