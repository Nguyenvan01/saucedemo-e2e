# ============================================================
# PYTEST LIFECYCLE
# - pytest_configure: tạo thư mục evidence, cấu hình log, JUnit, Allure, trace, retry.
# - Fixture tạo browser context riêng cho mỗi test (pytest-playwright), data-test làm test id.
# - auth_states: đăng nhập qua UI một lần cho mỗi user cần dùng, lưu storageState vào .auth/;
#   cookie phiên saucedemo chỉ sống 600 s -> file sắp hết hạn thì đăng nhập lại.
# - Hook thu evidence khi call FAIL: screenshot + HTML + URL + category.
# - Lỗi evidence chỉ ghi WARNING, không che lỗi test gốc. Không log mật khẩu.
# ============================================================
import logging
import os
from datetime import datetime

import allure
import pytest
from playwright.sync_api import expect

from config import (
    ACTION_TIMEOUT,
    ARTIFACTS_DIR,
    AUTH_DIR,
    AUTH_MIN_REMAINING_SECONDS,
    BASE_URL,
    EXPECT_TIMEOUT,
    IS_CI,
    LOCALE,
    NAVIGATION_TIMEOUT,
    PASSWORD,
    TEST_ENV,
    TEST_ID_ATTRIBUTE,
    USERS,
    VIEWPORT,
)
from keywords import Keywords
from pages.page_objects import PageObjects
from utils.artifact_manager import create_artifact_layout, safe_artifact_name
from utils.cases import case_title
from utils.data_loader import base_context
from utils.error_classifier import classify_report_text
from utils.logging_config import LOGGER_NAME, configure_logging, current_tc_id, event_context
from utils.storage import session_seconds_left, write_storage_state


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
    if config.option.tracing == "off":
        config.option.tracing = "retain-on-failure"
    if config.option.video == "off":
        config.option.video = "retain-on-failure"
    if config.option.output == "test-results":
        config.option.output = str(layout.traces)
    # Site tĩnh, ổn định -> chỉ retry trên CI (mạng runner).
    rerun_given = any(arg.startswith("--reruns") for arg in config.invocation_params.args)
    if hasattr(config.option, "reruns") and not rerun_given:
        config.option.reruns = 1 if IS_CI else 0
    if os.getenv("SLOW_MO") and not config.option.slowmo:
        config.option.slowmo = float(os.environ["SLOW_MO"])

    expect.set_options(timeout=EXPECT_TIMEOUT)
    logger.info(
        f"Bắt đầu pytest session; env={TEST_ENV}, base_url={BASE_URL}, password={'có' if PASSWORD else 'THIẾU'}",
        extra=event_context(action="pytest_session", result="START"),
    )


def pytest_collection_modifyitems(config, items):
    """Gắn marker theo thư mục: tests/framework -> core, tests/e2e -> e2e (+ keyword)."""
    for item in items:
        path = item.path.as_posix()
        if "/tests/framework/" in path:
            item.add_marker(pytest.mark.core)
        elif "/tests/e2e/" in path:
            item.add_marker(pytest.mark.e2e)
        if "/tests/e2e/keyword_driven/" in path:
            item.add_marker(pytest.mark.keyword)


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

    page = item.funcargs.get("page") if hasattr(item, "funcargs") else None
    if page is None or page.is_closed():
        return
    layout = item.config._e2e_layout
    name = safe_artifact_name(item.nodeid)
    try:
        screenshot = page.screenshot(full_page=True)
        screenshot_path = layout.screenshots / f"{name}.png"
        screenshot_path.write_bytes(screenshot)
        allure.attach(screenshot, "failure-screenshot", allure.attachment_type.PNG)

        source = page.content()
        source_path = layout.page_sources / f"{name}.html"
        source_path.write_text(source, encoding="utf-8")
        allure.attach(source, "page-source", allure.attachment_type.HTML)
        allure.attach(page.url, "current-url", allure.attachment_type.TEXT)
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
# Browser: data-test làm test id, phiên đăng nhập sẵn theo user
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def _test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute(TEST_ID_ATTRIBUTE)


def _context_options():
    return {"base_url": BASE_URL, "locale": LOCALE, "viewport": VIEWPORT}


@pytest.fixture(scope="session")
def auth_states(browser, _test_id_attribute):
    """Hàm user -> file storageState còn hạn. Đăng nhập qua UI lần đầu cần dùng (mỗi worker),
    và đăng nhập lại khi cookie còn dưới AUTH_MIN_REMAINING_SECONDS."""

    def get(user):
        if user not in USERS:
            raise ValueError(f"user không hợp lệ: {user!r}; chọn {USERS}")
        file = AUTH_DIR / f"{TEST_ENV}-{user}.json"
        if session_seconds_left(file) >= AUTH_MIN_REMAINING_SECONDS:
            return file
        context = browser.new_context(**_context_options())
        try:
            context.set_default_timeout(ACTION_TIMEOUT)
            po = PageObjects(context.new_page())
            po.login.goto()
            po.login.login(user, PASSWORD)
            expect(po.inventory.list).to_be_visible()
            write_storage_state(file, context.storage_state())
        finally:
            context.close()
        logging.getLogger(LOGGER_NAME).info(
            f"Đã tạo phiên đăng nhập cho {user}",
            extra=event_context(action="auth_states", target=file.name, result="PASS"),
        )
        return file

    return get


@pytest.fixture
def browser_context_args(browser_context_args, request):
    """Mở rộng context mặc định của pytest-playwright: base_url, locale, viewport, phiên đăng nhập.
    Phiên chọn bằng marker: @pytest.mark.role("standard_user")."""
    args = {**browser_context_args, **_context_options()}
    marker = request.node.get_closest_marker("role")
    if marker:
        if not PASSWORD:
            pytest.skip("Cần SAUCE_PASSWORD trong .env")
        args["storage_state"] = str(request.getfixturevalue("auth_states")(marker.args[0]))
    return args


@pytest.fixture
def context(new_context, _test_id_attribute):
    context = new_context()
    context.set_default_timeout(ACTION_TIMEOUT)
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
    return context


@pytest.fixture
def page(context):
    return context.new_page()


# ---------------------------------------------------------------------------
# Fixture nghiệp vụ
# ---------------------------------------------------------------------------

@pytest.fixture
def k(page):
    """Thư viện keyword (tầng nghiệp vụ) - cách viết test chính."""
    return Keywords(page)


@pytest.fixture
def po(k):
    """Page Object - dùng khi cần locator trực tiếp trong test."""
    return k.po


@pytest.fixture
def ctx():
    """Context thay biến ${...} cho dữ liệu: env (URL, mật khẩu), msg (thông báo nguyên văn)."""
    return base_context()
