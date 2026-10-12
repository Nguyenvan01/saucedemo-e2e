# Menu burger. Nút mở/đóng không có data-test trên <button> -> dùng role.
class BurgerMenu:
    def __init__(self, page):
        self.open_button = page.get_by_role("button", name="Open Menu")
        self.close_button = page.get_by_role("button", name="Close Menu")
        # Menu đóng chỉ bị dịch ra ngoài màn hình (is_visible vẫn True) nhưng có aria-hidden="true";
        # locator theo role bỏ qua phần tử aria-hidden -> chỉ khớp khi menu đang mở.
        self.panel = page.get_by_role("navigation")
        self.links = {
            "All Items": page.get_by_test_id("inventory-sidebar-link"),
            "Dynamic Catalog": page.get_by_test_id("dynamic-catalog-sidebar-link"),
            "About": page.get_by_test_id("about-sidebar-link"),
            "Logout": page.get_by_test_id("logout-sidebar-link"),
            "Reset App State": page.get_by_test_id("reset-sidebar-link"),
        }

    def link(self, name):
        if name not in self.links:
            raise ValueError(f"Mục menu không tồn tại: {name!r}; chọn {list(self.links)}")
        return self.links[name]
