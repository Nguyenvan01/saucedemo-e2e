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

DATA = load_data("inventory/products.json")
SORTS = load_data("inventory/sorting.json#cases")


@pytest.fixture(autouse=True)
def open_inventory(k):
    k.inventory.open_inventory()


@pytest.mark.parametrize("case", case_params(DATA["listing"]))
def test_product_listing(k, ctx, case):
    c = resolve_data(case, ctx)
    k.inventory.verify_product_count(len(c["names"]))
    k.inventory.verify_product_names(c["names"])
    k.inventory.verify_product_prices(c["prices"])


@pytest.mark.parametrize("case", case_params(SORTS))
def test_sort(k, ctx, case):
    sort = resolve_data(case, ctx)["sort"]
    k.inventory.sort_products_by(sort["label"])
    k.inventory.verify_active_sort(sort["label"])
    k.inventory.verify_product_names(sort["names"])
    k.inventory.verify_product_prices(sort["prices"])


@pytest.mark.parametrize("case", case_params(DATA["addRemove"]))
def test_add_remove_updates_badge(k, case):
    for count, name in enumerate(case["add"], 1):
        k.inventory.add_product_to_cart(name)
        k.common.verify_cart_badge(count)
        k.inventory.verify_product_button_state(name, "Remove")
    k.inventory.remove_product_from_inventory(case["remove"])
    k.common.verify_cart_badge(len(case["add"]) - 1)
    k.inventory.verify_product_button_state(case["remove"], "Add to cart")
    k.common.verify_cart_storage(case["remainingIds"])


@pytest.mark.parametrize("case", case_params(DATA["detail"]))
def test_open_product_detail(k, case):
    k.inventory.open_product_detail(case["name"])
    k.common.verify_url(product_route(case["productId"]))
    k.product.verify_product_detail(case["name"], case["price"])
    k.product.add_to_cart_from_detail()
    k.common.verify_cart_badge(1)
    k.product.back_to_products()
    k.inventory.verify_product_button_state(case["name"], "Remove")
