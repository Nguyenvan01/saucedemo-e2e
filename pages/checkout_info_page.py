# Trang /checkout-step-one.html - nhập thông tin người nhận.
from pages.base_page import BasePage, by_test, step


class CheckoutInfoPage(BasePage):
    path = "/checkout-step-one.html"
    FIRST_NAME = by_test("firstName")
    LAST_NAME = by_test("lastName")
    POSTAL_CODE = by_test("postalCode")
    CONTINUE_BUTTON = by_test("continue")
    CANCEL_BUTTON = by_test("cancel")
    landmark = FIRST_NAME

    @step('Nhập thông tin "{first_name}" / "{last_name}" / "{postal_code}"')
    def fill(self, first_name, last_name, postal_code):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)

    @step("Bấm Continue")
    def submit(self):
        self.click(self.CONTINUE_BUTTON)

    @step("Bấm Cancel")
    def cancel(self):
        self.click(self.CANCEL_BUTTON)
