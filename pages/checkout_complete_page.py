# Trang /checkout-complete.html - đặt hàng thành công.
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    path = "/checkout-complete.html"

    def __init__(self, page):
        super().__init__(page)
        self.header = page.get_by_test_id("complete-header")
        self.text = page.get_by_test_id("complete-text")
        self.back_home = page.get_by_test_id("back-to-products")
