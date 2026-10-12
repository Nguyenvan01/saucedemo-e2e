# Khảo sát saucedemo.com (Swag Labs)

Khảo sát ngày 2026-10-12 bằng Playwright Chromium (headless, viewport 1280×720) trên https://www.saucedemo.com.
Mọi chuỗi trong tài liệu là **nguyên văn** từ trang thật. Mật khẩu chung hiển thị trong `data-test="login-password"`
trên trang login — **không** ghi vào repo, chỉ đặt trong `.env`.

## 1. Kết luận nhanh — khác gì so với phần "Bối cảnh"

| # | Bối cảnh giả định | Thực tế | Ảnh hưởng thiết kế |
|---|---|---|---|
| 1 | Menu: All Items, About, Logout, Reset App State | Có thêm **Dynamic Catalog** (`dynamic-catalog-sidebar-link`) | Ghi nhận; ngoài phạm vi test tối thiểu |
| 2 | Truy cập `/inventory.html` khi chưa đăng nhập → về login | **URL giữ nguyên** `/inventory.html`, trang hiển thị form login + lỗi riêng cho từng path | `verifyUrl` không dùng được; kiểm tra form login + thông báo lỗi |
| 3 | Phiên ở cookie | Cookie `session-username` = **tên user** (không phải token), **hết hạn sau 600 giây** | storageState trong `.auth/` chỉ sống 10 phút → `auth_states` phải tạo lại khi hết hạn |
| 4 | Giỏ ở localStorage | Khoá `cart-contents` = mảng JSON **id sản phẩm**, ví dụ `"[4,0]"`; ngoài ra có `backtrace-guid`, `backtrace-last-active` (SDK báo lỗi) | Chỉ quan tâm `cart-contents` |
| 5 | Mọi phần tử có `data-test` | Nút mở/đóng menu **không** có `data-test` trên `<button>` (chỉ có trên `<img>` `open-menu`/`close-menu`) | Dùng `get_by_role("button", name="Open Menu"/"Close Menu")` |
| 6 | — | Trang chi tiết dùng `add-to-cart` / `remove` (không kèm slug), không có `data-test="title"` | Page Object riêng cho chi tiết |
| 7 | — | Reset App State xoá badge + `cart-contents` nhưng **nút "Remove" trên trang hiện tại vẫn còn** tới khi reload; menu vẫn mở | Hành vi gốc của site (cả standard_user) — kiểm tra badge + localStorage, xem mục 7 |
| 8 | — | performance_glitch_user: URL đổi sang `/inventory.html` ngay nhưng danh sách sản phẩm **~5,5 s** mới hiện | Chờ theo phần tử (`inventory-list`), timeout ≥ 10 s; không chờ theo URL |

## 2. Trang và URL

| Trang | URL | `title` (data-test) | Phần tử chờ sẵn sàng |
|---|---|---|---|
| Login | `/` | — (tiêu đề tab: `Swag Labs`) | `login-button` |
| Danh sách | `/inventory.html` | `Products` | `inventory-list` |
| Chi tiết | `/inventory-item.html?id=N` | — | `back-to-products` |
| Giỏ | `/cart.html` | `Your Cart` | `cart-list` |
| Checkout 1 | `/checkout-step-one.html` | `Checkout: Your Information` | `firstName` |
| Checkout 2 | `/checkout-step-two.html` | `Checkout: Overview` | `finish` |
| Hoàn tất | `/checkout-complete.html` | `Checkout: Complete!` | `complete-header` |
| About (ngoài site) | `https://saucelabs.com/` | — | chỉ kiểm tra `href` |

`/inventory-item.html?id=999` → `inventory-item-name` = `ITEM NOT FOUND`.

## 3. `data-test` theo trang

Header (mọi trang sau đăng nhập): `header-container`, `primary-header`, `open-menu` (img), `shopping-cart-link`,
`shopping-cart-badge` (chỉ có khi giỏ ≥ 1), `secondary-header`, `title`. Footer: `footer`, `footer-copy`,
`social-x`, `social-facebook`, `social-linkedin`.

**Burger menu**: nút `button` "Open Menu" (`#react-burger-menu-btn`), "Close Menu" (`#react-burger-cross-btn`);
link `inventory-sidebar-link` (All Items), `dynamic-catalog-sidebar-link` (Dynamic Catalog),
`about-sidebar-link` (About, `href=https://saucelabs.com/`), `logout-sidebar-link` (Logout),
`reset-sidebar-link` (Reset App State).

