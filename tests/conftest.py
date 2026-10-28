# ============================================================
# PYTEST LIFECYCLE
# - pytest_configure: tạo thư mục evidence, cấu hình log, JUnit, Allure, retry.
# - Fixture `driver`: mỗi test một Chrome (Selenium WebDriver) riêng, đóng khi test xong.
# - auth_sessions: đăng nhập qua UI một lần cho mỗi user cần dùng (mỗi worker), giữ cookie phiên;
#   cookie saucedemo chỉ sống 600 s -> sắp hết hạn thì đăng nhập lại.
# - Hook thu evidence khi call FAIL: screenshot + HTML + URL + category.
# - Lỗi evidence chỉ ghi WARNING, không che lỗi test gốc. Không log mật khẩu.
# ============================================================
import logging
import os
from datetime import datetime

import allure
import pytest
from selenium import webdriver

from config import (
    ARTIFACTS_DIR,
    AUTH_MIN_REMAINING_SECONDS,
    BASE_URL,
    IS_CI,
    LOCALE,
    PAGE_LOAD_TIMEOUT,
    PASSWORD,
    TEST_ENV,
    USERS,
    WINDOW_SIZE,
)
from pages.page_objects import PageObjects
from utils.artifact_manager import create_artifact_layout, safe_artifact_name
from utils.cases import case_title
from utils.data_loader import base_context
from utils.error_classifier import classify_report_text
from utils.logging_config import LOGGER_NAME, configure_logging, current_tc_id, event_context
from utils.storage import STORAGE_KEYS, session_seconds_left


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="Mở cửa sổ Chrome (mặc định chạy headless)")


def _worker_id(config):
    return getattr(config, "workerinput", {}).get("workerid", "")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Tiến trình chính sinh run_id; worker xdist kế thừa qua biến môi trường.
    run_id = os.environ.setdefault("E2E_RUN_ID", datetime.now().strftime("%Y%m%d_%H%M%S"))
    layout = create_artifact_layout(ARTIFACTS_DIR, run_id)
    worker = _worker_id(config)
    logger, log_path = configure_logging(layout.logs, f"{run_id}_{worker}" if worker else run_id)
    config._e2e_layout = layout
    config._e2e_log_path = log_path

    # Báo cáo mặc định (người dùng truyền tham số riêng thì giữ nguyên).
    if not config.option.xmlpath:
        config.option.xmlpath = str(layout.junit / "results.xml")
    if hasattr(config.option, "allure_report_dir") and not config.option.allure_report_dir:
        config.option.allure_report_dir = str(layout.allure_results)
    # Site tĩnh, ổn định -> chỉ retry trên CI (mạng runner).
    rerun_given = any(arg.startswith("--reruns") for arg in config.invocation_params.args)
    if hasattr(config.option, "reruns") and not rerun_given:
        config.option.reruns = 1 if IS_CI else 0

    logger.info(
        f"Bắt đầu pytest session; env={TEST_ENV}, base_url={BASE_URL}, password={'có' if PASSWORD else 'THIẾU'}",
        extra=event_context(action="pytest_session", result="START"),
    )


def pytest_collection_modifyitems(config, items):
    """Gắn marker theo thư mục: tests/framework -> core, tests/e2e -> e2e."""
    for item in items:
        path = item.path.as_posix()
        if "/tests/framework/" in path:
            item.add_marker(pytest.mark.core)
        elif "/tests/e2e/" in path:
            item.add_marker(pytest.mark.e2e)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Thu bằng chứng đúng một lần ở call phase và giữ nguyên kết quả report."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)
    if report.when != "call" or not report.failed:
        return

    category = classify_report_text(report.longreprtext)
    report.user_properties.append(("error_category", category))
    logger = logging.getLogger(LOGGER_NAME)
    logger.error(
        f"Pytest item thất bại; category={category}",
        extra=event_context(tc_id=item.name, action="pytest_report", result="FAIL"),
    )
    allure.dynamic.label("error_category", category)
    allure.attach(category, "error-category", allure.attachment_type.TEXT)

    driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if driver is None:
        return
    layout = item.config._e2e_layout
    name = safe_artifact_name(item.nodeid)
    try:
        screenshot = driver.get_screenshot_as_png()
        screenshot_path = layout.screenshots / f"{name}.png"
        screenshot_path.write_bytes(screenshot)
        allure.attach(screenshot, "failure-screenshot", allure.attachment_type.PNG)

        source = driver.page_source
        source_path = layout.page_sources / f"{name}.html"
        source_path.write_text(source, encoding="utf-8")
        allure.attach(source, "page-source", allure.attachment_type.HTML)
        allure.attach(driver.current_url, "current-url", allure.attachment_type.TEXT)
        logger.info(
            f"Đã lưu evidence: {screenshot_path.name}, {source_path.name}",
            extra=event_context(tc_id=item.name, action="collect_evidence", result="PASS"),
        )
    except Exception as evidence_error:
        logger.warning(
            f"Không thu được đầy đủ evidence: {evidence_error}",
            extra=event_context(tc_id=item.name, action="collect_evidence", result="WARNING"),
        )


