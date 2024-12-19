# BizRequests

requests的方法的拓展和重写，主打一个偷懒

github: `https://github.com/ylw00/biz_requests`

vx: y278369368

就是想偷懒, 不用写乱七八糟的导包(之前写的删了,太烂了)

已经自用了一段时间才敢发出来玩, 感觉也还可以,确实轻松了点


## 胡乱写的,可能只适合***业务(我不是爬虫)
- 菜菜菜菜菜菜菜菜菜菜菜菜菜菜菜菜菜菜菜菜菜

## 1. 依赖

```text
python==3.9.9
requests==2.31.0

这里主要是搞mysql连接(目前设计的还有点臃肿, 后续会逐渐的做优化)
SQLAlchemy==1.4.7
pandas==1.3.5

loguru==0.7.2
```

## 2. 需求

- `请求效率要求不高`,  甚至还需要sleep, 如果需要效率也没必要使用同步库
- `捕获异常返回值`, 异常情况需要打印或者保存到日志文件, 便于后续代码的分析优化
- `二进制报表(dataframe)`, 经常会导出一些二进制报表, 或者是base64类型
- 场景示例: 商家后台取数需求

## 3. 新增方法

- **(请求/响应)**
  - 重写`requests.request`: 新增 `retries, delay` 参数,增加重试功能
  - 重写`response.json`: json序列化, 失败则自动日志输出 response.text
  - 新增`response.jsonp`: json序列化jsonp类型返回值, 失败则自动日志输出 response.text
  - 新增`response.dataframe`: 二进制报表(返回dataframe), 参数: `c_type, non2none` ;同理, 如果失败则自动日志输出 response.text
  - 新增`response.head_scookie`: 返回['set-cookie'], 参数 `as_dict`: 返回值类型
  - 新增`response.set_encoding`: 设置编码并返回`self`, 支持 response.set_encoding().json()


- **参数c_type: 六种模式**
  - `xlsx_content`:  字节转xlsx
  - `xlsx_zip`:      字节[压缩包]转xlsx
  - `xlsx_base64`:   base64转xlsx
  - `csv_content`:   字节转csv
  - `csv_zip`:       字节[压缩包]转csv
  - `csv_base64`:    base64转csv


- **Headers[重写]**
  - 忽略大小写敏感
  - 重写`copy`: 参数state_stay: 是否保持当前的key状态; value: 覆盖或新增key


- **Wrapper[装饰器工具]**
  - `add_method_desc`: 给函数增加 desc 属性, 我一般用来写注释(菜菜菜)
  - `retry_until_done`: 用来重试直到成功(不为None); 场景1: 报表导出


- **(操作/用户)**
  - 只能`继承`去使用BizRequest
  - `init_request`: 初始化session, 全局配置`retries, delay, headers`
  - `init_engine`: 初始化`mysql`, 目前有点臃肿, 后续再去优化吧
  - `safe_parse`: 解析：self.safe_parse(lambda: n: n['data'], response), 失败则自动日志输出 `函数传参`

## 4. 代码



```python
from biz_request import BizRequest

# 请求方式跟requests一摸一样
biz_req = BizRequest()  # 不能直接使用, 必须要继承, 这里只是做一个demo
biz_req.init_request().init_engine()  # 设置seeion, mysql连接

# 请求新增两个参数  delay=3, retries=2 如果 delay=0 则不重试 默认不重试
_ = biz_req.request.get('').text
biz_req.request.get('').json()  # 报错则自动日志输出.text文本
biz_req.request.get('').jsonp()  # 报错则自动日志输出.text文本

# 支持六种模式  xlsx_content | xlsx_zip | xlsx_base64 | csv_content | csv_zip | csv_base64
biz_req.request.get('').dataframe()  # 报错则自动日志输出.text文本

# ----------------------------------------------------------------------------------------------

from biz_request import BizRequest, Wrapper, Headers

headers = Headers()
# Headers【大写小写不敏感】; 并增加了方法, copy, cookie 

# 解析失败的话, 则自动日志输出参数
biz_req = BizRequest()  # 不能直接使用, 必须要继承, 这里只是做一个demo
biz_req.safe_parse()  # 参数1: 回调解析response函数;  *args, **kwargs: 回调函数参数 

# 适用于等待报表导出, 直至成功
@Wrapper.retry_until_done(retries=5, delay=6, desc='...报表导出失败')
def demo():
    ...
```

## 5. 拓展
```text
response.py  # 新增返回值类型
biz_requests.py  # 加入业务函数封装
```

## 6. 菜菜菜

```text
1, 原本想使用 `from hyper.contrib import HTTP20Adapter` 使得 requests 支持 http2 请求, 但是好像并不理想, 就放弃了  `http1.py`

2, 可以试试通过适配器 加入简单的 tls/ja3 指纹算法
```

## 7. 完整demo 见demo.py
```text
菜菜菜
```