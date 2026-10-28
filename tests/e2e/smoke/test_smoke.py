# ============================================================
# TEST: SMOKE - luồng chính đi qua đủ các tầng (test -> page object -> Selenium WebDriver)
# Đăng nhập qua UI (không dùng phiên sẵn) -> thêm 1 sản phẩm -> giỏ -> checkout -> hoàn tất -> logout.
# Dữ liệu: data/checkout/smoke.json#purchase
# ============================================================
import pytest

from config import PASSWORD
from utils.cases import case_params
from utils.data_loader import load_data, resolve_data
from utils.routes import ROUTES

DATA = load_data("checkout/smoke.json#purchase")


@pytest.mark.parametrize("case", case_params(DATA))
def test_smoke_purchase(po, ctx, case):
    c = resolve_data(case, ctx)
    customer = c["customer"]
    inventory = po.login.login_as(c["username"], PASSWORD)
    assert inventory.product_count() == c["productCount"]
    inventory.add_to_cart(c["product"])
    assert po.header.cart_badge() == 1
    cart = po.header.open_cart()
    assert cart.names() == [c["product"]]
    info = cart.checkout()
    info.fill(customer["firstName"], customer["lastName"], customer["postalCode"])
    info.submit()
    overview = po.checkout_overview.wait_loaded()
    assert overview.names() == [c["product"]]
    amounts = overview.amounts()
    assert amounts["total"] == amounts["itemTotal"] + amounts["tax"]
    overview.finish()
    overview.wait_for_path(ROUTES["checkoutComplete"])
    assert po.checkout_complete.header() == c["completeHeader"]
    assert po.checkout_complete.message() == c["completeText"]
    assert po.header.cart_badge() == 0
    po.menu.logout()
    assert po.login.form_displayed()
