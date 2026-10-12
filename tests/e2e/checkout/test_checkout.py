# ============================================================
# TEST: THANH TOÁN
# Mục tiêu: luồng mua hoàn chỉnh (tổng tiền = item total + tax); validate 3 trường bắt buộc;
#           Cancel ở từng bước. Lỗi cố ý của problem_user / error_user -> knownBug (xfail).
# Dữ liệu: data/checkout/checkout.json
# ============================================================
import pytest

from utils.cases import case_params
from utils.data_loader import load_data, resolve_data
from utils.routes import ROUTES

DATA = load_data("checkout/checkout.json")
CUSTOMER = DATA["customer"]


@pytest.fixture(autouse=True)
def open_inventory(k):
    k.inventory.open_inventory()


def _go_to_checkout(k, products):
    k.inventory.add_products_to_cart(products)
    k.cart.open_cart()
    k.cart.proceed_to_checkout()


@pytest.mark.parametrize("case", case_params(DATA["purchase"]))
def test_purchase(k, ctx, case):
    done = ctx["msg"]["checkout"]
    _go_to_checkout(k, case["products"])
    k.checkout.fill_checkout_info(CUSTOMER["firstName"], CUSTOMER["lastName"], CUSTOMER["postalCode"])
    k.checkout.continue_checkout()
    k.common.verify_url(ROUTES["checkoutOverview"])
    k.checkout.verify_overview_items(case["products"])
    k.checkout.verify_item_total(case["itemTotal"])
    k.checkout.verify_item_total_equals_sum()
    k.checkout.verify_total_equals_item_total_plus_tax()
    k.checkout.finish_checkout()
    k.common.verify_url(ROUTES["checkoutComplete"])
    k.checkout.verify_order_complete(done["completeHeader"], done["completeText"])
    k.common.verify_cart_badge(0)
    k.common.verify_cart_storage([])
    k.checkout.back_home()


@pytest.mark.parametrize("case", case_params(DATA["validation"]))
def test_required_fields(k, ctx, case):
    c = resolve_data(case, ctx)
    k.cart.open_cart()
    k.cart.proceed_to_checkout()
    k.checkout.continue_checkout_expecting_error(c["firstName"], c["lastName"], c["postalCode"], c["error"])
    k.common.verify_url(ROUTES["checkoutInfo"])


@pytest.mark.parametrize("case", case_params(DATA["cancel"]))
def test_cancel(k, case):
    _go_to_checkout(k, case["products"])
    if case["cancelAt"] == "overview":
        k.checkout.fill_checkout_info(CUSTOMER["firstName"], CUSTOMER["lastName"], CUSTOMER["postalCode"])
        k.checkout.continue_checkout()
        k.common.verify_url(ROUTES["checkoutOverview"])
    k.checkout.cancel_checkout()
    k.common.verify_url(case["expectedPath"])
    k.common.verify_cart_badge(len(case["products"]))
