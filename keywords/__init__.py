# ============================================================
# THƯ VIỆN KEYWORD (tầng nghiệp vụ). Dùng trong test qua fixture `k`:
#     k.inventory.add_product_to_cart("Sauce Labs Onesie")
#     k.common.verify_cart_badge(1)
# Kịch bản Excel gọi cùng các keyword này bằng tên "nhóm.tenCamelCase", vd: "common.verifyCartBadge".
# KEYWORD_MAP là registry tường minh: tên keyword -> (thuộc tính nhóm, tên method).
# ============================================================
from keywords.kw_auth import AuthKeywords
from keywords.kw_cart import CartKeywords
from keywords.kw_checkout import CheckoutKeywords
from keywords.kw_common import CommonKeywords
from keywords.kw_inventory import InventoryKeywords
from keywords.kw_menu import MenuKeywords
from keywords.kw_product import ProductKeywords
from pages.page_objects import PageObjects

# (thuộc tính trên Keywords, lớp keyword). Thứ tự = thứ tự trong KEYWORDS.md.
GROUPS = (
    ("common", CommonKeywords),
    ("auth", AuthKeywords),
    ("inventory", InventoryKeywords),
    ("product", ProductKeywords),
    ("cart", CartKeywords),
    ("checkout", CheckoutKeywords),
    ("menu", MenuKeywords),
)


def build_keyword_map(groups=GROUPS):
    keyword_map = {}
    for attr, klass in groups:
        if not klass.group:
            raise ValueError(f"{klass.__name__} chưa khai báo group")
        for name, method in klass.keywords().items():
            full_name = f"{klass.group}.{name}"
            if full_name in keyword_map:
                raise ValueError(f"Keyword trùng tên: {full_name}")
            keyword_map[full_name] = (attr, method)
    return keyword_map


KEYWORD_MAP = build_keyword_map()


class Keywords:
    def __init__(self, page):
        self.page = page
        self.po = PageObjects(page)
        for attr, klass in GROUPS:
            setattr(self, attr, klass(page, self.po))

    def resolve(self, name):
        """Tìm keyword theo tên "nhóm.tenCamelCase" -> method đã bind sẵn."""
        if name not in KEYWORD_MAP:
            raise ValueError(f'Keyword không tồn tại: "{name}". Xem danh sách trong KEYWORDS.md')
        attr, method = KEYWORD_MAP[name]
        return getattr(getattr(self, attr), method)
