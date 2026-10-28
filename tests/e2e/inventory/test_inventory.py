# ============================================================
# TEST: DANH SÁCH SẢN PHẨM
# Mục tiêu: đủ 6 sản phẩm; 4 kiểu sắp xếp đúng thứ tự; thêm/bỏ cập nhật badge + localStorage;
#           mở chi tiết đúng sản phẩm. Lỗi cố ý của problem/error/visual_user -> knownBug (xfail).
# Dữ liệu: data/inventory/products.json, data/inventory/sorting.json
# ============================================================
import pytest

from utils.cases import case_params
from utils.data_loader import load_data, resolve_data
from utils.routes import product_route
from utils.storage import read_cart

DATA = load_data("inventory/products.json")
SORTS = load_data("inventory/sorting.json#cases")


@pytest.fixture(autouse=True)
def open_inventory(po):
    po.inventory.open()


@pytest.mark.parametrize("case", case_params(DATA["listing"]))
def test_product_listing(po, ctx, case):
    c = resolve_data(case, ctx)
    assert po.inventory.product_count() == len(c["names"])
    assert po.inventory.names() == c["names"]
    assert po.inventory.prices() == c["prices"]


@pytest.mark.parametrize("case", case_params(SORTS))
def test_sort(po, ctx, case):
    sort = resolve_data(case, ctx)["sort"]
    po.inventory.sort_by(sort["label"])
    assert po.inventory.active_sort() == sort["label"]
    assert po.inventory.names() == sort["names"]
    assert po.inventory.prices() == sort["prices"]


@pytest.mark.parametrize("case", case_params(DATA["addRemove"]))
def test_add_remove_updates_badge(po, case):
    for count, name in enumerate(case["add"], 1):
        po.inventory.add_to_cart(name)
        assert po.header.cart_badge() == count
        assert po.inventory.button_text(name) == "Remove"
    po.inventory.remove_from_cart(case["remove"])
    assert po.header.cart_badge() == len(case["add"]) - 1
    assert po.inventory.button_text(case["remove"]) == "Add to cart"
    assert sorted(read_cart(po.driver)) == sorted(case["remainingIds"])


@pytest.mark.parametrize("case", case_params(DATA["detail"]))
def test_open_product_detail(po, case):
    detail = po.inventory.open_product(case["name"])
    assert detail.current_path() == product_route(case["productId"])
    assert detail.name() == case["name"]
    assert detail.price() == case["price"]
    detail.add_to_cart()
    assert po.header.cart_badge() == 1
    detail.back_to_products()
    assert po.inventory.button_text(case["name"]) == "Remove"
