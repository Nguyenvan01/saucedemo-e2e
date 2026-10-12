# ============================================================
# UNIT: utils/template_binding + utils/hybrid_reader (không mở browser)
# Mục tiêu: lỗi binding {cot} / join TestSteps-TestData / schema bị phát hiện lúc collection.
# Biến runtime ${...} không bị binding đụng tới; template dùng lại không bị sửa.
# ============================================================
from copy import deepcopy

import pytest

from utils.hybrid_reader import build_cases
from utils.template_binding import bind_template, parse_args


def _step(number, keyword, args, note=""):
    return {"template_id": "T-CART", "step": str(number), "keyword": keyword, "args": args, "note": note}


TEMPLATE = [
    _step(1, "auth.loginAs", ["{user}"]),
    _step(2, "inventory.addProductToCart", ["{product}"]),
    _step(3, "common.verifyCartBadge", ["{badge}"]),
    _step(4, "common.verifyErrorMessage", ["${msg.login.lockedOut}"], "biến runtime"),
]
CASE = {
    "case_id": "CART-01",
    "template_id": "T-CART",
    "title": "Thêm 1 sản phẩm",
    "tags": "@smoke",
    "requires": "password",
    "known_bug": "",
    "user": "standard_user",
    "product": "Sauce Labs Onesie",
    "badge": "1",
}


def test_bind_one_case():
    steps = bind_template(TEMPLATE, CASE)
    assert steps[1]["args"] == ["Sauce Labs Onesie"]
    assert steps[1]["case_id"] == "CART-01"
    assert steps[3]["args"] == ["${msg.login.lockedOut}"]
    assert TEMPLATE[1]["args"] == ["{product}"]


def test_missing_placeholder():
    case = {key: value for key, value in CASE.items() if key != "product"}
    with pytest.raises(ValueError, match="thiếu placeholder product"):
        bind_template(TEMPLATE, case)


@pytest.mark.parametrize("value", ["{missing}", "{product", "name:{product}"])
def test_invalid_placeholder(value):
    template = deepcopy(TEMPLATE)
    template[1]["args"] = [value]
    with pytest.raises(ValueError, match="[Pp]laceholder"):
        bind_template(template, CASE)


def test_unknown_keyword_rejected():
    template = deepcopy(TEMPLATE)
    template[0]["keyword"] = "auth.loginAss"
    with pytest.raises(ValueError, match="Keyword chưa khai báo"):
        bind_template(template, CASE)


def test_wrong_step_order_rejected():
    template = deepcopy(TEMPLATE)
    template[1]["step"] = "5"
    with pytest.raises(ValueError, match="thứ tự step"):
        bind_template(template, CASE)


def test_binding_is_independent():
    original = deepcopy(TEMPLATE)
    first = bind_template(TEMPLATE, CASE)
    second = bind_template(TEMPLATE, {**CASE, "case_id": "CART-02", "product": "Sauce Labs Backpack"})
    first[1]["args"][0] = "khác"
    assert second[1]["args"][0] == "Sauce Labs Backpack"
    assert TEMPLATE == original


def test_build_cases_meta_and_join():
    other = [{**row, "template_id": "T-OTHER"} for row in TEMPLATE]
    cases = build_cases(
        TEMPLATE + other,
        [CASE, {**CASE, "case_id": "OTHER-01", "template_id": "T-OTHER", "known_bug": "Sort hỏng"}],
    )
    assert [case["id"] for case in cases] == ["CART-01", "OTHER-01"]
    assert cases[0]["tags"] == ["@smoke"] and cases[0]["requires"] == ["password"]
    assert cases[0]["knownBug"] is None and cases[1]["knownBug"] == "Sort hỏng"


@pytest.mark.parametrize(
    ("rows", "message"),
    [
        (lambda: [CASE, CASE.copy()], "trùng"),
        (lambda: [{**CASE, "template_id": "MISSING"}], "Template không tồn tại"),
        (lambda: [{**CASE, "title": ""}], "thiếu title"),
        (lambda: [{**CASE, "badge": None}], "giá trị chuỗi"),
    ],
)
def test_build_cases_rejects_bad_data(rows, message):
    with pytest.raises(ValueError, match=message):
        build_cases(TEMPLATE, rows())


def test_unused_template_rejected():
    other = [{**row, "template_id": "T-OTHER"} for row in TEMPLATE]
    with pytest.raises(ValueError, match="Template chưa có dữ liệu"):
        build_cases(TEMPLATE + other, [CASE])


@pytest.mark.parametrize(
    ("text", "expected"),
    [("", []), ('["Sauce Labs Onesie", 2]', ["Sauce Labs Onesie", 2]), ("[[]]", [[]])],
)
def test_parse_args(text, expected):
    assert parse_args(text, "test") == expected


@pytest.mark.parametrize("text", ["{", '"chuỗi"', '{"a": 1}'])
def test_parse_args_rejects(text):
    with pytest.raises(ValueError, match="args"):
        parse_args(text, "test")
