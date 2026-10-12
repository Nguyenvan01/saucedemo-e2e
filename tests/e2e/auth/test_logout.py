# ============================================================
# TEST: ĐĂNG XUẤT
# Mục tiêu: Logout trong menu đưa về form login và xoá phiên; mở lại trang trong bị chặn.
# Dữ liệu: data/auth/login.json#logout
# ============================================================
import pytest

from utils.cases import case_params
from utils.data_loader import load_data, resolve_data
from utils.routes import ROUTES

DATA = load_data("auth/login.json#logout")


@pytest.mark.role("standard_user")
@pytest.mark.parametrize("case", case_params(DATA))
def test_logout(k, ctx, case):
    c = resolve_data(case, ctx)
    k.inventory.open_inventory()
    k.menu.logout()
    k.common.verify_url(ROUTES["login"])
    k.auth.verify_login_form_displayed()
    k.common.open_page(c["protectedPath"])
    k.common.verify_error_message(c["error"])
