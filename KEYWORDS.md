# Danh mục Keyword

> File tự sinh bởi `.venv/bin/python scripts/gen_keywords_doc.py` — đừng sửa tay.

Dùng trong code (pytest): `k.<nhóm>.<keyword_snake_case>(...)`, vd: `k.common.verify_cart_badge(2)` · Dùng trong kịch bản Excel: cột `keyword` = `<nhóm>.<keywordCamelCase>`, vd: `common.verifyCartBadge`.

Kịch bản nằm trong `data/scenarios/*.xlsx`, mỗi file có 2 sheet:

- `TestSteps`: `template_id | step | keyword | args | note` — `args` là mảng JSON, vd: `[2]`, `["Sauce Labs Onesie"]`, `["${msg.login.lockedOut}"]`.
- `TestData`: `case_id | template_id | title | tags | requires | known_bug | <cột placeholder>` — mỗi dòng là 1 test case, giá trị cột placeholder thay vào placeholder `{tên_cột}` trong `args` lúc collection; `${...}` là biến runtime.

## common

| Keyword | Python | Tham số | Mô tả |
|---|---|---|---|
| `common.openPage` | `k.common.open_page(path)` | `path` | Mở trang theo đường dẫn tương đối, vd "/cart.html". |
| `common.reloadPage` | `k.common.reload_page()` | — | Tải lại trang hiện tại. |
| `common.verifyUrl` | `k.common.verify_url(path)` | `path` | Kiểm tra URL hiện tại đúng bằng BASE_URL + path. |
| `common.verifyPageTitle` | `k.common.verify_page_title(title)` | `title` | Kiểm tra tiêu đề trang (data-test="title"), vd "Your Cart". |
| `common.verifyErrorMessage` | `k.common.verify_error_message(message)` | `message` | Kiểm tra khung lỗi (login / checkout) hiện đúng nguyên văn thông báo. |
| `common.verifyNoErrorMessage` | `k.common.verify_no_error_message()` | — | Kiểm tra không còn khung lỗi trên trang. |
| `common.verifyCartBadge` | `k.common.verify_cart_badge(count)` | `count` | Kiểm tra số trên icon giỏ; 0 = không hiện badge. |
| `common.verifyCartStorage` | `k.common.verify_cart_storage(product_ids)` | `product_ids` | Kiểm tra localStorage "cart-contents" chứa đúng các id sản phẩm (không xét thứ tự). |

## auth

| Keyword | Python | Tham số | Mô tả |
|---|---|---|---|
| `auth.openLogin` | `k.auth.open_login()` | — | Mở trang đăng nhập. |
| `auth.login` | `k.auth.login(username, password)` | `username, password` | Nhập username + mật khẩu và bấm Login (không chờ kết quả). |
| `auth.loginAs` | `k.auth.login_as(username)` | `username` | Đăng nhập bằng mật khẩu chung trong .env và chờ danh sách sản phẩm hiện ra. |
| `auth.loginExpectingError` | `k.auth.login_expecting_error(username, password, message)` | `username, password, message` | Đăng nhập và chờ thông báo lỗi đúng nguyên văn, vẫn ở trang login. |
| `auth.dismissError` | `k.auth.dismiss_error()` | — | Bấm nút X để đóng khung lỗi đăng nhập. |
| `auth.verifyLoginFormDisplayed` | `k.auth.verify_login_form_displayed()` | — | Kiểm tra form đăng nhập hiển thị (username, password, nút Login). |
| `auth.verifyLoginFieldsHighlighted` | `k.auth.verify_login_fields_highlighted()` | — | Kiểm tra ô username và password được đánh dấu lỗi (class "error"). |
| `auth.verifyLoggedIn` | `k.auth.verify_logged_in()` | — | Kiểm tra đã vào trang danh sách sản phẩm sau đăng nhập. |

## inventory

| Keyword | Python | Tham số | Mô tả |
|---|---|---|---|
| `inventory.openInventory` | `k.inventory.open_inventory()` | — | Mở trang danh sách sản phẩm (cần phiên đăng nhập). |
| `inventory.verifyProductCount` | `k.inventory.verify_product_count(count)` | `count` | Kiểm tra số sản phẩm hiển thị. |
| `inventory.verifyProductNames` | `k.inventory.verify_product_names(names)` | `names` | Kiểm tra tên sản phẩm theo ĐÚNG thứ tự hiển thị. |
| `inventory.verifyProductPrices` | `k.inventory.verify_product_prices(prices)` | `prices` | Kiểm tra giá sản phẩm theo đúng thứ tự hiển thị, vd ["$7.99", "$9.99"]. |
| `inventory.verifyProductPrice` | `k.inventory.verify_product_price(name, price)` | `name, price` | Kiểm tra giá của 1 sản phẩm trên danh sách. |
| `inventory.sortProductsBy` | `k.inventory.sort_products_by(label)` | `label` | Chọn kiểu sắp xếp theo nhãn, vd "Price (low to high)". |
| `inventory.verifyActiveSort` | `k.inventory.verify_active_sort(label)` | `label` | Kiểm tra nhãn kiểu sắp xếp đang chọn. |
| `inventory.addProductToCart` | `k.inventory.add_product_to_cart(name)` | `name` | Bấm "Add to cart" của 1 sản phẩm trên danh sách. |
| `inventory.addProductsToCart` | `k.inventory.add_products_to_cart(names)` | `names` | Bấm "Add to cart" lần lượt cho nhiều sản phẩm. |
| `inventory.removeProductFromInventory` | `k.inventory.remove_product_from_inventory(name)` | `name` | Bấm "Remove" của 1 sản phẩm ngay trên danh sách. |
| `inventory.verifyProductButtonState` | `k.inventory.verify_product_button_state(name, text)` | `name, text` | Kiểm tra nút của sản phẩm đang là "Add to cart" hay "Remove". |
| `inventory.openProductDetail` | `k.inventory.open_product_detail(name)` | `name` | Bấm tên sản phẩm để mở trang chi tiết. |

