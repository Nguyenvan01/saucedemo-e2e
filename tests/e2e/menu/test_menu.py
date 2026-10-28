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
def open_inventory(po):
    po.inventory.open()


@pytest.mark.parametrize("case", case_params(DATA["items"]))
def test_menu_items(po, case):
    po.menu.open_menu()
    assert po.menu.item_texts(case["items"]) == case["items"]
    assert po.menu.about_href() == case["aboutHref"]
    po.menu.close_menu()


@pytest.mark.parametrize("case", case_params(DATA["allItems"]))
def test_all_items(po, case):
    if "fromProductId" in case:
        po.product.open_by_id(case["fromProductId"])
    else:
        po.header.open_cart()
    po.menu.all_items()
    assert po.inventory.current_path() == ROUTES["inventory"]
