# Trang /checkout-step-two.html - xem lại đơn và tổng tiền.
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"

    def __init__(self, page):
        super().__init__(page)
        self.names = page.get_by_test_id("inventory-item-name")
        self.prices = page.get_by_test_id("inventory-item-price")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")
        self.cancel_button = page.get_by_test_id("cancel")
