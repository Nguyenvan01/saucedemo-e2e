# Header của mọi trang sau đăng nhập: icon giỏ + badge số lượng.
class Header:
    def __init__(self, page):
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
