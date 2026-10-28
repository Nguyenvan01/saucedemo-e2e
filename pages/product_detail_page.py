# Trang /inventory-item.html?id=N - chi tiết 1 sản phẩm.
from pages.base_page import BasePage, by_test, step
from pages.inventory_page import InventoryPage
from utils.routes import product_route


class ProductDetailPage(BasePage):
    path = "/inventory-item.html"
    NAME = by_test("inventory-item-name")
    DESCRIPTION = by_test("inventory-item-desc")
    PRICE = by_test("inventory-item-price")
    ADD_BUTTON = by_test("add-to-cart")
    REMOVE_BUTTON = by_test("remove")
    BACK_BUTTON = by_test("back-to-products")
    landmark = BACK_BUTTON

    @step("Mở chi tiết sản phẩm id={product_id}")
    def open_by_id(self, product_id):
        return self.open(product_route(product_id))

    def name(self):
        return self.text(self.NAME)

    def price(self):
        return self.text(self.PRICE)

    @step("Thêm vào giỏ từ trang chi tiết")
    def add_to_cart(self):
        self.click(self.ADD_BUTTON)

    @step("Bỏ khỏi giỏ từ trang chi tiết")
    def remove_from_cart(self):
        self.click(self.REMOVE_BUTTON)

    @step("Quay lại danh sách sản phẩm")
    def back_to_products(self):
        self.click(self.BACK_BUTTON)
        return InventoryPage(self.driver).wait_loaded()
