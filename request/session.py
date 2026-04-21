# -*- coding: UTF-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Mapping, Optional, Tuple, Union, cast

from curl_cffi import requests as curl_requests
from curl_cffi.const import CurlHttpVersion
from curl_cffi.requests import Session as CurlSession

from .headers import Headers
from .params import MethodEnum, SessionParams
from .response import BizResponse

try:
    from ..tools.wrapper import Wrapper
except ImportError:
    from tools.wrapper import Wrapper

Timeout = Union[float, Tuple[float, float], object]
HeaderLike = Union[Headers, Mapping[str, str], Dict[str, str], None]


@dataclass
class SessionConfig:
    retries: int = field(default=0)
    delay: int = field(default=0)
    encoding: Optional[str] = field(default=None)
    headers: Dict[str, str] = field(default_factory=dict)
    http2: bool = field(default=False)
    impersonate: Optional[str] = field(default=None)
    ja3: Optional[str] = field(default=None)
    akamai: Optional[str] = field(default=None)
    extra_fp: Optional[Any] = field(default=None)
    default_headers: Optional[bool] = field(default=None)
    default_encoding: Union[str, Callable[[bytes], str]] = field(default="utf-8")

    def __post_init__(self) -> None:
        self.retries = int(self.retries or 0)
        self.delay = int(self.delay or 0)
        self.http2 = bool(self.http2 or False)
        self.headers = dict(self.headers or {})


