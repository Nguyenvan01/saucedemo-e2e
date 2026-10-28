# Menu burger. Nút mở/đóng không có data-test trên <button> (data-test nằm ở <img> bị nút trong suốt
# phủ lên, không click được) -> dùng id của nút. Menu đóng có thuộc tính hidden; mở thì trượt vào trong 0,5 s (transition)
# -> chờ khung menu nằm hẳn trong màn hình rồi mới bấm mục, tránh click trượt.
from selenium.webdriver.common.by import By

from pages.base_page import BasePage, by_test, step
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

ITEMS = {
    "All Items": by_test("inventory-sidebar-link"),
    "Dynamic Catalog": by_test("dynamic-catalog-sidebar-link"),
    "About": by_test("about-sidebar-link"),
    "Logout": by_test("logout-sidebar-link"),
    "Reset App State": by_test("reset-sidebar-link"),
}


class BurgerMenu(BasePage):
    OPEN_BUTTON = (By.ID, "react-burger-menu-btn")
    CLOSE_BUTTON = (By.ID, "react-burger-cross-btn")
    PANEL = (By.CSS_SELECTOR, ".bm-menu-wrap")

    def item(self, name):
        if name not in ITEMS:
            raise ValueError(f"Mục menu không tồn tại: {name!r}; chọn {list(ITEMS)}")
        return ITEMS[name]

    def is_open(self):
        panels = self.find_all(self.PANEL)
        return bool(panels) and panels[0].get_attribute("aria-hidden") == "false"

    @step("Mở menu")
    def open_menu(self):
        # Cú bấm ngay sau khi trang vừa tải có thể chưa có tác dụng -> bấm lại tới khi menu mở.
        self.wait_until(lambda d: self.is_open() or self.click(self.OPEN_BUTTON), "Menu không mở")
        panel = self.find(self.PANEL)
        self.wait_until(
            lambda d: self.is_open() and d.execute_script("return arguments[0].getBoundingClientRect().left", panel) == 0,
            "Menu chưa mở hết",
        )

    @step("Đóng menu")
    def close_menu(self):
        self.click(self.CLOSE_BUTTON)
        self.wait_until(lambda d: not self.is_open(), "Menu chưa đóng")

    def item_texts(self, names):
        """Nhãn đang hiển thị của các mục menu (menu phải đang mở)."""
        return [self.text(self.item(name)) for name in names]

    def about_href(self):
        return self.attribute(self.item("About"), "href")

    def choose(self, name):
        """Mở menu nếu đang đóng rồi bấm mục `name`."""
        if not self.is_open():
            self.open_menu()
        self.click(self.item(name))

    @step("Menu: All Items")
    def all_items(self):
        self.choose("All Items")
        return InventoryPage(self.driver).wait_loaded()

    @step("Menu: Logout")
    def logout(self):
        self.choose("Logout")
        return LoginPage(self.driver).wait_loaded()

    @step("Menu: Reset App State")
    def reset_app_state(self):
        """Xoá giỏ trong localStorage; nút trên trang chỉ đổi sau reload."""
        self.choose("Reset App State")
