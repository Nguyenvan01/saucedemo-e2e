# ============================================================
# POM CƠ SỞ (Selenium WebDriver): locator + thao tác nguyên tử; không chứa expected của ca kiểm thử.
# - Locator ưu tiên thuộc tính data-test (by_test). Không dùng XPath theo cấu trúc DOM.
# - Mọi thao tác chờ tường minh bằng WebDriverWait (không dùng implicit wait, không sleep cứng).
# - @step: 1 Allure step + log START/PASS/FAIL cho method nghiệp vụ của Page Object.
# ============================================================
import functools
import inspect

import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, WAIT_TIMEOUT
from utils.data_loader import mask_secrets
from utils.error_classifier import classify_exception
from utils.logging_config import event_context, get_logger


def by_test(value):
    """Locator theo data-test, vd by_test("login-button") -> [data-test="login-button"]."""
    return By.CSS_SELECTOR, f'[data-test="{value}"]'


def slug(name):
    """Tên sản phẩm -> hậu tố data-test của nút, vd: "Sauce Labs Onesie" -> "sauce-labs-onesie"."""
    return name.lower().replace(" ", "-")


def step(title):
    """Đánh dấu method là 1 bước nghiệp vụ; title dùng tên tham số, vd step('Đăng nhập "{username}"')."""

    def decorate(function):
        signature = inspect.signature(function)

        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            bound = signature.bind(self, *args, **kwargs)
            bound.apply_defaults()
            text = mask_secrets(title.format(**bound.arguments))
            logger = get_logger()
            context = event_context(action=type(self).__name__, target=text, result="START")
            logger.debug("Bắt đầu bước", extra=context)
            with allure.step(text):
                try:
                    result = function(self, *args, **kwargs)
                except Exception as error:
                    logger.error(
                        f"Bước thất bại; category={classify_exception(error)}",
                        extra={**context, "result": "FAIL"},
                    )
                    raise
            logger.info("Hoàn thành bước", extra={**context, "result": "PASS"})
            return result

        return wrapper

    return decorate


class BasePage:
    # URL tương đối của trang (để trống nếu trang cần tham số) và phần tử báo trang đã sẵn sàng.
    path = ""
    landmark = None

    TITLE = by_test("title")
    # Khung lỗi dùng chung: trang login và checkout bước 1.
    ERROR = by_test("error")

    def __init__(self, driver):
        self.driver = driver

    # --- chờ -------------------------------------------------------------
    def wait(self, timeout=WAIT_TIMEOUT):
        return WebDriverWait(self.driver, timeout, ignored_exceptions=[StaleElementReferenceException])

    def wait_until(self, condition, message, timeout=WAIT_TIMEOUT):
        """Chờ condition(driver) truthy; hết giờ -> AssertionError (kỳ vọng không đạt)."""
        try:
            return self.wait(timeout).until(condition)
        except Exception as error:
            raise AssertionError(f"{message} (sau {timeout}s)") from error

    def wait_loaded(self):
        if self.landmark:
            self.find(self.landmark)
        return self

    # --- tìm phần tử -----------------------------------------------------
    def find(self, locator):
        """Phần tử đầu tiên khớp locator, chờ tới khi hiển thị."""
        return self.wait().until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Mọi phần tử khớp locator tại thời điểm gọi (có thể rỗng, không chờ)."""
        return self.driver.find_elements(*locator)

    def count(self, locator):
        return len(self.find_all(locator))

    def text(self, locator):
        return self.find(locator).text

    def texts(self, locator):
        return [element.text for element in self.find_all(locator)]

    def attribute(self, locator, name):
        return self.find(locator).get_attribute(name)

    # --- thao tác --------------------------------------------------------
    def click(self, locator):
        """Chờ click được rồi click; bị phần tử khác che (hiệu ứng) thì thử lại tới hết timeout."""
        wait = WebDriverWait(
            self.driver,
            WAIT_TIMEOUT,
            ignored_exceptions=[StaleElementReferenceException, ElementClickInterceptedException],
        )
        wait.until(lambda d: EC.element_to_be_clickable(locator)(d).click() or True)

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        if text:
            element.send_keys(text)

    # --- điều hướng ------------------------------------------------------
    def open(self, path=None):
        self.driver.get(BASE_URL + (path or self.path))
        return self.wait_loaded()

    def reload(self):
        self.driver.refresh()
        return self.wait_loaded()

    def current_path(self):
        """URL hiện tại bỏ BASE_URL, vd "/cart.html" hoặc "/inventory-item.html?id=4"."""
        url = self.driver.current_url
        return url[len(BASE_URL):] if url.startswith(BASE_URL) else url

    def wait_for_path(self, path):
        """Chờ URL hiện tại đúng bằng BASE_URL + path."""
        self.wait_until(lambda d: self.current_path() == path, f'URL khác "{path}": "{self.current_path()}"')

    # --- phần tử chung ---------------------------------------------------
    def page_title(self):
        return self.text(self.TITLE)

    def error_message(self):
        return self.text(self.ERROR)

    def has_error(self):
        return self.count(self.ERROR) > 0
