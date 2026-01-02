import base64
from typing import Any


def encode_cursor(value: Any) -> str:
    if value is None:
        return ""
    return base64.b64encode(str(value).encode("utf-8")).decode("utf-8")


def decode_cursor(cursor: str | None) -> str | None:
    if not cursor:
        return None
    try:
        return base64.b64decode(cursor).decode("utf-8")
    except (ValueError, TypeError, UnicodeDecodeError):
        return None
