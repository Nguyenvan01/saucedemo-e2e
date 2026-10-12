# Đường dẫn các trang của app (tương đối với BASE_URL).
ROUTES = {
    "login": "/",
    "inventory": "/inventory.html",
    "product": "/inventory-item.html",
    "cart": "/cart.html",
    "checkoutInfo": "/checkout-step-one.html",
    "checkoutOverview": "/checkout-step-two.html",
    "checkoutComplete": "/checkout-complete.html",
}


def product_route(product_id):
    return f"{ROUTES['product']}?id={product_id}"
