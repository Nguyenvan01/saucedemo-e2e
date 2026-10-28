# Trang /checkout-step-two.html - xem lại đơn và tổng tiền.
from pages.base_page import BasePage, by_test, step
from utils.assertions import money


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"
    NAMES = by_test("inventory-item-name")
    PRICES = by_test("inventory-item-price")
    SUBTOTAL = by_test("subtotal-label")
    TAX = by_test("tax-label")
    TOTAL = by_test("total-label")
    FINISH_BUTTON = by_test("finish")
    CANCEL_BUTTON = by_test("cancel")
    landmark = TOTAL

    def names(self):
        return self.texts(self.NAMES)

    def subtotal_text(self):
        return self.text(self.SUBTOTAL)

    def amounts(self):
        """Số tiền trên trang (Decimal): giá từng sản phẩm, Item total, Tax, Total."""
        self.wait_loaded()
        return {
            "prices": [money(text) for text in self.texts(self.PRICES)],
            "itemTotal": money(self.text(self.SUBTOTAL)),
            "tax": money(self.text(self.TAX)),
            "total": money(self.text(self.TOTAL)),
        }

    @step("Bấm Finish")
    def finish(self):
        self.click(self.FINISH_BUTTON)

    @step("Bấm Cancel")
    def cancel(self):
        self.click(self.CANCEL_BUTTON)
