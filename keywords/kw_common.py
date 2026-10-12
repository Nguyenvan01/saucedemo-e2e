# THƯ VIỆN KEYWORD - NHÓM common: điều hướng, URL, tiêu đề trang, khung lỗi, badge giỏ, localStorage.
from playwright.sync_api import expect

from config import BASE_URL
from keywords.base_keywords import BaseKeywords, keyword
from utils.assertions import poll_until
from utils.storage import read_cart


class CommonKeywords(BaseKeywords):
    group = "common"

    @keyword("openPage")
    def open_page(self, path):
        """Mở trang theo đường dẫn tương đối, vd "/cart.html"."""
        with self.step(f'Mở trang "{path}"'):
            self.page.goto(path)

    @keyword("reloadPage")
    def reload_page(self):
        """Tải lại trang hiện tại."""
        with self.step("Tải lại trang"):
            self.page.reload()

    @keyword("verifyUrl")
    def verify_url(self, path):
        """Kiểm tra URL hiện tại đúng bằng BASE_URL + path."""
        with self.step(f'Kiểm tra URL là "{path}"'):
            expect(self.page).to_have_url(BASE_URL + path)

    @keyword("verifyPageTitle")
    def verify_page_title(self, title):
        """Kiểm tra tiêu đề trang (data-test="title"), vd "Your Cart"."""
        with self.step(f'Kiểm tra tiêu đề trang "{title}"'):
            expect(self.po.base.title).to_have_text(title)

    @keyword("verifyErrorMessage")
    def verify_error_message(self, message):
        """Kiểm tra khung lỗi (login / checkout) hiện đúng nguyên văn thông báo."""
        with self.step(f'Kiểm tra thông báo lỗi "{message}"'):
            expect(self.po.base.error).to_have_text(message)

    @keyword("verifyNoErrorMessage")
    def verify_no_error_message(self):
        """Kiểm tra không còn khung lỗi trên trang."""
        with self.step("Kiểm tra không có thông báo lỗi"):
            expect(self.po.base.error).to_have_count(0)

    @keyword("verifyCartBadge")
    def verify_cart_badge(self, count):
        """Kiểm tra số trên icon giỏ; 0 = không hiện badge."""
        with self.step(f"Kiểm tra badge giỏ = {count}"):
            if int(count) == 0:
                expect(self.po.header.cart_badge).to_have_count(0)
            else:
                expect(self.po.header.cart_badge).to_have_text(str(count))

    @keyword("verifyCartStorage")
    def verify_cart_storage(self, product_ids):
        """Kiểm tra localStorage "cart-contents" chứa đúng các id sản phẩm (không xét thứ tự)."""
        with self.step(f"Kiểm tra localStorage giỏ = {product_ids}"):
            expected = sorted(int(i) for i in product_ids)
            poll_until(
                self.page,
                lambda: sorted(read_cart(self.page)) == expected,
                f"cart-contents khác {expected}: {read_cart(self.page)}",
            )
