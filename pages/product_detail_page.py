# Trang /inventory-item.html?id=N - chi tiết 1 sản phẩm.
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    path = "/inventory-item.html"

    def __init__(self, page):
        super().__init__(page)
        self.name = page.get_by_test_id("inventory-item-name")
        self.description = page.get_by_test_id("inventory-item-desc")
        self.price = page.get_by_test_id("inventory-item-price")
        self.add_button = page.get_by_test_id("add-to-cart")
        self.remove_button = page.get_by_test_id("remove")
        self.back_button = page.get_by_test_id("back-to-products")
