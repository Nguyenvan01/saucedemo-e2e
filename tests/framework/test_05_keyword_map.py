# ============================================================
# UNIT: keywords.KEYWORD_MAP - registry tường minh "nhóm.tenCamelCase" -> (nhóm, method).
# ============================================================
import inspect
import re

import pytest

from keywords import GROUPS, KEYWORD_MAP, Keywords, build_keyword_map
from keywords.base_keywords import BaseKeywords, keyword

EXPECTED_GROUPS = ["common", "auth", "inventory", "product", "cart", "checkout", "menu"]


def test_groups():
    assert [klass.group for _, klass in GROUPS] == EXPECTED_GROUPS
    assert [attr for attr, _ in GROUPS] == EXPECTED_GROUPS


def test_every_keyword_is_camel_case_and_documented():
    for full_name, (attr, method_name) in KEYWORD_MAP.items():
        group, name = full_name.split(".")
        assert re.fullmatch(r"[a-z][a-zA-Z0-9]*", name), full_name
        klass = dict(GROUPS)[attr]
        method = getattr(klass, method_name)
        assert (inspect.getdoc(method) or "").strip(), f"{full_name} thiếu docstring"


def test_every_group_has_a_verify_keyword():
    for group in EXPECTED_GROUPS:
        assert any(name.startswith(f"{group}.verify") for name in KEYWORD_MAP), group


def test_duplicate_keyword_rejected():
    class A(BaseKeywords):
        group = "dup"

        @keyword("same")
        def one(self):
            """1."""

    class B(BaseKeywords):
        group = "dup"

        @keyword("same")
        def two(self):
            """2."""

    with pytest.raises(ValueError, match="trùng tên"):
        build_keyword_map((("a", A), ("b", B)))


def test_group_required():
    class NoGroup(BaseKeywords):
        pass

    with pytest.raises(ValueError, match="chưa khai báo group"):
        build_keyword_map((("x", NoGroup),))


def test_resolve_binds_method_without_browser():
    # Page Object chỉ tạo Locator (lazy) -> dùng object giả thay cho page thật.
    class FakePage:
        def __getattr__(self, name):
            return lambda *args, **kwargs: None

    k = Keywords(FakePage())
    assert k.resolve("cart.openCart").__func__ is type(k.cart).open_cart
    with pytest.raises(ValueError, match="Keyword không tồn tại"):
        k.resolve("cart.nope")
