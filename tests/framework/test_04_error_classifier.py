# ============================================================
# UNIT: utils/error_classifier - cùng một taxonomy lỗi cho log / JUnit / Allure.
# ============================================================
import pytest
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidSessionIdException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    UnexpectedAlertPresentException,
    WebDriverException,
)

from utils.error_classifier import classify_exception, classify_report_text


@pytest.mark.parametrize(
    ("error", "category"),
    [
        (AssertionError("x"), "ASSERTION_FAILED"),
        (TimeoutException("timeout"), "TIMEOUT"),
        (NoSuchElementException("no such element"), "ELEMENT_NOT_FOUND"),
        (StaleElementReferenceException("stale"), "STALE_ELEMENT"),
        (ElementClickInterceptedException("intercepted"), "ELEMENT_NOT_INTERACTABLE"),
        (UnexpectedAlertPresentException("Sorting is broken!"), "UNEXPECTED_ALERT"),
        (InvalidSessionIdException("invalid session id"), "BROWSER_CLOSED"),
        (WebDriverException("unknown error: net::ERR_NAME_NOT_RESOLVED"), "NETWORK_ERROR"),
        (WebDriverException("khác"), "WEBDRIVER_ERROR"),
        (ValueError("x"), "DATA_OR_CONTRACT_ERROR"),
        (KeyError("x"), "DATA_OR_CONTRACT_ERROR"),
        (RuntimeError("x"), "UNEXPECTED_ERROR"),
    ],
)
def test_classify_exception(error, category):
    assert classify_exception(error) == category


@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("selenium.common.exceptions.TimeoutException: Message:", "TIMEOUT"),
        ("E   AssertionError: assert 'Products' == 'Your Cart'", "ASSERTION_FAILED"),
        ("selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: Sorting is broken!", "UNEXPECTED_ALERT"),
        ("ValueError: Không có sản phẩm", "DATA_OR_CONTRACT_ERROR"),
        ("", "UNEXPECTED_ERROR"),
    ],
)
def test_classify_report_text(text, category):
    assert classify_report_text(text) == category
