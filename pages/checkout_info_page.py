# Trang /checkout-step-one.html - nhập thông tin người nhận.
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.cancel_button = page.get_by_test_id("cancel")

    def fill(self, first_name, last_name, postal_code):
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
