# PHÂN LOẠI LỖI: hỗ trợ báo cáo, không thay đổi kiểu exception hoặc kết quả test.
# Cùng một vocabulary cho log, JUnit và Allure.
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidSessionIdException,
    NoSuchElementException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    UnexpectedAlertPresentException,
    WebDriverException,
)

NETWORK_TOKENS = ("net::ERR_", "ECONNREFUSED", "ENOTFOUND", "ECONNRESET", "ETIMEDOUT")

# Thứ tự quan trọng: lớp con đứng trước WebDriverException.
EXCEPTION_CATEGORIES = (
    (AssertionError, "ASSERTION_FAILED"),
    (TimeoutException, "TIMEOUT"),
    (NoSuchElementException, "ELEMENT_NOT_FOUND"),
    (StaleElementReferenceException, "STALE_ELEMENT"),
    ((ElementClickInterceptedException, ElementNotInteractableException), "ELEMENT_NOT_INTERACTABLE"),
    (UnexpectedAlertPresentException, "UNEXPECTED_ALERT"),
    ((InvalidSessionIdException, NoSuchWindowException), "BROWSER_CLOSED"),
)


def classify_exception(error):
    for types, category in EXCEPTION_CATEGORIES:
        if isinstance(error, types):
            return category
    if isinstance(error, WebDriverException):
        if any(token in (error.msg or "") for token in NETWORK_TOKENS):
            return "NETWORK_ERROR"
        return "WEBDRIVER_ERROR"
    if isinstance(error, (ValueError, KeyError, TypeError)):
        return "DATA_OR_CONTRACT_ERROR"
    return "UNEXPECTED_ERROR"


def classify_report_text(text):
    """Phân loại dự phòng tại pytest hook khi chỉ còn traceback dạng chuỗi."""
    content = text or ""
    patterns = (
        ("AssertionError", "ASSERTION_FAILED"),
        ("TimeoutException", "TIMEOUT"),
        ("NoSuchElementException", "ELEMENT_NOT_FOUND"),
        ("StaleElementReferenceException", "STALE_ELEMENT"),
        ("ElementClickInterceptedException", "ELEMENT_NOT_INTERACTABLE"),
        ("ElementNotInteractableException", "ELEMENT_NOT_INTERACTABLE"),
        ("UnexpectedAlertPresentException", "UNEXPECTED_ALERT"),
        ("InvalidSessionIdException", "BROWSER_CLOSED"),
        ("NoSuchWindowException", "BROWSER_CLOSED"),
        *((token, "NETWORK_ERROR") for token in NETWORK_TOKENS),
        ("selenium.common.exceptions", "WEBDRIVER_ERROR"),
        ("ValueError", "DATA_OR_CONTRACT_ERROR"),
        ("KeyError", "DATA_OR_CONTRACT_ERROR"),
        ("TypeError", "DATA_OR_CONTRACT_ERROR"),
    )
    for token, category in patterns:
        if token in content:
            return category
    return "UNEXPECTED_ERROR"
