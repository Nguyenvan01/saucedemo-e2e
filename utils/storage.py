# STORAGE: localStorage (giỏ hàng) và storageState (cookie phiên) của saucedemo.
import json
import os
import time

# Phiên đăng nhập = cookie; giỏ hàng = localStorage (mảng JSON id sản phẩm, vd "[4,0]").
STORAGE_KEYS = {"session": "session-username", "cart": "cart-contents"}


def write_storage_state(file, state):
    """Ghi storageState ra file tạm rồi đổi tên: nhiều worker xdist ghi cùng lúc không làm hỏng file."""
    file.parent.mkdir(parents=True, exist_ok=True)
    tmp = file.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, file)


def session_seconds_left(file, now=None):
    """Số giây còn lại của cookie phiên trong file storageState; 0 nếu không có/hỏng."""
    try:
        state = json.loads(file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return 0
    expires = [c.get("expires", -1) for c in state.get("cookies", []) if c.get("name") == STORAGE_KEYS["session"]]
    if not expires:
        return 0
    return max(0, expires[0] - (time.time() if now is None else now))


def read_cart(page):
    """Danh sách id sản phẩm trong giỏ (localStorage)."""
    return page.evaluate("key => JSON.parse(localStorage.getItem(key) || '[]')", STORAGE_KEYS["cart"])
