# THƯ VIỆN KEYWORD - NHÓM menu: menu burger (All Items, About, Logout, Reset App State).
from playwright.sync_api import expect

from keywords.base_keywords import BaseKeywords, keyword


class MenuKeywords(BaseKeywords):
    group = "menu"

    def _click(self, name):
        """Mở menu nếu đang đóng rồi bấm mục `name`."""
        menu = self.po.menu
        if menu.panel.count() == 0:
            menu.open_button.click()
            expect(menu.panel).to_be_visible()
        menu.link(name).click()

    @keyword("openMenu")
    def open_menu(self):
        """Mở menu burger."""
        with self.step("Mở menu"):
            self.po.menu.open_button.click()
            expect(self.po.menu.panel).to_be_visible()

    @keyword("closeMenu")
    def close_menu(self):
        """Đóng menu burger."""
        with self.step("Đóng menu"):
            self.po.menu.close_button.click()
            expect(self.po.menu.panel).to_be_hidden()

    @keyword("verifyMenuItems")
    def verify_menu_items(self, names):
        """Kiểm tra các mục menu đang hiển thị với đúng nhãn."""
        with self.step(f"Kiểm tra menu có: {names}"):
            for name in names:
                expect(self.po.menu.link(name)).to_be_visible()
                expect(self.po.menu.link(name)).to_have_text(name)

    @keyword("verifyAboutLink")
    def verify_about_link(self, href):
        """Kiểm tra link About trỏ đúng địa chỉ (không mở trang ngoài)."""
        with self.step(f'Kiểm tra About trỏ tới "{href}"'):
            expect(self.po.menu.link("About")).to_have_attribute("href", href)

    @keyword("gotoAllItems")
    def goto_all_items(self):
        """Chọn "All Items" và chờ danh sách sản phẩm."""
        with self.step("Menu: All Items"):
            self._click("All Items")
            expect(self.po.inventory.list).to_be_visible()

    @keyword("logout")
    def logout(self):
        """Chọn "Logout" và chờ form đăng nhập."""
        with self.step("Menu: Logout"):
            self._click("Logout")
            expect(self.po.login.login_button).to_be_visible()

    @keyword("resetAppState")
    def reset_app_state(self):
        """Chọn "Reset App State" (xoá giỏ trong localStorage; nút trên trang chỉ đổi sau reload)."""
        with self.step("Menu: Reset App State"):
            self._click("Reset App State")