class Session:
    def __init__(self, config: Optional[SessionConfig] = None):
        self.__config = config or SessionConfig()
        self._retries = self.__config.retries
        self._delay = self.__config.delay
        self.headers: Headers = Headers(self.__config.headers)
        self.session: Optional[CurlSession] = None
        self.reset_session()

    def reset_session(self, headers: Optional[Dict[str, str]] = None) -> None:
        if isinstance(self.session, CurlSession):
            self.session.close()

        self.session = curl_requests.Session()
        self.headers = Headers(headers or self.__config.headers)

    @property
    def exceptions(self) -> Any:
        return curl_requests.exceptions

    def close(self) -> None:
        if isinstance(self.session, CurlSession):
            self.session.close()

    def __enter__(self) -> "Session":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    @staticmethod
    def _method_value(method: Union[str, MethodEnum, None]) -> str:
        if isinstance(method, MethodEnum):
            return method.value
        if method is None:
            return "GET"
        return str(method).upper()

    @staticmethod
    def _headers_value(headers: HeaderLike) -> Optional[Dict[str, str]]:
        if headers is None:
            return None
        return dict(headers)

    def _params_to_kwargs(self, params: SessionParams) -> Dict[str, Any]:
        return {
            "method": self._method_value(params.method),
            "url": params.url,
            "params": params.params,
            "data": params.data,
            "headers": params.headers,
            "cookies": params.cookies,
            "timeout": params.timeout,
            "allow_redirects": params.allow_redirects,
            "proxies": params.proxies,
            "verify": params.verify,
            "json": params.json,
            "files": params.files,
            "auth": params.auth,
            "stream": params.stream,
            "cert": params.cert,
        }

    def __requests(
            self,
            method: Union[str, MethodEnum],
            url: str,
            params: Optional[Union[Dict[str, Any], bytes]] = None,
            data: Optional[Any] = None,
            headers: HeaderLike = None,
            cookies: Optional[Dict[str, str]] = None,
            timeout: Optional[Timeout] = None,
            allow_redirects: Optional[bool] = True,
            proxies: Optional[Dict[str, str]] = None,
            verify: Optional[Union[bool, str]] = None,
            json: Optional[Any] = None,
            encoding: Optional[str] = None,
            **kwargs: Any,
    ) -> BizResponse:
        if not isinstance(self.session, CurlSession):
            self.reset_session()

        http_version = kwargs.pop("http_version", None)
        if http_version is None and self.__config.http2:
            http_version = CurlHttpVersion.V2_0

        request_kwargs: Dict[str, Any] = {
            "method": self._method_value(method),
            "url": url,
            "params": params,
            "data": data,
            "json": json,
            "headers": self._headers_value(headers),
            "cookies": cookies,
            "timeout": timeout,
            "allow_redirects": allow_redirects,
            "proxies": proxies,
            "verify": verify,
            "impersonate": kwargs.pop("impersonate", self.__config.impersonate),
            "ja3": kwargs.pop("ja3", self.__config.ja3),
            "akamai": kwargs.pop("akamai", self.__config.akamai),
            "extra_fp": kwargs.pop("extra_fp", self.__config.extra_fp),
            "default_headers": kwargs.pop("default_headers", self.__config.default_headers),
            "default_encoding": kwargs.pop("default_encoding", self.__config.default_encoding),
            "http_version": http_version,
        }
        request_kwargs.update(kwargs)
        request_kwargs = {key: value for key, value in request_kwargs.items() if value is not None}

        response = cast(CurlSession, self.session).request(**request_kwargs)
        biz_response = BizResponse.from_response(response)
        response_encoding = encoding or self.__config.encoding
        if response_encoding:
            biz_response.set_encoding(response_encoding)
        return biz_response

    def request(
            self,
            method: Union[str, MethodEnum, SessionParams],
            url: Optional[str] = None,
            params: Optional[Union[Dict[str, Any], bytes]] = None,
            data: Optional[Any] = None,
            headers: HeaderLike = None,
            cookies: Optional[Dict[str, str]] = None,
            timeout: Optional[Timeout] = None,
            allow_redirects: Optional[bool] = True,
            proxies: Optional[Dict[str, str]] = None,
            verify: Optional[Union[bool, str]] = None,
            json: Optional[Any] = None,
            retries: int = 0,
            delay: int = 0,
            encoding: Optional[str] = None,
            **kwargs: Any,
    ) -> BizResponse:
        if isinstance(method, SessionParams):
            params_kwargs = self._params_to_kwargs(method)
            params_kwargs.update({k: v for k, v in kwargs.items() if v is not None})
            method = params_kwargs.pop("method")
            url = params_kwargs.pop("url")
            params = params if params is not None else params_kwargs.pop("params")
            data = data if data is not None else params_kwargs.pop("data")
            headers = headers if headers is not None else params_kwargs.pop("headers")
            cookies = cookies if cookies is not None else params_kwargs.pop("cookies")
            timeout = timeout if timeout is not None else params_kwargs.pop("timeout")
            allow_redirects = allow_redirects if allow_redirects is not None else params_kwargs.pop("allow_redirects")
            proxies = proxies if proxies is not None else params_kwargs.pop("proxies")
            verify = verify if verify is not None else params_kwargs.pop("verify")
            json = json if json is not None else params_kwargs.pop("json")
            kwargs.update({k: v for k, v in params_kwargs.items() if v is not None})

        if not isinstance(url, str) or not url:
            raise ValueError("url must be a non-empty string")

        retry_count = retries or self._retries
        retry_delay = delay or self._delay if retry_count else 0
        head = headers if headers is not None else self.headers
        req_wrap = self.__requests if retry_count == 0 else Wrapper.retry(retries=retry_count, delay=retry_delay)(self.__requests)
        return req_wrap(
            method, url, params, data, head, cookies, timeout, allow_redirects,
            proxies, verify, json, encoding, **kwargs,
        )

    def get(self, url: Union[str, SessionParams], params: Optional[Union[Dict[str, Any], bytes]] = None,
            data: Optional[Any] = None, headers: HeaderLike = None, cookies: Optional[Dict[str, str]] = None,
            timeout: Optional[Timeout] = None, allow_redirects: Optional[bool] = True,
            proxies: Optional[Dict[str, str]] = None, verify: Optional[Union[bool, str]] = None,
            json: Optional[Any] = None, retries: int = 0, delay: int = 0,
            encoding: Optional[str] = None, **kwargs: Any) -> BizResponse:
        if isinstance(url, SessionParams):
            return self.request(url, retries=retries, delay=delay, encoding=encoding, **kwargs)
        return self.request("get", url, params, data, headers, cookies, timeout, allow_redirects,
                            proxies, verify, json, retries, delay, encoding, **kwargs)

    def post(self, url: Union[str, SessionParams], params: Optional[Union[Dict[str, Any], bytes]] = None,
             data: Optional[Any] = None, headers: HeaderLike = None, cookies: Optional[Dict[str, str]] = None,
             timeout: Optional[Timeout] = None, allow_redirects: Optional[bool] = True,
             proxies: Optional[Dict[str, str]] = None, verify: Optional[Union[bool, str]] = None,
             json: Optional[Any] = None, retries: int = 0, delay: int = 0,
             encoding: Optional[str] = None, **kwargs: Any) -> BizResponse:
        if isinstance(url, SessionParams):
            return self.request(url, retries=retries, delay=delay, encoding=encoding, **kwargs)
        return self.request("post", url, params, data, headers, cookies, timeout, allow_redirects,
                            proxies, verify, json, retries, delay, encoding, **kwargs)

    def put(self, url: str, **kwargs: Any) -> BizResponse:
        return self.request("put", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> BizResponse:
        return self.request("delete", url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> BizResponse:
        return self.request("patch", url, **kwargs)

    def head(self, url: str, **kwargs: Any) -> BizResponse:
        return self.request("head", url, **kwargs)

    def options(self, url: str, **kwargs: Any) -> BizResponse:
        return self.request("options", url, **kwargs)
