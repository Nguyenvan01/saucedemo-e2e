# Trang / - đăng nhập. Cũng là trang hiện ra khi mở trang cần đăng nhập mà chưa có phiên.
from pages.base_page import BasePage, by_test, step
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    path = "/"
    USERNAME = by_test("username")
    PASSWORD = by_test("password")
    LOGIN_BUTTON = by_test("login-button")
    ERROR_CLOSE = by_test("error-button")
    landmark = LOGIN_BUTTON

    @step('Đăng nhập với "{username}"')
    def login(self, username, password):
        """Nhập username + mật khẩu và bấm Login (không chờ kết quả)."""
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    @step('Đăng nhập "{username}" và chờ danh sách sản phẩm')
    def login_as(self, username, password):
        self.open()
        self.login(username, password)
        return InventoryPage(self.driver).wait_loaded()

    @step("Đóng khung lỗi")
    def dismiss_error(self):
        self.click(self.ERROR_CLOSE)

    def form_displayed(self):
        """Form đăng nhập (username, password, nút Login) đang hiển thị."""
        self.wait_loaded()
        return all(self.find(loc).is_displayed() for loc in (self.USERNAME, self.PASSWORD, self.LOGIN_BUTTON))

    def highlighted_fields(self):
        """Tên các ô nhập đang bị đánh dấu lỗi (class "error")."""
        fields = {"username": self.USERNAME, "password": self.PASSWORD}
        return [name for name, loc in fields.items() if "error" in self.attribute(loc, "class").split()]
