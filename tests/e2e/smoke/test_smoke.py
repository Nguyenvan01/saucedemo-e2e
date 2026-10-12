# ============================================================
# TEST: SMOKE - luồng chính đi qua đủ các tầng (test -> keyword -> page -> Playwright)
# Đăng nhập qua UI (không dùng phiên sẵn) -> thêm 1 sản phẩm -> giỏ -> checkout -> hoàn tất -> logout.
# Dữ liệu: data/checkout/smoke.json#purchase
# ============================================================
import pytest

from utils.cases import case_params
from utils.data_loader import load_data, resolve_data
from utils.routes import ROUTES

DATA = load_data("checkout/smoke.json#purchase")


@pytest.mark.parametrize("case", case_params(DATA))
def test_smoke_purchase(k, ctx, case):
    c = resolve_data(case, ctx)
    customer = c["customer"]
    k.auth.login_as(c["username"])
    k.inventory.verify_product_count(c["productCount"])
    k.inventory.add_product_to_cart(c["product"])
    k.common.verify_cart_badge(1)
    k.cart.open_cart()
    k.cart.verify_cart_items([c["product"]])
    k.cart.proceed_to_checkout()
    k.checkout.fill_checkout_info(customer["firstName"], customer["lastName"], customer["postalCode"])
    k.checkout.continue_checkout()
    k.checkout.verify_overview_items([c["product"]])
    k.checkout.verify_total_equals_item_total_plus_tax()
    k.checkout.finish_checkout()
    k.common.verify_url(ROUTES["checkoutComplete"])
    k.checkout.verify_order_complete(c["completeHeader"], c["completeText"])
    k.common.verify_cart_badge(0)
    k.menu.logout()
    k.auth.verify_login_form_displayed()
