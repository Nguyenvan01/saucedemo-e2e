# THƯ VIỆN KEYWORD - NHÓM product: trang chi tiết sản phẩm.
from playwright.sync_api import expect

from keywords.base_keywords import BaseKeywords, keyword
from utils.routes import product_route


class ProductKeywords(BaseKeywords):
    group = "product"

    @keyword("openProductById")
    def open_product_by_id(self, product_id):
        """Mở thẳng trang chi tiết /inventory-item.html?id=N."""
        with self.step(f"Mở chi tiết sản phẩm id={product_id}"):
            self.page.goto(product_route(product_id))
            expect(self.po.product.back_button).to_be_visible()

    @keyword("verifyProductDetail")
    def verify_product_detail(self, name, price):
        """Kiểm tra tên và giá trên trang chi tiết."""
        with self.step(f'Kiểm tra chi tiết "{name}" giá {price}'):
            expect(self.po.product.name).to_have_text(name)
            expect(self.po.product.price).to_have_text(price)

    @keyword("addToCartFromDetail")
    def add_to_cart_from_detail(self):
        """Bấm "Add to cart" trên trang chi tiết."""
        with self.step("Thêm vào giỏ từ trang chi tiết"):
            self.po.product.add_button.click()

    @keyword("removeFromDetail")
    def remove_from_detail(self):
        """Bấm "Remove" trên trang chi tiết."""
        with self.step("Bỏ khỏi giỏ từ trang chi tiết"):
            self.po.product.remove_button.click()

    @keyword("backToProducts")
    def back_to_products(self):
        """Bấm "Back to products" và chờ danh sách sản phẩm."""
        with self.step("Quay lại danh sách sản phẩm"):
            self.po.product.back_button.click()
            expect(self.po.inventory.list).to_be_visible()
