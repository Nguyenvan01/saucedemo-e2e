# ASSERTION BỔ SUNG: những gì Playwright Python chưa có sẵn.
# - poll_until ~ expect.poll(...).toBe(true)
# - money      : "$29.99" / "Total: $32.39" -> Decimal (tính tiền không dùng float)
import re
import time
from decimal import Decimal

from config import EXPECT_TIMEOUT

_MONEY = re.compile(r"\$(\d+(?:\.\d+)?)")


def poll_until(page, condition, message, timeout=EXPECT_TIMEOUT, interval=100):
    """Gọi lại condition() tới khi trả truthy; hết timeout (ms) thì AssertionError.
    Chờ bằng page.wait_for_timeout để Playwright vẫn xử lý sự kiện trong lúc poll."""
    deadline = time.monotonic() + timeout / 1000
    while True:
        value = condition()
        if value:
            return value
        if time.monotonic() >= deadline:
            raise AssertionError(f"{message} (sau {timeout}ms)")
        page.wait_for_timeout(interval)


def money(text):
    match = _MONEY.search(text or "")
    if not match:
        raise ValueError(f"Không đọc được số tiền trong {text!r}")
    return Decimal(match.group(1))
