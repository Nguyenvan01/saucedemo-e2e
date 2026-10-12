# ============================================================
# CẤU HÌNH DỰ ÁN: đường dẫn, môi trường, URL, tài khoản và timeout dùng chung.
# Chỉ có một môi trường: production https://www.saucedemo.com (TEST_ENV=prod).
# Mật khẩu đọc từ .env (local) hoặc biến môi trường SAUCE_PASSWORD (GitHub Secrets trên CI).
# Expected thuộc dữ liệu/đặc tả; cấu hình không được sửa expected để làm test xanh.
# ============================================================
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
SCENARIO_DIR = DATA_DIR / "scenarios"


def _load_env(path):
    """Đọc KEY=VALUE từ .env; biến môi trường đã có (CI) luôn được ưu tiên."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() and not key.strip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


_load_env(ROOT / ".env")

TEST_ENV = os.getenv("TEST_ENV") or "prod"
ARTIFACTS_DIR = ROOT / "artifacts" / TEST_ENV
BASE_URL = (os.getenv("BASE_URL") or "https://www.saucedemo.com").rstrip("/")
IS_CI = bool(os.getenv("CI"))

PASSWORD = os.getenv("SAUCE_PASSWORD", "")
# Tên đăng nhập công khai trên trang login (không phải bí mật).
USERS = (
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
)

# storageState của từng user (sinh bởi fixture auth_states trong tests/conftest.py).
AUTH_DIR = ROOT / ".auth"
# Cookie phiên của saucedemo hết hạn sau 600 s; state còn ít hơn chừng này thì đăng nhập lại.
AUTH_MIN_REMAINING_SECONDS = 180

# Timeout (mili giây) theo quy ước của Playwright.
# performance_glitch_user mất ~5,5 s mới hiện danh sách sản phẩm -> EXPECT_TIMEOUT phải > 6 s.
EXPECT_TIMEOUT = 10_000
ACTION_TIMEOUT = 10_000
NAVIGATION_TIMEOUT = 20_000

TEST_ID_ATTRIBUTE = "data-test"
VIEWPORT = {"width": 1280, "height": 720}
LOCALE = "en-US"
