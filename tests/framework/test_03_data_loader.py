# ============================================================
# UNIT: utils/data_loader (resolve_data, load_data, mask_secrets), utils/cases, utils/storage,
#       utils/assertions.money (không mở browser)
# ============================================================
import json
from decimal import Decimal

import pytest

import utils.data_loader as data_loader
from utils.assertions import money
from utils.cases import case_params
from utils.data_loader import base_context, load_data, mask_secrets, resolve_data
from utils.storage import session_seconds_left

CTX = {"user": {"name": "standard_user", "count": 2}, "flag": True, "items": ["a", "b"]}


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("${user.count}", 2),  # cả chuỗi là 1 biến -> giữ kiểu
        ("Xin chào ${user.name}", "Xin chào standard_user"),
        ("${flag}/${items.1}", "true/b"),
        (["${user.name}", {"n": "${user.count}"}, 3], ["standard_user", {"n": 2}, 3]),
        ("không có biến", "không có biến"),
    ],
)
def test_resolve_data(value, expected):
    assert resolve_data(value, CTX) == expected


def test_resolve_unknown_variable():
    with pytest.raises(ValueError, match="user.missing"):
        resolve_data("${user.missing}", CTX)


def test_resolve_uid_is_unique():
    assert resolve_data("${uid}", {}) != resolve_data("${uid}", {})


def test_resolve_messages_from_base_context():
    assert resolve_data("${msg.login.lockedOut}", base_context()) == "Epic sadface: Sorry, this user has been locked out."


@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(data_loader, "DATA_DIR", tmp_path)
    monkeypatch.setattr(data_loader, "_cache", {})
    (tmp_path / "x.json").write_text(json.dumps({"a": {"b": [10, {"c": "ok"}]}}), encoding="utf-8")
    return tmp_path


def test_load_data_pointer_and_copy(data_dir):
    assert load_data("x.json#a.b.1.c") == "ok"
    first = load_data("x.json")
    first["a"]["b"][0] = 99
    assert load_data("x.json#a.b.0") == 10


def test_load_data_via_reference(data_dir):
    assert resolve_data(["@data:x.json#a.b.0"], {}) == [10]


@pytest.mark.parametrize("ref", ["missing.json", "x.json#a.z"])
def test_load_data_errors(data_dir, ref):
    with pytest.raises(ValueError):
        load_data(ref)


def test_mask_secrets():
    assert mask_secrets("login(standard_user, s3cret)", ["s3cret"]) == "login(standard_user, ***)"
    assert mask_secrets("không đổi", [""]) == "không đổi"


def test_case_params_marks():
    params = case_params([
        {"id": "A", "tags": ["@smoke"]},
        {"id": "B", "knownBug": "Sort hỏng", "session": "problem_user"},
    ])
    assert [p.id for p in params] == ["A", "B"]
    assert params[0].marks[0].name == "smoke"
    xfail, role = params[1].marks
    assert xfail.name == "xfail" and xfail.kwargs["strict"] is True
    assert role.name == "role" and role.args == ("problem_user",)


@pytest.mark.parametrize(
    ("cases", "message"),
    [
        ([{"id": "A"}, {"id": "A"}], "trùng"),
        ([{"title": "thiếu id"}], "thiếu id"),
        ([{"id": "A", "tags": ["@lạ"]}], "tag chưa khai báo"),
        ([{"id": "A", "requires": ["admin"]}], "requires không hợp lệ"),
    ],
)
def test_case_params_rejects(cases, message):
    with pytest.raises(ValueError, match=message):
        case_params(cases)


def test_session_seconds_left():
    assert session_seconds_left(None) == 0
    cookie = {"name": "session-username", "value": "u", "expiry": 1600}
    assert session_seconds_left(cookie, now=1000) == 600
    assert session_seconds_left(cookie, now=2000) == 0


@pytest.mark.parametrize(
    ("text", "expected"),
    [("$29.99", Decimal("29.99")), ("Total: $32.39", Decimal("32.39")), ("$11.7", Decimal("11.7"))],
)
def test_money(text, expected):
    assert money(text) == expected


def test_money_rejects():
    with pytest.raises(ValueError):
        money("không có tiền")
