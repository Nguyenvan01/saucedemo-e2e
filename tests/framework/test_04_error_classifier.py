# ============================================================
# UNIT: utils/error_classifier - cùng một taxonomy lỗi cho log / JUnit / Allure.
# ============================================================
import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from utils.error_classifier import classify_exception, classify_report_text


@pytest.mark.parametrize(
    ("error", "category"),
    [
        (AssertionError("x"), "ASSERTION_FAILED"),
        (PlaywrightTimeoutError("Timeout 10000ms exceeded"), "TIMEOUT"),
        (PlaywrightError("strict mode violation: resolved to 6 elements"), "LOCATOR_AMBIGUOUS"),
        (PlaywrightError("net::ERR_NAME_NOT_RESOLVED"), "NETWORK_ERROR"),
        (PlaywrightError("Target page, context or browser has been closed"), "BROWSER_CLOSED"),
        (PlaywrightError("khác"), "PLAYWRIGHT_ERROR"),
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
        ("playwright._impl._errors.TimeoutError: Locator expected", "TIMEOUT"),
        ("E   AssertionError: Locator expected to have text", "ASSERTION_FAILED"),
        ("ValueError: Keyword chưa khai báo", "DATA_OR_CONTRACT_ERROR"),
        ("", "UNEXPECTED_ERROR"),
    ],
)
def test_classify_report_text(text, category):
    assert classify_report_text(text) == category
