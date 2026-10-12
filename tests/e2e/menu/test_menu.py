# ============================================================
# TEST: MENU BURGER
# Mục tiêu: đủ mục menu, About trỏ đúng địa chỉ, All Items quay về danh sách.
# (Logout ở tests/e2e/auth/test_logout.py, Reset App State ở tests/e2e/cart/test_cart.py.)
# Dữ liệu: data/inventory/menu.json
# ============================================================
import pytest

from utils.cases import case_params
from utils.data_loader import load_data
from utils.routes import ROUTES

DATA = load_data("inventory/menu.json")


@pytest.fixture(autouse=True)
def open_inventory(k):
    k.inventory.open_inventory()


@pytest.mark.parametrize("case", case_params(DATA["items"]))
def test_menu_items(k, case):
    k.menu.open_menu()
    k.menu.verify_menu_items(case["items"])
    k.menu.verify_about_link(case["aboutHref"])
    k.menu.close_menu()


@pytest.mark.parametrize("case", case_params(DATA["allItems"]))
def test_all_items(k, case):
    if "fromProductId" in case:
        k.product.open_product_by_id(case["fromProductId"])
    else:
        k.cart.open_cart()
    k.menu.goto_all_items()
    k.common.verify_url(ROUTES["inventory"])
