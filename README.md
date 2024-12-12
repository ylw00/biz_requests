# BizRequests

简易requests封装

vx: y278369368

### 1. 依赖

```text
python==3.9.9
requests==2.31.0

这里主要是搞mysql连接
SQLAlchemy==1.4.7
pandas==1.3.5

日志
loguru==0.7.2
```

### 2. 背景/适合业务

```text
- 对效率要求不搞
- 数据准确性要求高(日志输出敏感性)
- 导出二进制报表
总结：类似商家后台数据需求
```

### 3. 新增封装方法

```python
from biz_request import BizRequest

# 请求方式跟requests一摸一样
biz_req = BizRequest()  # 不能直接使用, 必须要继承, 这里只是做一个demo
biz_req.setRequest().setEngine()  # 设置seeion, mysql连接

# 请求新增两个参数  delay=3, retries=2 如果 delay=0 则不重试 默认不重试
_ = biz_req.request.get('').text
biz_req.request.get('').json()  # 自动日志输出返回值文本
biz_req.request.get('').jsonp2json()  # 自动日志输出返回值文本

# 支持六种模式  xlsx_content | xlsx_zip | xlsx_base64 | csv_content | csv_zip | csv_base64
biz_req.request.get('').dataframe()
```

### 4. 特性

```python
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

### 5. 拓展
```text
response.py  # 新增返回值类型
biz_requests.py  # 加入业务函数封装
```

### 7. 菜菜菜

```text
1, 原本想使用 `from hyper.contrib import HTTP20Adapter` 使得 requests 支持 http2 请求, 
   但是好像并不理想, 就放弃了

2, 可以试试通过适配器 加入简单的 tls/ja3 指纹算法
```

### 7. 完整demo 见demo.py
```text
菜菜菜
```