def pytest_sessionfinish(session, exitstatus):
    logging.getLogger(LOGGER_NAME).info(
        f"Kết thúc pytest session; exitstatus={exitstatus}",
        extra=event_context(action="pytest_session", result="END"),
    )


# ---------------------------------------------------------------------------
# Ngữ cảnh test: TC_ID cho log, tiêu đề Allure
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _test_context(request):
    """TC_ID = id của data case (nếu có) hoặc tên test; tiêu đề Allure lấy từ case/docstring."""
    params = getattr(getattr(request.node, "callspec", None), "params", {})
    case = params.get("case")
    if isinstance(case, dict) and case.get("id") and case.get("title"):
        tc_id, title = case["id"], case_title(case)
    else:
        doc = (request.function.__doc__ or "").strip().splitlines()
        tc_id, title = request.node.name, doc[0] if doc else None
    if title:
        allure.dynamic.title(title)
    allure.dynamic.parameter("env", TEST_ENV)
    token = current_tc_id.set(tc_id)
    yield
    current_tc_id.reset(token)


# ---------------------------------------------------------------------------
# Browser: Chrome qua Selenium WebDriver, phiên đăng nhập sẵn theo user
# ---------------------------------------------------------------------------

def _new_driver(config):
    options = webdriver.ChromeOptions()
    if not config.getoption("headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size={},{}".format(*WINDOW_SIZE))
    options.add_argument(f"--lang={LOCALE}")
    if IS_CI:
        options.add_argument("--disable-dev-shm-usage")
    # Tắt trình quản lý mật khẩu: Chrome hiện popup "mật khẩu bị lộ" che trang khi dùng mật khẩu demo.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "intl.accept_languages": LOCALE,
    })
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver


@pytest.fixture(scope="session")
def auth_sessions(pytestconfig):
    """Hàm user -> cookie phiên còn hạn. Đăng nhập qua UI lần đầu cần dùng (mỗi worker),
    và đăng nhập lại khi cookie còn dưới AUTH_MIN_REMAINING_SECONDS."""
    cookies = {}

    def get(user):
        if user not in USERS:
            raise ValueError(f"user không hợp lệ: {user!r}; chọn {USERS}")
        if session_seconds_left(cookies.get(user)) >= AUTH_MIN_REMAINING_SECONDS:
            return cookies[user]
        driver = _new_driver(pytestconfig)
        try:
            PageObjects(driver).login.login_as(user, PASSWORD)
            cookies[user] = driver.get_cookie(STORAGE_KEYS["session"])
        finally:
            driver.quit()
        logging.getLogger(LOGGER_NAME).info(
            f"Đã tạo phiên đăng nhập cho {user}",
            extra=event_context(action="auth_sessions", target=user, result="PASS"),
        )
        return cookies[user]

    return get


@pytest.fixture
def driver(request):
    """Chrome riêng cho test. Phiên chọn bằng marker: @pytest.mark.role("standard_user")."""
    marker = request.node.get_closest_marker("role")
    cookie = None
    if marker:
        if not PASSWORD:
            pytest.skip("Cần SAUCE_PASSWORD trong .env")
        cookie = request.getfixturevalue("auth_sessions")(marker.args[0])
    driver = _new_driver(request.config)
    try:
        if cookie:
            # Cookie chỉ gắn được khi đang ở đúng domain.
            driver.get(BASE_URL + "/")
            driver.add_cookie({key: cookie[key] for key in ("name", "value", "path", "expiry")})
        yield driver
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# Fixture nghiệp vụ
# ---------------------------------------------------------------------------

@pytest.fixture
def po(driver):
    """Page Object của test - cách viết test chính: po.login, po.inventory, po.cart..."""
    return PageObjects(driver)


@pytest.fixture
def ctx():
    """Context thay biến ${...} cho dữ liệu: env (URL, mật khẩu), msg (thông báo nguyên văn)."""
    return base_context()
