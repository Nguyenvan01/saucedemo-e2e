# ASSERTION BỔ SUNG:
# - poll_until : chờ một điều kiện không gắn với phần tử (vd localStorage) tới khi đúng
# - money      : "$29.99" / "Total: $32.39" -> Decimal (tính tiền không dùng float)
import re
import time
from decimal import Decimal

from config import WAIT_TIMEOUT

_MONEY = re.compile(r"\$(\d+(?:\.\d+)?)")


def poll_until(condition, message, timeout=WAIT_TIMEOUT, interval=0.1):
    """Gọi lại condition() tới khi trả truthy; hết timeout (giây) thì AssertionError."""
    deadline = time.monotonic() + timeout
    while True:
        value = condition()
        if value:
            return value
        if time.monotonic() >= deadline:
            raise AssertionError(f"{message} (sau {timeout}s)")
        time.sleep(interval)


def money(text):
    match = _MONEY.search(text or "")
    if not match:
        raise ValueError(f"Không đọc được số tiền trong {text!r}")
    return Decimal(match.group(1))