## product

| Keyword | Python | Tham số | Mô tả |
|---|---|---|---|
| `product.openProductById` | `k.product.open_product_by_id(product_id)` | `product_id` | Mở thẳng trang chi tiết /inventory-item.html?id=N. |
| `product.verifyProductDetail` | `k.product.verify_product_detail(name, price)` | `name, price` | Kiểm tra tên và giá trên trang chi tiết. |
| `product.addToCartFromDetail` | `k.product.add_to_cart_from_detail()` | — | Bấm "Add to cart" trên trang chi tiết. |
| `product.removeFromDetail` | `k.product.remove_from_detail()` | — | Bấm "Remove" trên trang chi tiết. |
| `product.backToProducts` | `k.product.back_to_products()` | — | Bấm "Back to products" và chờ danh sách sản phẩm. |

## cart

| Keyword | Python | Tham số | Mô tả |
|---|---|---|---|
| `cart.openCart` | `k.cart.open_cart()` | — | Bấm icon giỏ trên header và chờ trang giỏ hàng. |
| `cart.verifyCartItems` | `k.cart.verify_cart_items(names)` | `names` | Kiểm tra tên sản phẩm trong giỏ theo thứ tự; [] = giỏ trống. |
| `cart.removeFromCart` | `k.cart.remove_from_cart(name)` | `name` | Bấm "Remove" của 1 sản phẩm trong giỏ. |
| `cart.continueShopping` | `k.cart.continue_shopping()` | — | Bấm "Continue Shopping" và chờ danh sách sản phẩm. |
| `cart.proceedToCheckout` | `k.cart.proceed_to_checkout()` | — | Bấm "Checkout" và chờ form thông tin người nhận. |

## checkout

| Keyword | Python | Tham số | Mô tả |
|---|---|---|---|
| `checkout.fillCheckoutInfo` | `k.checkout.fill_checkout_info(first_name, last_name, postal_code)` | `first_name, last_name, postal_code` | Nhập First Name, Last Name, Zip/Postal Code. |
| `checkout.continueCheckout` | `k.checkout.continue_checkout()` | — | Bấm "Continue" ở bước thông tin người nhận. |
| `checkout.continueCheckoutExpectingError` | `k.checkout.continue_checkout_expecting_error(first_name, last_name, postal_code, message)` | `first_name, last_name, postal_code, message` | Nhập thông tin, bấm Continue và chờ lỗi đúng nguyên văn, vẫn ở bước 1. |
| `checkout.verifyOverviewItems` | `k.checkout.verify_overview_items(names)` | `names` | Kiểm tra tên sản phẩm ở trang xem lại đơn theo thứ tự. |
| `checkout.verifyItemTotal` | `k.checkout.verify_item_total(amount)` | `amount` | Kiểm tra dòng "Item total" bằng số tiền cho trước, vd "$39.98". |
| `checkout.verifyItemTotalEqualsSum` | `k.checkout.verify_item_total_equals_sum()` | — | Kiểm tra Item total = tổng giá các sản phẩm trong đơn. |
| `checkout.verifyTotalEqualsItemTotalPlusTax` | `k.checkout.verify_total_equals_item_total_plus_tax()` | — | Kiểm tra Total = Item total + Tax. |
| `checkout.finishCheckout` | `k.checkout.finish_checkout()` | — | Bấm "Finish" ở trang xem lại đơn. |
| `checkout.verifyOrderComplete` | `k.checkout.verify_order_complete(header, text)` | `header, text` | Kiểm tra trang hoàn tất hiện đúng tiêu đề và nội dung cảm ơn. |
| `checkout.cancelCheckout` | `k.checkout.cancel_checkout()` | — | Bấm "Cancel" ở bước checkout hiện tại (bước 1 hoặc 2). |
| `checkout.backHome` | `k.checkout.back_home()` | — | Bấm "Back Home" ở trang hoàn tất và chờ danh sách sản phẩm. |

## menu

| Keyword | Python | Tham số | Mô tả |
|---|---|---|---|
| `menu.openMenu` | `k.menu.open_menu()` | — | Mở menu burger. |
| `menu.closeMenu` | `k.menu.close_menu()` | — | Đóng menu burger. |
| `menu.verifyMenuItems` | `k.menu.verify_menu_items(names)` | `names` | Kiểm tra các mục menu đang hiển thị với đúng nhãn. |
| `menu.verifyAboutLink` | `k.menu.verify_about_link(href)` | `href` | Kiểm tra link About trỏ đúng địa chỉ (không mở trang ngoài). |
| `menu.gotoAllItems` | `k.menu.goto_all_items()` | — | Chọn "All Items" và chờ danh sách sản phẩm. |
| `menu.logout` | `k.menu.logout()` | — | Chọn "Logout" và chờ form đăng nhập. |
| `menu.resetAppState` | `k.menu.reset_app_state()` | — | Chọn "Reset App State" (xoá giỏ trong localStorage; nút trên trang chỉ đổi sau reload). |

