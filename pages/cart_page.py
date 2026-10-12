# Trang /cart.html - giỏ hàng.
from pages.base_page import BasePage, slug


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.list = page.get_by_test_id("cart-list")
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.continue_shopping = page.get_by_test_id("continue-shopping")
        self.checkout_button = page.get_by_test_id("checkout")

    def remove_button(self, name):
        return self.page.get_by_test_id(f"remove-{slug(name)}")
