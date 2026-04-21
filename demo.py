# -*- coding: UTF-8 -*-
from __future__ import annotations

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from biz_requests import BizRequest, Headers, Session
from biz_requests.request.params import MethodEnum, SessionParams
from biz_requests.request.response import BizResponse


class DemoRequest(BizRequest):
    def __init__(self) -> None:
        super().__init__()
        self.init_request(
            retries=1,
            delay=0,
            headers={"x-demo": "biz_requests"},
            http2=True,
            impersonate="chrome",
        )


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path.startswith("/jsonp"):
            self._send_text('callback({"ok": true, "type": "jsonp"})')
            return

        self._send_json({
            "ok": True,
            "method": "GET",
            "path": self.path,
            "x_demo": self.headers.get("x-demo"),
        })

    def do_POST(self) -> None:
        length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(length) if length else b""
        self._send_json({
            "ok": True,
            "method": "POST",
            "body": body.decode("utf-8"),
        })

    def log_message(self, *_args: Any) -> None:
        pass

    def _send_json(self, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Set-Cookie", "token=abc; Path=/; HttpOnly")
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/javascript; charset=utf-8")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))


def start_server() -> Tuple[HTTPServer, str]:
    server = HTTPServer(("127.0.0.1", 0), DemoHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_port}"


def assert_equal(actual: Any, expected: Any, name: str) -> None:
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")


def demo() -> None:
    server, base_url = start_server()
    biz = DemoRequest()
    request = biz.request
    assert isinstance(request, Session)

    get_resp = request.get(f"{base_url}/json", timeout=5)
    assert isinstance(get_resp, BizResponse)
    assert_equal(get_resp.status_code, 200, "GET status_code")
    assert_equal(get_resp.json()["x_demo"], "biz_requests", "default headers")
    assert_equal(get_resp.head_scookie(), {"token": "abc"}, "head_scookie")

    post_resp = request.post(f"{base_url}/submit", json={"name": "curl_cffi"}, timeout=5)
    assert_equal(post_resp.json()["method"], "POST", "POST method")

    params_resp = request.request(SessionParams(
        method=MethodEnum.GET,
        url=f"{base_url}/params?keyword=test",
        headers={"x-demo": "session-params"},
        timeout=5,
    ))
    assert_equal(params_resp.json()["x_demo"], "session-params", "SessionParams headers")

    jsonp_resp = request.get(f"{base_url}/jsonp", timeout=5)
    assert_equal(jsonp_resp.jsonp()["type"], "jsonp", "jsonp parser")

    retry_state = {"count": 0}

    def eventually_done() -> str | None:
        retry_state["count"] += 1
        return "done" if retry_state["count"] == 2 else None

    assert_equal(
        biz.safe_retry_until_done(eventually_done, retries=3, delay=0),
        "done",
        "safe_retry_until_done",
    )

    headers = Headers({"Cookie": "a=1; b=2"})
    assert_equal(headers["cookie"], "a=1; b=2", "Headers case insensitive")
    assert_equal(headers.cookie(as_dict=True), {"a": "1", "b": "2"}, "Headers.cookie")

    print("All demo tests passed.")
    print(f"GET: {get_resp.json()}")
    print(f"POST: {post_resp.json()}")
    print(f"JSONP: {jsonp_resp.jsonp()}")


if __name__ == "__main__":
    demo()
