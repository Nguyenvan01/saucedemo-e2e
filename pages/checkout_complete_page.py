# Trang /checkout-complete.html - đặt hàng thành công.
from pages.base_page import BasePage, by_test, step
from pages.inventory_page import InventoryPage


class CheckoutCompletePage(BasePage):
    path = "/checkout-complete.html"
    HEADER = by_test("complete-header")
    TEXT = by_test("complete-text")
    BACK_HOME = by_test("back-to-products")
    landmark = HEADER

    def header(self):
        return self.text(self.HEADER)

    def message(self):
        return self.text(self.TEXT)

    @step("Về trang danh sách sản phẩm")
    def back_home(self):
        self.click(self.BACK_HOME)
        return InventoryPage(self.driver).wait_loaded()
