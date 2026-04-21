# -*- coding: UTF-8 -*-
from __future__ import annotations

try:
    from .core import BizRequest
    from .db_engine.engine import Engine
    from .request.headers import Headers
    from .request.session import Session
    from .tools.cookies import CookieTools
    from .tools.wrapper import Wrapper
except ImportError:
    import sys
    from pathlib import Path

    package_parent = Path(__file__).resolve().parent.parent
    if str(package_parent) not in sys.path:
        sys.path.insert(0, str(package_parent))

    from biz_requests.core import BizRequest
    from biz_requests.db_engine.engine import Engine
    from biz_requests.request.headers import Headers
    from biz_requests.request.session import Session
    from biz_requests.tools.cookies import CookieTools
    from biz_requests.tools.wrapper import Wrapper

__all__ = ["BizRequest", "Session", "Headers", "Engine", "Wrapper", "CookieTools"]
