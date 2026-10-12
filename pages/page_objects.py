# Gom toàn bộ Page Object của 1 `page` - tầng Keyword dùng qua đây (k.po.header, k.po.cart...).
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.components.burger_menu import BurgerMenu
from pages.components.header import Header
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage


class PageObjects:
    def __init__(self, page):
        self.page = page
        self.base = BasePage(page)
        self.header = Header(page)
        self.menu = BurgerMenu(page)
        self.login = LoginPage(page)
        self.inventory = InventoryPage(page)
        self.product = ProductDetailPage(page)
        self.cart = CartPage(page)
        self.checkout_info = CheckoutInfoPage(page)
        self.checkout_overview = CheckoutOverviewPage(page)
        self.checkout_complete = CheckoutCompletePage(page)