**Login**: `username` (placeholder `Username`), `password` (placeholder `Password`), `login-button`,
`error` (khung lỗi), `error-button` (nút X đóng lỗi), `login-credentials`, `login-password`.
Khi lỗi: cả hai input có class `error` và hiện 2 icon lỗi.

**Inventory**: `product-sort-container` (select), `active-option` (nhãn đang chọn), `inventory-list`,
`inventory-item` (×6), trong mỗi item: `inventory-item-name`, `inventory-item-desc`, `inventory-item-price`,
`item-<id>-title-link`, `item-<id>-img-link`, `inventory-item-<slug>-img`,
`add-to-cart-<slug>` ↔ `remove-<slug>` (chữ `Add to cart` ↔ `Remove`).

**Chi tiết**: `back-to-products` (`Back to products`), `inventory-item-name`, `inventory-item-desc`,
`inventory-item-price`, `item-<slug>-img`, `add-to-cart` ↔ `remove`.

**Giỏ**: `cart-list`, `cart-quantity-label` (QTY), `cart-desc-label` (Description), `inventory-item`,
`item-quantity`, `item-<id>-title-link`, `inventory-item-name/desc/price`, `remove-<slug>`,
`continue-shopping`, `checkout`.

**Checkout 1**: `firstName` (placeholder `First Name`), `lastName` (`Last Name`), `postalCode` (`Zip/Postal Code`),
`cancel`, `continue`, `error`.

**Checkout 2**: `cart-list`, `inventory-item`, `item-quantity`, `inventory-item-name/desc/price`,
`payment-info-label`/`payment-info-value` (`SauceCard #31337`), `shipping-info-label`/`shipping-info-value`
(`Free Pony Express Delivery!`), `total-info-label` (`Price Total`), `subtotal-label` (`Item total: $9.99`),
`tax-label` (`Tax: $0.80`), `total-label` (`Total: $10.79`), `cancel`, `finish`.

**Hoàn tất**: `pony-express` (ảnh), `complete-header`, `complete-text`, `back-to-products` (`Back Home`),
`generate-pdf-order`.

## 4. Sản phẩm (standard_user)

`<slug>` = tên viết thường, khoảng trắng → `-`.

| id | Tên | Giá | slug |
|---|---|---|---|
| 4 | Sauce Labs Backpack | $29.99 | `sauce-labs-backpack` |
| 0 | Sauce Labs Bike Light | $9.99 | `sauce-labs-bike-light` |
| 1 | Sauce Labs Bolt T-Shirt | $15.99 | `sauce-labs-bolt-t-shirt` |
| 5 | Sauce Labs Fleece Jacket | $49.99 | `sauce-labs-fleece-jacket` |
| 2 | Sauce Labs Onesie | $7.99 | `sauce-labs-onesie` |
| 3 | Test.allTheThings() T-Shirt (Red) | $15.99 | `test.allthethings()-t-shirt-(red)` |

Sắp xếp — `value` → nhãn → thứ tự thực tế:

| value | Nhãn | Thứ tự |
|---|---|---|
| `az` (mặc định) | Name (A to Z) | Backpack, Bike Light, Bolt T-Shirt, Fleece Jacket, Onesie, Test.allTheThings() |
| `za` | Name (Z to A) | ngược lại của `az` |
| `lohi` | Price (low to high) | Onesie, Bike Light, Bolt T-Shirt, Test.allTheThings(), Backpack, Fleece Jacket |
| `hilo` | Price (high to low) | Fleece Jacket, Backpack, Bolt T-Shirt, Test.allTheThings(), Bike Light, Onesie |

Hai sản phẩm cùng giá $15.99 giữ thứ tự theo tên (ổn định) ở cả `lohi` và `hilo`.

## 5. Thông báo (nguyên văn)

