# BizRequests
面向工作的requests封装

## 新增方法

```python
from biz_request import BizRequest

# 注意, 该类只能继承使用
biz_req = BizRequest()
biz_req.init_engine(**{
    # 初始化数据库
}).init_request(**{
    # 初始化请求
})

# 错误日志打印
# 以下几个方法执行报错的时候会自动日志输出 biz_req.text

biz_req.request.get('', headers={}).json()
biz_req.request.get('', headers={}).jsonp2json()
biz_req.request.get('', headers={}).dataframe()

# 这两个不会有报错日志
biz_req.request.get('', headers={}).set_encoding()  # 设置响应编码, 并返回self
biz_req.request.get('', headers={}).resp_cookie()  # 获取到response.set_cookie
```
