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
from utils.storage import read_cart

DATA = load_data("checkout/checkout.json")
CUSTOMER = DATA["customer"]


@pytest.fixture(autouse=True)
def open_inventory(po):
    po.inventory.open()


def go_to_overview(po, products):
    po.inventory.add_all_to_cart(products)
    po.header.open_cart()
    info = po.cart.checkout()
    info.fill(CUSTOMER["firstName"], CUSTOMER["lastName"], CUSTOMER["postalCode"])
    info.submit()
    info.wait_for_path(ROUTES["checkoutOverview"])


@pytest.mark.parametrize("case", case_params(DATA["purchase"]))
def test_purchase(po, ctx, case):
    done = ctx["msg"]["checkout"]
    go_to_overview(po, case["products"])
    overview = po.checkout_overview
    assert overview.names() == case["products"]
    assert overview.subtotal_text() == f"Item total: {case['itemTotal']}"
    amounts = overview.amounts()
    assert amounts["itemTotal"] == sum(amounts["prices"])
    assert amounts["total"] == amounts["itemTotal"] + amounts["tax"]
    overview.finish()
    overview.wait_for_path(ROUTES["checkoutComplete"])
    assert po.checkout_complete.header() == done["completeHeader"]
    assert po.checkout_complete.message() == done["completeText"]
    assert po.header.cart_badge() == 0
    assert read_cart(po.driver) == []
    po.checkout_complete.back_home()


@pytest.mark.parametrize("case", case_params(DATA["validation"]))
def test_required_fields(po, ctx, case):
    c = resolve_data(case, ctx)
    info = po.header.open_cart().checkout()
    info.fill(c["firstName"], c["lastName"], c["postalCode"])
    info.submit()
    assert info.error_message() == c["error"]
    assert info.current_path() == ROUTES["checkoutInfo"]


@pytest.mark.parametrize("case", case_params(DATA["cancel"]))
def test_cancel(po, case):
    if case["cancelAt"] == "overview":
        go_to_overview(po, case["products"])
        po.checkout_overview.cancel()
    else:
        po.inventory.add_all_to_cart(case["products"])
        po.header.open_cart().checkout().cancel()
    po.base.wait_for_path(case["expectedPath"])
    assert po.header.cart_badge() == len(case["products"])
