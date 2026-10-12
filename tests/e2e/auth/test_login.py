# ============================================================
# TEST: ĐĂNG NHẬP
# Mục tiêu: đăng nhập hợp lệ cho từng user; lỗi bỏ trống / sai mật khẩu / bị khoá;
#           trang cần đăng nhập bị chặn khi chưa có phiên.
# Dữ liệu: data/auth/login.json (valid, invalid, protectedPages)
# Kết quả mong đợi: thông báo lỗi đúng nguyên văn (utils/messages.py), không vào được trang trong.
# ============================================================
import pytest

from utils.cases import case_params
from utils.data_loader import load_data, resolve_data
from utils.routes import ROUTES

DATA = load_data("auth/login.json")


class TestLoginValid:
    """Đăng nhập hợp lệ (data-driven theo user)"""

    @pytest.mark.parametrize("case", case_params(DATA["valid"]))
    def test_login_valid(self, k, case):
        k.auth.login_as(case["username"])
        k.common.verify_url(ROUTES["inventory"])
        k.auth.verify_logged_in()


class TestLoginInvalid:
    """Đăng nhập thất bại: hiện lỗi nguyên văn, đánh dấu 2 ô nhập, đóng được khung lỗi"""

    @pytest.mark.parametrize("case", case_params(DATA["invalid"]))
    def test_login_invalid(self, k, ctx, case):
        c = resolve_data(case, ctx)
        k.auth.open_login()
        k.auth.login_expecting_error(c["username"], c["password"], c["error"])
        k.common.verify_url(ROUTES["login"])
        k.auth.verify_login_fields_highlighted()
        k.auth.dismiss_error()
        k.common.verify_no_error_message()


class TestProtectedPages:
    """Mở trang cần đăng nhập khi chưa đăng nhập -> form login + lỗi riêng cho từng trang"""

    @pytest.mark.parametrize("case", case_params(DATA["protectedPages"]))
    def test_protected_page(self, k, ctx, case):
        c = resolve_data(case, ctx)
        k.common.open_page(c["path"])
        k.auth.verify_login_form_displayed()
        k.common.verify_error_message(c["error"])
