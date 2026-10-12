# POM CƠ SỞ: locator + thao tác nguyên tử; không chứa expected của ca kiểm thử.
# Locator ưu tiên data-test (selectors.set_test_id_attribute("data-test") -> get_by_test_id),
# sau đó tới get_by_role. Không dùng XPath/CSS theo cấu trúc DOM.


def slug(name):
    """Tên sản phẩm -> hậu tố data-test của nút, vd: "Sauce Labs Onesie" -> "sauce-labs-onesie"."""
    return name.lower().replace(" ", "-")


class BasePage:
    # URL tương đối của trang (để trống nếu trang cần tham số).
    path = ""

    def __init__(self, page):
        self.page = page
        self.title = page.get_by_test_id("title")
        # Khung lỗi dùng chung: trang login và checkout bước 1.
        self.error = page.get_by_test_id("error")

    def goto(self, path=None):
        self.page.goto(path or self.path)
