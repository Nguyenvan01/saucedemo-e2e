# THƯ VIỆN KEYWORD - NHÓM auth: đăng nhập, thông báo lỗi đăng nhập, trạng thái đã đăng nhập.
import re

from playwright.sync_api import expect

from config import PASSWORD
from keywords.base_keywords import BaseKeywords, keyword


class AuthKeywords(BaseKeywords):
    group = "auth"

    @keyword("openLogin")
    def open_login(self):
        """Mở trang đăng nhập."""
        with self.step("Mở trang đăng nhập"):
            self.po.login.goto()
            expect(self.po.login.login_button).to_be_visible()

    @keyword("login")
    def login(self, username, password):
        """Nhập username + mật khẩu và bấm Login (không chờ kết quả)."""
        with self.step(f'Đăng nhập với "{username}"'):
            self.po.login.login(username, password)

    @keyword("loginAs")
    def login_as(self, username):
        """Đăng nhập bằng mật khẩu chung trong .env và chờ danh sách sản phẩm hiện ra."""
        with self.step(f'Đăng nhập "{username}" bằng mật khẩu trong .env'):
            assert PASSWORD, "Chưa cấu hình SAUCE_PASSWORD trong .env"
            self.po.login.goto()
            self.po.login.login(username, PASSWORD)
            expect(self.po.inventory.list).to_be_visible()

    @keyword("loginExpectingError")
    def login_expecting_error(self, username, password, message):
        """Đăng nhập và chờ thông báo lỗi đúng nguyên văn, vẫn ở trang login."""
        with self.step(f'Đăng nhập "{username}" và chờ lỗi "{message}"'):
            self.po.login.login(username, password)
            expect(self.po.login.error).to_have_text(message)
            expect(self.po.login.login_button).to_be_visible()

    @keyword("dismissError")
    def dismiss_error(self):
        """Bấm nút X để đóng khung lỗi đăng nhập."""
        with self.step("Đóng khung lỗi"):
            self.po.login.error_close.click()

    @keyword("verifyLoginFormDisplayed")
    def verify_login_form_displayed(self):
        """Kiểm tra form đăng nhập hiển thị (username, password, nút Login)."""
        with self.step("Kiểm tra form đăng nhập hiển thị"):
            for locator in (self.po.login.username, self.po.login.password, self.po.login.login_button):
                expect(locator).to_be_visible()

    @keyword("verifyLoginFieldsHighlighted")
    def verify_login_fields_highlighted(self):
        """Kiểm tra ô username và password được đánh dấu lỗi (class "error")."""
        with self.step("Kiểm tra 2 ô nhập bị đánh dấu lỗi"):
            for locator in (self.po.login.username, self.po.login.password):
                expect(locator).to_have_class(re.compile(r"\berror\b"))

    @keyword("verifyLoggedIn")
    def verify_logged_in(self):
        """Kiểm tra đã vào trang danh sách sản phẩm sau đăng nhập."""
        with self.step("Kiểm tra đã đăng nhập"):
            expect(self.po.inventory.list).to_be_visible()
            expect(self.po.header.cart_link).to_be_visible()
