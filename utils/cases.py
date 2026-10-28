# ============================================================
# CASE META: biến 1 test case dữ liệu thành pytest item.
# - id        -> id của pytest item (hiện trong report, chọn bằng -k)
# - requires  -> skip nếu thiếu điều kiện (mật khẩu trong .env)
# - knownBug  -> xfail(strict=True): lỗi cố ý của app; nếu test PASS thì báo "bug đã sửa?"
# - tags      -> marker pytest, vd: "@smoke" -> pytest.mark.smoke
# - session   -> marker role(user): mở test với phiên đăng nhập sẵn (cookie) của user đó
# ============================================================
import pytest

from config import PASSWORD

REQUIREMENTS = {
    "password": lambda: None if PASSWORD else "Cần SAUCE_PASSWORD trong .env",
}
TAG_MARKS = {"@smoke": pytest.mark.smoke}


def missing_requirement(requires=None):
    """Lý do skip nếu thiếu điều kiện, None nếu đủ."""
    for name in requires or []:
        if name not in REQUIREMENTS:
            raise ValueError(f"requires không hợp lệ: {name!r}; chọn {sorted(REQUIREMENTS)}")
        reason = REQUIREMENTS[name]()
        if reason:
            return reason
    return None


def case_marks(case):
    marks = []
    reason = missing_requirement(case.get("requires"))
    if reason:
        marks.append(pytest.mark.skip(reason=reason))
    if case.get("knownBug"):
        marks.append(pytest.mark.xfail(strict=True, reason=f"BUG: {case['knownBug']}"))
    if case.get("session"):
        marks.append(pytest.mark.role(case["session"]))
    for tag in case.get("tags") or []:
        if tag not in TAG_MARKS:
            raise ValueError(f"Case {case.get('id')}: tag chưa khai báo: {tag}")
        marks.append(TAG_MARKS[tag])
    return marks


def case_param(case):
    """Một data row -> một pytest.param có id và marker riêng."""
    if not case.get("id"):
        raise ValueError(f"Case thiếu id: {case!r}")
    return pytest.param(case, id=case["id"], marks=case_marks(case))


def case_params(cases):
    params = [case_param(case) for case in cases]
    ids = [param.id for param in params]
    duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicates:
        raise ValueError(f"case id trùng: {duplicates}")
    return params


def case_title(case):
    """Tên hiển thị chuẩn cho 1 case dữ liệu: "[ID] Tiêu đề"."""
    return f"[{case['id']}] {case['title']}"
