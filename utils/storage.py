# STORAGE: localStorage (giỏ hàng) và cookie phiên của saucedemo.
import time

# Phiên đăng nhập = cookie; giỏ hàng = localStorage (mảng JSON id sản phẩm, vd "[4,0]").
STORAGE_KEYS = {"session": "session-username", "cart": "cart-contents"}


def session_seconds_left(cookie, now=None):
    """Số giây còn lại của cookie phiên (dict theo định dạng Selenium get_cookie); 0 nếu không có."""
    if not cookie or "expiry" not in cookie:
        return 0
    return max(0, cookie["expiry"] - (time.time() if now is None else now))


def read_cart(driver):
    """Danh sách id sản phẩm trong giỏ (localStorage)."""
    return driver.execute_script("return JSON.parse(localStorage.getItem(arguments[0]) || '[]')", STORAGE_KEYS["cart"])
