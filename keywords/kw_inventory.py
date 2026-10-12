# THƯ VIỆN KEYWORD - NHÓM inventory: danh sách sản phẩm, sắp xếp, thêm/bỏ giỏ từ danh sách.
from playwright.sync_api import expect

from keywords.base_keywords import BaseKeywords, keyword


class InventoryKeywords(BaseKeywords):
    group = "inventory"

    @keyword("openInventory")
    def open_inventory(self):
        """Mở trang danh sách sản phẩm (cần phiên đăng nhập)."""
        with self.step("Mở trang danh sách sản phẩm"):
            self.po.inventory.goto()
            expect(self.po.inventory.list).to_be_visible()

    @keyword("verifyProductCount")
    def verify_product_count(self, count):
        """Kiểm tra số sản phẩm hiển thị."""
        with self.step(f"Kiểm tra có {count} sản phẩm"):
            expect(self.po.inventory.items).to_have_count(int(count))

    @keyword("verifyProductNames")
    def verify_product_names(self, names):
        """Kiểm tra tên sản phẩm theo ĐÚNG thứ tự hiển thị."""
        with self.step(f"Kiểm tra thứ tự tên sản phẩm: {names}"):
            expect(self.po.inventory.names).to_have_text(names)

    @keyword("verifyProductPrices")
    def verify_product_prices(self, prices):
        """Kiểm tra giá sản phẩm theo đúng thứ tự hiển thị, vd ["$7.99", "$9.99"]."""
        with self.step(f"Kiểm tra thứ tự giá: {prices}"):
            expect(self.po.inventory.prices).to_have_text(prices)

    @keyword("verifyProductPrice")
    def verify_product_price(self, name, price):
        """Kiểm tra giá của 1 sản phẩm trên danh sách."""
        with self.step(f'Kiểm tra giá "{name}" = {price}'):
            expect(self.po.inventory.price_of(name)).to_have_text(price)

    @keyword("sortProductsBy")
    def sort_products_by(self, label):
        """Chọn kiểu sắp xếp theo nhãn, vd "Price (low to high)"."""
        with self.step(f'Sắp xếp theo "{label}"'):
            self.po.inventory.sort_select.select_option(label=label)

    @keyword("verifyActiveSort")
    def verify_active_sort(self, label):
        """Kiểm tra nhãn kiểu sắp xếp đang chọn."""
        with self.step(f'Kiểm tra đang sắp xếp theo "{label}"'):
            expect(self.po.inventory.active_sort).to_have_text(label)

    @keyword("addProductToCart")
    def add_product_to_cart(self, name):
        """Bấm "Add to cart" của 1 sản phẩm trên danh sách."""
        with self.step(f'Thêm "{name}" vào giỏ'):
            self.po.inventory.add_button(name).click()

    @keyword("addProductsToCart")
    def add_products_to_cart(self, names):
        """Bấm "Add to cart" lần lượt cho nhiều sản phẩm."""
        with self.step(f"Thêm {len(names)} sản phẩm vào giỏ"):
            for name in names:
                self.po.inventory.add_button(name).click()

    @keyword("removeProductFromInventory")
    def remove_product_from_inventory(self, name):
        """Bấm "Remove" của 1 sản phẩm ngay trên danh sách."""
        with self.step(f'Bỏ "{name}" khỏi giỏ từ danh sách'):
            self.po.inventory.remove_button(name).click()

    @keyword("verifyProductButtonState")
    def verify_product_button_state(self, name, text):
        """Kiểm tra nút của sản phẩm đang là "Add to cart" hay "Remove"."""
        with self.step(f'Kiểm tra nút của "{name}" là "{text}"'):
            expect(self.po.inventory.button_of(name)).to_have_text(text)

    @keyword("openProductDetail")
    def open_product_detail(self, name):
        """Bấm tên sản phẩm để mở trang chi tiết."""
        with self.step(f'Mở chi tiết "{name}"'):
            self.po.inventory.name_of(name).click()
            expect(self.po.product.back_button).to_be_visible()
