# Gom toàn bộ Page Object của 1 WebDriver - test dùng qua fixture `po` (po.login, po.cart...).
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
    def __init__(self, driver):
        self.driver = driver
        self.base = BasePage(driver)
        self.header = Header(driver)
        self.menu = BurgerMenu(driver)
        self.login = LoginPage(driver)
        self.inventory = InventoryPage(driver)
        self.product = ProductDetailPage(driver)
        self.cart = CartPage(driver)
        self.checkout_info = CheckoutInfoPage(driver)
        self.checkout_overview = CheckoutOverviewPage(driver)
        self.checkout_complete = CheckoutCompletePage(driver)
