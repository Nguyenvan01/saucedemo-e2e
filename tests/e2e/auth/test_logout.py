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
def test_logout(po, ctx, case):
    c = resolve_data(case, ctx)
    po.inventory.open()
    po.menu.logout()
    assert po.login.current_path() == ROUTES["login"]
    assert po.login.form_displayed()
    po.base.open(c["protectedPath"])
    assert po.login.error_message() == c["error"]
