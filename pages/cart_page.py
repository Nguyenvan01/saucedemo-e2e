# Trang /cart.html - giỏ hàng.
from pages.base_page import BasePage, by_test, slug, step
from pages.checkout_info_page import CheckoutInfoPage
from pages.inventory_page import InventoryPage


class CartPage(BasePage):
    path = "/cart.html"
    LIST = by_test("cart-list")
    ITEMS = by_test("inventory-item")
    NAMES = by_test("inventory-item-name")
    CONTINUE_SHOPPING = by_test("continue-shopping")
    CHECKOUT_BUTTON = by_test("checkout")
    landmark = LIST

    def names(self):
        return self.texts(self.NAMES)

    @step('Xoá "{name}" khỏi giỏ')
    def remove(self, name):
        self.click(by_test(f"remove-{slug(name)}"))

    @step("Tiếp tục mua sắm")
    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)
        return InventoryPage(self.driver).wait_loaded()

    @step("Sang bước checkout")
    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutInfoPage(self.driver).wait_loaded()
