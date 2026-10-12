# Trang /inventory.html - danh sách 6 sản phẩm, sắp xếp, thêm/bỏ giỏ.
import re

from pages.base_page import BasePage, slug


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.list = page.get_by_test_id("inventory-list")
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.prices = page.get_by_test_id("inventory-item-price")
        self.sort_select = page.get_by_test_id("product-sort-container")
        self.active_sort = page.get_by_test_id("active-option")

    def item(self, name):
        exact = self.page.get_by_test_id("inventory-item-name").filter(has_text=re.compile(f"^{re.escape(name)}$"))
        return self.items.filter(has=exact)

    def name_of(self, name):
        return self.item(name).get_by_test_id("inventory-item-name")

    def price_of(self, name):
        return self.item(name).get_by_test_id("inventory-item-price")

    def button_of(self, name):
        """Nút của item ở trạng thái bất kỳ: data-test "add-to-cart-<slug>" hoặc "remove-<slug>"."""
        return self.page.get_by_test_id(re.compile(f"^(add-to-cart|remove)-{re.escape(slug(name))}$"))

    def add_button(self, name):
        return self.page.get_by_test_id(f"add-to-cart-{slug(name)}")

    def remove_button(self, name):
        return self.page.get_by_test_id(f"remove-{slug(name)}")
