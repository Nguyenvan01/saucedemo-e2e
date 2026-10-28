# Header của mọi trang sau đăng nhập: icon giỏ + badge số lượng.
from pages.base_page import BasePage, by_test, step
from pages.cart_page import CartPage


class Header(BasePage):
    CART_LINK = by_test("shopping-cart-link")
    CART_BADGE = by_test("shopping-cart-badge")
    landmark = CART_LINK

    def cart_badge(self):
        """Số trên icon giỏ; 0 nếu không hiện badge."""
        badges = self.find_all(self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    @step("Mở giỏ hàng")
    def open_cart(self):
        self.click(self.CART_LINK)
        return CartPage(self.driver).wait_loaded()
