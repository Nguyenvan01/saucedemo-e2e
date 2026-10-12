# THƯ VIỆN KEYWORD - NHÓM cart: trang giỏ hàng.
from playwright.sync_api import expect

from keywords.base_keywords import BaseKeywords, keyword


class CartKeywords(BaseKeywords):
    group = "cart"

    @keyword("openCart")
    def open_cart(self):
        """Bấm icon giỏ trên header và chờ trang giỏ hàng."""
        with self.step("Mở giỏ hàng"):
            self.po.header.cart_link.click()
            expect(self.po.cart.list).to_be_visible()

    @keyword("verifyCartItems")
    def verify_cart_items(self, names):
        """Kiểm tra tên sản phẩm trong giỏ theo thứ tự; [] = giỏ trống."""
        with self.step(f"Kiểm tra giỏ có: {names}"):
            if names:
                expect(self.po.cart.names).to_have_text(names)
            else:
                expect(self.po.cart.items).to_have_count(0)

    @keyword("removeFromCart")
    def remove_from_cart(self, name):
        """Bấm "Remove" của 1 sản phẩm trong giỏ."""
        with self.step(f'Xoá "{name}" khỏi giỏ'):
            self.po.cart.remove_button(name).click()

    @keyword("continueShopping")
    def continue_shopping(self):
        """Bấm "Continue Shopping" và chờ danh sách sản phẩm."""
        with self.step("Tiếp tục mua sắm"):
            self.po.cart.continue_shopping.click()
            expect(self.po.inventory.list).to_be_visible()

    @keyword("proceedToCheckout")
    def proceed_to_checkout(self):
        """Bấm "Checkout" và chờ form thông tin người nhận."""
        with self.step("Sang bước checkout"):
            self.po.cart.checkout_button.click()
            expect(self.po.checkout_info.first_name).to_be_visible()
