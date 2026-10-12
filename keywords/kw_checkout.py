# THƯ VIỆN KEYWORD - NHÓM checkout: thông tin người nhận, xem lại đơn, hoàn tất.
from playwright.sync_api import expect

from keywords.base_keywords import BaseKeywords, keyword
from utils.assertions import money


class CheckoutKeywords(BaseKeywords):
    group = "checkout"

    @keyword("fillCheckoutInfo")
    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Nhập First Name, Last Name, Zip/Postal Code."""
        with self.step(f'Nhập thông tin "{first_name}" / "{last_name}" / "{postal_code}"'):
            self.po.checkout_info.fill(first_name, last_name, postal_code)

    @keyword("continueCheckout")
    def continue_checkout(self):
        """Bấm "Continue" ở bước thông tin người nhận."""
        with self.step("Bấm Continue"):
            self.po.checkout_info.continue_button.click()

    @keyword("continueCheckoutExpectingError")
    def continue_checkout_expecting_error(self, first_name, last_name, postal_code, message):
        """Nhập thông tin, bấm Continue và chờ lỗi đúng nguyên văn, vẫn ở bước 1."""
        with self.step(f'Continue với thông tin thiếu, chờ lỗi "{message}"'):
            self.po.checkout_info.fill(first_name, last_name, postal_code)
            self.po.checkout_info.continue_button.click()
            expect(self.po.checkout_info.error).to_have_text(message)
            expect(self.po.checkout_info.first_name).to_be_visible()

    @keyword("verifyOverviewItems")
    def verify_overview_items(self, names):
        """Kiểm tra tên sản phẩm ở trang xem lại đơn theo thứ tự."""
        with self.step(f"Kiểm tra đơn có: {names}"):
            expect(self.po.checkout_overview.names).to_have_text(names)

    @keyword("verifyItemTotal")
    def verify_item_total(self, amount):
        """Kiểm tra dòng "Item total" bằng số tiền cho trước, vd "$39.98"."""
        with self.step(f"Kiểm tra Item total = {amount}"):
            expect(self.po.checkout_overview.subtotal).to_have_text(f"Item total: {amount}")

    @keyword("verifyItemTotalEqualsSum")
    def verify_item_total_equals_sum(self):
        """Kiểm tra Item total = tổng giá các sản phẩm trong đơn."""
        with self.step("Kiểm tra Item total = tổng giá sản phẩm"):
            overview = self.po.checkout_overview
            expect(overview.subtotal).to_be_visible()
            prices = [money(text) for text in overview.prices.all_inner_texts()]
            item_total = money(overview.subtotal.inner_text())
            assert item_total == sum(prices), f"Item total {item_total} != tổng giá {prices}"

    @keyword("verifyTotalEqualsItemTotalPlusTax")
    def verify_total_equals_item_total_plus_tax(self):
        """Kiểm tra Total = Item total + Tax."""
        with self.step("Kiểm tra Total = Item total + Tax"):
            overview = self.po.checkout_overview
            expect(overview.total).to_be_visible()
            item_total, tax, total = (money(x.inner_text()) for x in (overview.subtotal, overview.tax, overview.total))
            assert total == item_total + tax, f"Total {total} != Item total {item_total} + Tax {tax}"

    @keyword("finishCheckout")
    def finish_checkout(self):
        """Bấm "Finish" ở trang xem lại đơn."""
        with self.step("Bấm Finish"):
            self.po.checkout_overview.finish_button.click()

    @keyword("verifyOrderComplete")
    def verify_order_complete(self, header, text):
        """Kiểm tra trang hoàn tất hiện đúng tiêu đề và nội dung cảm ơn."""
        with self.step(f'Kiểm tra đặt hàng thành công "{header}"'):
            expect(self.po.checkout_complete.header).to_have_text(header)
            expect(self.po.checkout_complete.text).to_have_text(text)

    @keyword("cancelCheckout")
    def cancel_checkout(self):
        """Bấm "Cancel" ở bước checkout hiện tại (bước 1 hoặc 2)."""
        with self.step("Bấm Cancel"):
            self.po.checkout_info.cancel_button.click()

    @keyword("backHome")
    def back_home(self):
        """Bấm "Back Home" ở trang hoàn tất và chờ danh sách sản phẩm."""
        with self.step("Về trang danh sách sản phẩm"):
            self.po.checkout_complete.back_home.click()
            expect(self.po.inventory.list).to_be_visible()
