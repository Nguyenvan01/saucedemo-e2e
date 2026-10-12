# Chuỗi hiển thị trên UI, lấy NGUYÊN VĂN từ trang thật (xem docs/site-survey.md).
# Đổi text ở app thì chỉ sửa tại đây. Dữ liệu tham chiếu bằng biến runtime "${msg.login.lockedOut}".
MSG = {
    "login": {
        "usernameRequired": "Epic sadface: Username is required",
        "passwordRequired": "Epic sadface: Password is required",
        "wrongCredentials": "Epic sadface: Username and password do not match any user in this service",
        "lockedOut": "Epic sadface: Sorry, this user has been locked out.",
    },
    "checkout": {
        "firstNameRequired": "Error: First Name is required",
        "lastNameRequired": "Error: Last Name is required",
        "postalCodeRequired": "Error: Postal Code is required",
        "completeHeader": "Thank you for your order!",
        "completeText": "Your order has been dispatched, and will arrive just as fast as the pony can get there!",
    },
    "title": {
        "inventory": "Products",
        "cart": "Your Cart",
        "checkoutInfo": "Checkout: Your Information",
        "checkoutOverview": "Checkout: Overview",
        "checkoutComplete": "Checkout: Complete!",
    },
    # Mở trang cần đăng nhập khi chưa có phiên (path là pathname, không kèm query).
    "loginRequired": {
        "inventory": "Epic sadface: You can only access '/inventory.html' when you are logged in.",
        "cart": "Epic sadface: You can only access '/cart.html' when you are logged in.",
        "checkoutInfo": "Epic sadface: You can only access '/checkout-step-one.html' when you are logged in.",
        "product": "Epic sadface: You can only access '/inventory-item.html' when you are logged in.",
    },
}
