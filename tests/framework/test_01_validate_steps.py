# ============================================================
# UNIT: drivers/driver_script.validate_steps + execute_steps (không mở browser)
# Mục tiêu: kịch bản sai schema / sai thứ tự / keyword lạ / thiếu verify bị từ chối TRƯỚC khi chạy UI;
#           execute_steps thay biến runtime, gọi đúng keyword và gắn ngữ cảnh vào lỗi.
# ============================================================
from copy import deepcopy

import pytest

from drivers.driver_script import execute_steps, is_check_step, validate_steps


def _row(step, keyword, args=None, note=""):
    return {"case_id": "TC-01", "step": str(step), "keyword": keyword, "args": args or [], "note": note}


STEPS = [
    _row(1, "auth.loginAs", ["standard_user"]),
    _row(2, "inventory.addProductToCart", ["Sauce Labs Onesie"]),
    _row(3, "common.verifyCartBadge", [1]),
]


def test_valid_steps_pass():
    assert validate_steps(deepcopy(STEPS)) == STEPS


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda s: s[1].pop("note"), "sai schema"),
        (lambda s: s[1].update(extra=1), "sai schema"),
        (lambda s: s[1].update(step="3"), "thứ tự step"),
        (lambda s: s[2].update(case_id="TC-02"), "case_id"),
        (lambda s: s[1].update(keyword="inventory.addToCartt"), "keyword chưa khai báo"),
        (lambda s: s[1].update(args="Sauce Labs Onesie"), "args phải là mảng"),
        (lambda s: s[1].update(note=None), "note phải là chuỗi"),
    ],
)
def test_invalid_steps_rejected(mutate, message):
    steps = deepcopy(STEPS)
    mutate(steps)
    with pytest.raises(ValueError, match=message):
        validate_steps(steps)


@pytest.mark.parametrize("steps", [[], None, "abc"])
def test_empty_scenario_rejected(steps):
    with pytest.raises(ValueError, match="không có bước"):
        validate_steps(steps)


def test_scenario_needs_check_step():
    with pytest.raises(ValueError, match="bước kiểm tra"):
        validate_steps(deepcopy(STEPS[:2]))


@pytest.mark.parametrize(
    ("name", "expected"),
    [("common.verifyUrl", True), ("auth.loginExpectingError", True), ("auth.login", False)],
)
def test_is_check_step(name, expected):
    assert is_check_step(name) is expected


class FakeKeywords:
    """Thay cho Keywords thật: ghi lại lời gọi, bước "verify" ném AssertionError khi được yêu cầu."""

    def __init__(self, fail_on=None):
        self.calls, self.fail_on = [], fail_on

    def resolve(self, name):
        def call(*args):
            self.calls.append((name, args))
            if name == self.fail_on:
                raise AssertionError("badge sai")
        return call


def test_execute_resolves_runtime_variables():
    steps = deepcopy(STEPS)
    steps[0]["args"] = ["${user}"]
    k = FakeKeywords()
    execute_steps(k, steps, {"user": "standard_user"})
    assert k.calls[0] == ("auth.loginAs", ("standard_user",))
    assert [name for name, _ in k.calls] == [row["keyword"] for row in STEPS]


def test_execute_reraises_with_context():
    k = FakeKeywords(fail_on="common.verifyCartBadge")
    with pytest.raises(AssertionError) as info:
        execute_steps(k, deepcopy(STEPS), {})
    assert any("step 3" in note and "ASSERTION_FAILED" in note for note in info.value.__notes__)
