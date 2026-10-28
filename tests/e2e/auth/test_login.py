# ============================================================
# TEST: ĐĂNG NHẬP
# Mục tiêu: đăng nhập hợp lệ cho từng user; lỗi bỏ trống / sai mật khẩu / bị khoá;
#           trang cần đăng nhập bị chặn khi chưa có phiên.
# Dữ liệu: data/auth/login.json (valid, invalid, protectedPages)
# Kết quả mong đợi: thông báo lỗi đúng nguyên văn (utils/messages.py), không vào được trang trong.
# ============================================================
import pytest

from config import PASSWORD
from utils.cases import case_params
from utils.data_loader import load_data, resolve_data
from utils.routes import ROUTES

DATA = load_data("auth/login.json")


class TestLoginValid:
    """Đăng nhập hợp lệ (data-driven theo user)"""

    @pytest.mark.parametrize("case", case_params(DATA["valid"]))
    def test_login_valid(self, po, case):
        po.login.login_as(case["username"], PASSWORD)
        po.base.wait_for_path(ROUTES["inventory"])
        assert po.header.find(po.header.CART_LINK).is_displayed()


class TestLoginInvalid:
    """Đăng nhập thất bại: hiện lỗi nguyên văn, đánh dấu 2 ô nhập, đóng được khung lỗi"""

    @pytest.mark.parametrize("case", case_params(DATA["invalid"]))
    def test_login_invalid(self, po, ctx, case):
        c = resolve_data(case, ctx)
        po.login.open()
        po.login.login(c["username"], c["password"])
        assert po.login.error_message() == c["error"]
        assert po.login.current_path() == ROUTES["login"]
        assert po.login.highlighted_fields() == ["username", "password"]
        po.login.dismiss_error()
        assert not po.login.has_error()


class TestProtectedPages:
    """Mở trang cần đăng nhập khi chưa đăng nhập -> form login + lỗi riêng cho từng trang"""

    @pytest.mark.parametrize("case", case_params(DATA["protectedPages"]))
    def test_protected_page(self, po, ctx, case):
        c = resolve_data(case, ctx)
        po.base.open(c["path"])
        assert po.login.form_displayed()
        assert po.login.error_message() == c["error"]