| Tình huống | Thông báo |
|---|---|
| Bỏ trống username (dù có/không password) | `Epic sadface: Username is required` |
| Có username, bỏ trống password | `Epic sadface: Password is required` |
| Sai mật khẩu / user không tồn tại | `Epic sadface: Username and password do not match any user in this service` |
| locked_out_user | `Epic sadface: Sorry, this user has been locked out.` |
| Mở trang cần đăng nhập khi chưa đăng nhập | `Epic sadface: You can only access '<path>' when you are logged in.` — `<path>` là pathname, không kèm query (vd `'/inventory-item.html'`) |
| Checkout 1 thiếu First Name (kiểm tra theo thứ tự First → Last → Zip) | `Error: First Name is required` |
| Thiếu Last Name | `Error: Last Name is required` |
| Thiếu Postal Code | `Error: Postal Code is required` |
| Hoàn tất đơn | `Thank you for your order!` / `Your order has been dispatched, and will arrive just as fast as the pony can get there!` |
| error_user sắp xếp (hộp thoại `alert`) | `Sorting is broken! This error has been reported to Backtrace.` |

Nhấn `error-button` → khung lỗi biến mất.

## 6. Phiên và lưu trữ

| Thời điểm | Cookie | localStorage |
|---|---|---|
| Trước đăng nhập | — | `backtrace-guid`, `backtrace-last-active` |
| Sau đăng nhập | `session-username=<user>` (domain `www.saucedemo.com`, path `/`, hết hạn +600 s) | như trên |
| Thêm Backpack + Bike Light | như trên | `cart-contents = "[4,0]"` |
| Hoàn tất đơn / Reset App State | như trên | `cart-contents` bị xoá |
| Logout | cookie bị xoá | `backtrace-*` giữ lại |

- Giỏ còn nguyên sau `reload` (đã xác minh).
- `context.storage_state()` trả về `cookies` + `origins` (localStorage) → dùng trực tiếp cho `.auth/<user>.json`.
- Thuế = 8 % item total, làm tròn 2 số lẻ: $9.99 → $0.80; $29.99 → $2.40; $47.97 → $3.84.
- Cancel ở Checkout 1 → `/cart.html`; Cancel ở Checkout 2 → `/inventory.html`; Back Home → `/inventory.html`.

## 7. Hành vi theo tài khoản (lỗi cố ý → `knownBug`)

| User | Hành vi quan sát | Đề xuất khai báo |
|---|---|---|
| standard_user | Mọi luồng đúng như mục 2–6 | Chuẩn so sánh |
| locked_out_user | Không đăng nhập được, thông báo bị khoá | Case auth âm |
| problem_user | Mọi ảnh = `/assets/sl-404-*.jpg`; sắp xếp **không đổi** thứ tự; thêm giỏ chỉ được Backpack/Bike Light/Onesie (3 cái còn lại bấm không ăn); nút Remove trên inventory không bỏ được; click `item-4-title-link` (Backpack) mở `?id=5` (Fleece Jacket); nút `add-to-cart` ở chi tiết không ăn; Checkout 1: gõ Last Name lại ghi đè vào First Name → `Error: Last Name is required` | `knownBug` cho sort, add/remove, mở chi tiết, checkout |
| performance_glitch_user | Đăng nhập ~5,5 s rồi mới hiện danh sách; còn lại bình thường | Case dương, timeout rộng (không phải bug) |
| error_user | Sắp xếp hiện `alert` lỗi, thứ tự không đổi; thêm giỏ chỉ được Backpack/Bike Light/Onesie; Remove trên inventory không ăn (Remove trong giỏ vẫn được); Last Name không gõ được nhưng Continue vẫn qua bước 2; **Finish không làm gì** (đứng ở step-two) | `knownBug` cho sort, add/remove, finish |
| visual_user | Giá trên inventory **ngẫu nhiên mỗi lần tải** (vd `$11.7`, `$88.31`); ảnh Backpack = sl-404; icon giỏ lệch vị trí (x≈1034, y≈39 so với 1220, 10); giá ở chi tiết + checkout vẫn đúng | `knownBug` cho kiểm tra giá trên inventory |

## 8. Ghi chú cho thiết kế framework

- `test_id_attribute="data-test"` phủ gần hết; ngoại lệ duy nhất cần `get_by_role` là 2 nút burger.
- `data-test` trùng lặp (`inventory-item-name`, `inventory-item-price`, `error`…) → luôn lọc theo item cha
  (`get_by_test_id("inventory-item").filter(has_text=...)`), không dùng `nth` theo cấu trúc DOM.
- Không có API → không có `api_client`; mọi điều kiện đầu (giỏ có sẵn hàng) dựng bằng UI hoặc `localStorage`
  (`cart-contents`) trong `utils/storage.py`.
