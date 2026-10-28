# ============================================================
# TEST: GIỎ HÀNG
# Mục tiêu: giỏ giữ sản phẩm sau reload; xoá sản phẩm; Continue Shopping; Reset App State.
# Dữ liệu: data/cart/cart.json
# Lưu ý: Reset App State xoá badge + localStorage nhưng nút trên trang chỉ đổi sau reload
#        (hành vi gốc của site, xem docs/site-survey.md mục 1).
# ============================================================
import pytest

from utils.assertions import poll_until
from utils.cases import case_params
from utils.data_loader import load_data
from utils.routes import ROUTES
from utils.storage import read_cart

DATA = load_data("cart/cart.json")


@pytest.fixture(autouse=True)
def open_inventory(po):
    po.inventory.open()


def assert_cart_storage(driver, product_ids):
    """localStorage "cart-contents" chứa đúng các id sản phẩm (không xét thứ tự)."""
    expected = sorted(product_ids)
    poll_until(lambda: sorted(read_cart(driver)) == expected, f"cart-contents khác {expected}: {read_cart(driver)}")


@pytest.mark.parametrize("case", case_params(DATA["persist"]))
def test_cart_persists_after_reload(po, case):
    po.inventory.add_all_to_cart(case["products"])
    po.header.open_cart()
    po.cart.reload()
    assert po.cart.names() == case["products"]
    assert po.header.cart_badge() == len(case["products"])
    assert_cart_storage(po.driver, case["ids"])


@pytest.mark.parametrize("case", case_params(DATA["remove"]))
def test_remove_from_cart(po, case):
    po.inventory.add_all_to_cart(case["products"])
    po.header.open_cart()
    po.cart.remove(case["remove"])
    assert po.cart.names() == case["remaining"]
    assert po.header.cart_badge() == len(case["remaining"])
    assert_cart_storage(po.driver, case["remainingIds"])


@pytest.mark.parametrize("case", case_params(DATA["continueShopping"]))
def test_continue_shopping(po, case):
    po.inventory.add_all_to_cart(case["products"])
    po.header.open_cart()
    po.cart.continue_shopping()
    assert po.inventory.current_path() == ROUTES["inventory"]
    assert po.header.cart_badge() == len(case["products"])


@pytest.mark.parametrize("case", case_params(DATA["reset"]))
def test_reset_app_state(po, case):
    po.inventory.add_all_to_cart(case["products"])
    assert po.header.cart_badge() == len(case["products"])
    po.menu.reset_app_state()
    assert po.header.cart_badge() == 0
    assert_cart_storage(po.driver, [])
    po.inventory.reload()
    for name in case["products"]:
        assert po.inventory.button_text(name) == "Add to cart"
