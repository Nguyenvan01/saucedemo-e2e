# ============================================================
# TEST: GIỎ HÀNG
# Mục tiêu: giỏ giữ sản phẩm sau reload; xoá sản phẩm; Continue Shopping; Reset App State.
# Dữ liệu: data/cart/cart.json
# Lưu ý: Reset App State xoá badge + localStorage nhưng nút trên trang chỉ đổi sau reload
#        (hành vi gốc của site, xem docs/site-survey.md mục 1).
# ============================================================
import pytest

from utils.cases import case_params
from utils.data_loader import load_data
from utils.routes import ROUTES

DATA = load_data("cart/cart.json")


@pytest.fixture(autouse=True)
def open_inventory(k):
    k.inventory.open_inventory()


@pytest.mark.parametrize("case", case_params(DATA["persist"]))
def test_cart_persists_after_reload(k, case):
    k.inventory.add_products_to_cart(case["products"])
    k.cart.open_cart()
    k.common.reload_page()
    k.cart.verify_cart_items(case["products"])
    k.common.verify_cart_badge(len(case["products"]))
    k.common.verify_cart_storage(case["ids"])


@pytest.mark.parametrize("case", case_params(DATA["remove"]))
def test_remove_from_cart(k, case):
    k.inventory.add_products_to_cart(case["products"])
    k.cart.open_cart()
    k.cart.remove_from_cart(case["remove"])
    k.cart.verify_cart_items(case["remaining"])
    k.common.verify_cart_badge(len(case["remaining"]))
    k.common.verify_cart_storage(case["remainingIds"])


@pytest.mark.parametrize("case", case_params(DATA["continueShopping"]))
def test_continue_shopping(k, case):
    k.inventory.add_products_to_cart(case["products"])
    k.cart.open_cart()
    k.cart.continue_shopping()
    k.common.verify_url(ROUTES["inventory"])
    k.common.verify_cart_badge(len(case["products"]))


@pytest.mark.parametrize("case", case_params(DATA["reset"]))
def test_reset_app_state(k, case):
    k.inventory.add_products_to_cart(case["products"])
    k.common.verify_cart_badge(len(case["products"]))
    k.menu.reset_app_state()
    k.common.verify_cart_badge(0)
    k.common.verify_cart_storage([])
    k.common.reload_page()
    for name in case["products"]:
        k.inventory.verify_product_button_state(name, "Add to cart")
