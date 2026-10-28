# Trang /inventory.html - danh sách 6 sản phẩm, sắp xếp, thêm/bỏ giỏ.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, by_test, slug, step


class InventoryPage(BasePage):
    path = "/inventory.html"
    LIST = by_test("inventory-list")
    ITEMS = by_test("inventory-item")
    NAMES = by_test("inventory-item-name")
    PRICES = by_test("inventory-item-price")
    SORT_SELECT = by_test("product-sort-container")
    ACTIVE_SORT = by_test("active-option")
    landmark = LIST

    def names(self):
        return self.texts(self.NAMES)

    def prices(self):
        return self.texts(self.PRICES)

    def product_count(self):
        return self.count(self.ITEMS)

    def _item(self, name):
        """Thẻ sản phẩm có tên đúng nguyên văn `name`."""
        self.wait_loaded()
        for item in self.find_all(self.ITEMS):
            if item.find_element(*self.NAMES).text == name:
                return item
        raise ValueError(f"Không có sản phẩm {name!r} trên danh sách")

    def price_of(self, name):
        return self._item(name).find_element(*self.PRICES).text

    def button_text(self, name):
        """Nhãn nút của sản phẩm: "Add to cart" hoặc "Remove"."""
        s = slug(name)
        return self.text((By.CSS_SELECTOR, f'[data-test="add-to-cart-{s}"], [data-test="remove-{s}"]'))

    @step('Sắp xếp theo "{label}"')
    def sort_by(self, label):
        Select(self.find(self.SORT_SELECT)).select_by_visible_text(label)

    def active_sort(self):
        return self.text(self.ACTIVE_SORT)

    @step('Thêm "{name}" vào giỏ')
    def add_to_cart(self, name):
        self.click(by_test(f"add-to-cart-{slug(name)}"))

    def add_all_to_cart(self, names):
        for name in names:
            self.add_to_cart(name)

    @step('Bỏ "{name}" khỏi giỏ từ danh sách')
    def remove_from_cart(self, name):
        self.click(by_test(f"remove-{slug(name)}"))

    @step('Mở chi tiết "{name}"')
    def open_product(self, name):
        self._item(name).find_element(*self.NAMES).click()
        from pages.product_detail_page import ProductDetailPage  # import vòng: trang chi tiết quay về danh sách

        return ProductDetailPage(self.driver).wait_loaded()
