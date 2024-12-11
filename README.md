# BizRequests
面向工作的requests封装

## 新增方法

```python
from biz_request import BizRequest


# 注意, 该类只能继承使用

class Demo(BizRequest):
    def __init__(self):
        super(Demo, self).__init__()
        self.set_request(
            # 初始化请求
        ).set_engine(
            # 初始化数据库
        )

    def demo(self):
        # 错误日志打印
        # 以下几个方法执行报错的时候会自动日志输出 biz_req.text
        self.request.get('', headers={}).json()
        self.request.get('', headers={}).jsonp2json()
        self.request.get('', headers={}).dataframe(c_type='xlsx_content')  # 返回 pd.Dataframe 类型

        # 这两个不会有报错日志
        req = self.request.get('', headers={})
        req.set_encoding()  # 设置响应编码, 并重新获取
        req.set_encoding('utf-8').json()
        req.set_encoding('utf-8').text

        self.request.get('', headers={}).resp_cookie()  # 获取到response.set_cookie
```
