# Danh mục Test Case

> Tự sinh bởi `.venv/bin/python scripts/gen_test_cases.py` từ lần chạy **prod** lúc 10:04:43 27/10/2026. Đừng sửa tay.

## Tổng quan

| Module | Tổng | ✅ Đạt | 🐞 Bug đã biết | ❌ Lỗi | ⏭️ Bỏ qua | ⚠️ Bug đã sửa? |
|---|---|---|---|---|---|---|
| UI - Smoke | 1 | 1 |  |  |  |  |
| UI - Đăng nhập / Đăng xuất | 16 | 16 |  |  |  |  |
| UI - Danh sách & chi tiết sản phẩm | 15 | 9 | 6 |  |  |  |
| UI - Giỏ hàng | 5 | 5 |  |  |  |  |
| UI - Thanh toán | 11 | 9 | 2 |  |  |  |
| UI - Menu | 3 | 3 |  |  |  |  |
| Framework - unit test | 40 | 40 |  |  |  |  |
| **Tổng** | **91** | **83** | **8** | **0** | **0** | **0** |

Chú thích: 🐞 test đúng nhưng app còn bug (đánh dấu `xfail(strict=True)` / `knownBug`) · ❌ test fail · ⏭️ thiếu điều kiện (SAUCE_PASSWORD) · ⚠️ test PASS dù đánh dấu bug (bug có thể đã được sửa).

## Bug phát hiện

**8** test đang ghi nhận bug của app (`xfail`).

### Bug chức năng / giao diện (8 bug, gom theo mô tả)

| # | Module | Bug | Test |
|---|---|---|---|
| 1 | UI - Danh sách & chi tiết sản phẩm | problem_user không thêm được Bolt T-Shirt / Fleece Jacket / Red T-Shirt | UI-DSCT-07 |
| 2 | UI - Danh sách & chi tiết sản phẩm | problem_user chọn kiểu sắp xếp nhưng thứ tự sản phẩm không đổi | UI-DSCT-08 |
| 3 | UI - Danh sách & chi tiết sản phẩm | error_user bấm Remove trên danh sách không bỏ được sản phẩm | UI-DSCT-09 |
| 4 | UI - Danh sách & chi tiết sản phẩm | error_user sắp xếp hiện alert 'Sorting is broken!' và thứ tự không đổi | UI-DSCT-12 |
| 5 | UI - Danh sách & chi tiết sản phẩm | visual_user hiển thị giá ngẫu nhiên mỗi lần tải trang | UI-DSCT-13 |
| 6 | UI - Danh sách & chi tiết sản phẩm | problem_user bấm Backpack lại mở chi tiết sản phẩm id=5 (Fleece Jacket) | UI-DSCT-15 |
| 7 | UI - Thanh toán | problem_user gõ Last Name lại ghi đè vào First Name -> báo 'Last Name is required' | UI-TT-09 |
| 8 | UI - Thanh toán | error_user bấm Finish không có tác dụng, đứng ở checkout-step-two | UI-TT-10 |

## UI - Smoke

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-S-01 | test_smoke_purchase[SMOKE-01] | chromium | ✅ Đạt |  |

## UI - Đăng nhập / Đăng xuất

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-DNDX-01 | test_login_invalid[AUTH-E01] | chromium | ✅ Đạt |  |
| UI-DNDX-02 | test_login_valid[AUTH-01] | chromium | ✅ Đạt |  |
| UI-DNDX-03 | test_login_invalid[AUTH-E06] | chromium | ✅ Đạt |  |
| UI-DNDX-04 | test_login_valid[AUTH-02] | chromium | ✅ Đạt |  |
| UI-DNDX-05 | test_login_invalid[AUTH-E02] | chromium | ✅ Đạt |  |
| UI-DNDX-06 | test_protected_page[AUTH-P01] | chromium | ✅ Đạt |  |
| UI-DNDX-07 | test_logout[AUTH-L01] | chromium | ✅ Đạt |  |
| UI-DNDX-08 | test_protected_page[AUTH-P02] | chromium | ✅ Đạt |  |
| UI-DNDX-09 | test_login_invalid[AUTH-E03] | chromium | ✅ Đạt |  |
| UI-DNDX-10 | test_login_valid[AUTH-03] | chromium | ✅ Đạt |  |
| UI-DNDX-11 | test_protected_page[AUTH-P03] | chromium | ✅ Đạt |  |
| UI-DNDX-12 | test_login_invalid[AUTH-E04] | chromium | ✅ Đạt |  |
| UI-DNDX-13 | test_login_valid[AUTH-04] | chromium | ✅ Đạt |  |
| UI-DNDX-14 | test_protected_page[AUTH-P04] | chromium | ✅ Đạt |  |
| UI-DNDX-15 | test_login_invalid[AUTH-E05] | chromium | ✅ Đạt |  |
| UI-DNDX-16 | test_login_valid[AUTH-05] | chromium | ✅ Đạt |  |

## UI - Danh sách & chi tiết sản phẩm

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-DSCT-01 | test_add_remove_updates_badge[INV-C01] | chromium | ✅ Đạt |  |
| UI-DSCT-02 | test_sort[INV-S01] | chromium | ✅ Đạt |  |
| UI-DSCT-03 | test_add_remove_updates_badge[INV-C02] | chromium | ✅ Đạt |  |
| UI-DSCT-04 | test_sort[INV-S02] | chromium | ✅ Đạt |  |
| UI-DSCT-05 | test_sort[INV-S03] | chromium | ✅ Đạt |  |
| UI-DSCT-06 | test_sort[INV-S04] | chromium | ✅ Đạt |  |
| UI-DSCT-07 | test_add_remove_updates_badge[INV-C03] | chromium | 🐞 Bug đã biết | BUG: problem_user không thêm được Bolt T-Shirt / Fleece Jacket / Red T-Shirt |
| UI-DSCT-08 | test_sort[INV-S05] | chromium | 🐞 Bug đã biết | BUG: problem_user chọn kiểu sắp xếp nhưng thứ tự sản phẩm không đổi |
| UI-DSCT-09 | test_add_remove_updates_badge[INV-C04] | chromium | 🐞 Bug đã biết | BUG: error_user bấm Remove trên danh sách không bỏ được sản phẩm |
| UI-DSCT-10 | test_product_listing[INV-L01] | chromium | ✅ Đạt |  |
| UI-DSCT-11 | test_open_product_detail[INV-D01] | chromium | ✅ Đạt |  |
| UI-DSCT-12 | test_sort[INV-S06] | chromium | 🐞 Bug đã biết | BUG: error_user sắp xếp hiện alert 'Sorting is broken!' và thứ tự không đổi |
| UI-DSCT-13 | test_product_listing[INV-L02] | chromium | 🐞 Bug đã biết | BUG: visual_user hiển thị giá ngẫu nhiên mỗi lần tải trang |
| UI-DSCT-14 | test_open_product_detail[INV-D02] | chromium | ✅ Đạt |  |
| UI-DSCT-15 | test_open_product_detail[INV-D03] | chromium | 🐞 Bug đã biết | BUG: problem_user bấm Backpack lại mở chi tiết sản phẩm id=5 (Fleece Jacket) |

## UI - Giỏ hàng

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-GH-01 | test_cart_persists_after_reload[CART-01] | chromium | ✅ Đạt |  |
| UI-GH-02 | test_remove_from_cart[CART-02] | chromium | ✅ Đạt |  |
| UI-GH-03 | test_remove_from_cart[CART-03] | chromium | ✅ Đạt |  |
| UI-GH-04 | test_continue_shopping[CART-04] | chromium | ✅ Đạt |  |
| UI-GH-05 | test_reset_app_state[CART-05] | chromium | ✅ Đạt |  |

## UI - Thanh toán

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-TT-01 | test_required_fields[CHK-V02] | chromium | ✅ Đạt |  |
| UI-TT-02 | test_purchase[CHK-01] | chromium | ✅ Đạt |  |
| UI-TT-03 | test_required_fields[CHK-V03] | chromium | ✅ Đạt |  |
| UI-TT-04 | test_purchase[CHK-02] | chromium | ✅ Đạt |  |
| UI-TT-05 | test_required_fields[CHK-V04] | chromium | ✅ Đạt |  |
| UI-TT-06 | test_cancel[CHK-C01] | chromium | ✅ Đạt |  |
| UI-TT-07 | test_cancel[CHK-C02] | chromium | ✅ Đạt |  |
| UI-TT-08 | test_purchase[CHK-03] | chromium | ✅ Đạt |  |
| UI-TT-09 | test_purchase[CHK-04] | chromium | 🐞 Bug đã biết | BUG: problem_user gõ Last Name lại ghi đè vào First Name -> báo 'Last Name is required' |
| UI-TT-10 | test_purchase[CHK-05] | chromium | 🐞 Bug đã biết | BUG: error_user bấm Finish không có tác dụng, đứng ở checkout-step-two |
| UI-TT-11 | test_required_fields[CHK-V01] | chromium | ✅ Đạt |  |

## UI - Menu

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-M-01 | test_all_items[MENU-03] | chromium | ✅ Đạt |  |
| UI-M-02 | test_menu_items[MENU-01] | chromium | ✅ Đạt |  |
| UI-M-03 | test_all_items[MENU-02] | chromium | ✅ Đạt |  |

## Framework - unit test

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| FW-UT-01 | test_resolve_data[${flag}/${items.1}-true/b] | core | ✅ Đạt |  |
| FW-UT-02 | test_resolve_data[value3-expected3] | core | ✅ Đạt |  |
| FW-UT-03 | test_resolve_data[kh\xf4ng c\xf3 bi\u1ebfn-kh\xf4ng c\xf3 bi\u1ebfn] | core | ✅ Đạt |  |
| FW-UT-04 | test_resolve_unknown_variable | core | ✅ Đạt |  |
| FW-UT-05 | test_resolve_uid_is_unique | core | ✅ Đạt |  |
| FW-UT-06 | test_resolve_messages_from_base_context | core | ✅ Đạt |  |
| FW-UT-07 | test_load_data_pointer_and_copy | core | ✅ Đạt |  |
| FW-UT-08 | test_load_data_via_reference | core | ✅ Đạt |  |
| FW-UT-09 | test_load_data_errors[missing.json] | core | ✅ Đạt |  |
| FW-UT-10 | test_load_data_errors[x.json#a.z] | core | ✅ Đạt |  |
| FW-UT-11 | test_mask_secrets | core | ✅ Đạt |  |
| FW-UT-12 | test_case_params_marks | core | ✅ Đạt |  |
| FW-UT-13 | test_case_params_rejects[cases0-tr\xf9ng] | core | ✅ Đạt |  |
| FW-UT-14 | test_case_params_rejects[cases1-thi\u1ebfu id] | core | ✅ Đạt |  |
| FW-UT-15 | test_case_params_rejects[cases2-tag ch\u01b0a khai b\xe1o] | core | ✅ Đạt |  |
| FW-UT-16 | test_case_params_rejects[cases3-requires kh\xf4ng h\u1ee3p l\u1ec7] | core | ✅ Đạt |  |
| FW-UT-17 | test_session_seconds_left | core | ✅ Đạt |  |
| FW-UT-18 | test_money[$29.99-expected0] | core | ✅ Đạt |  |
| FW-UT-19 | test_money[Total: $32.39-expected1] | core | ✅ Đạt |  |
| FW-UT-20 | test_money[$11.7-expected2] | core | ✅ Đạt |  |
| FW-UT-21 | test_money_rejects | core | ✅ Đạt |  |
| FW-UT-22 | test_classify_exception[error0-ASSERTION_FAILED] | core | ✅ Đạt |  |
| FW-UT-23 | test_classify_exception[error1-TIMEOUT] | core | ✅ Đạt |  |
| FW-UT-24 | test_classify_exception[error2-ELEMENT_NOT_FOUND] | core | ✅ Đạt |  |
| FW-UT-25 | test_classify_exception[error3-STALE_ELEMENT] | core | ✅ Đạt |  |
| FW-UT-26 | test_classify_exception[error4-ELEMENT_NOT_INTERACTABLE] | core | ✅ Đạt |  |
| FW-UT-27 | test_classify_exception[error5-UNEXPECTED_ALERT] | core | ✅ Đạt |  |
| FW-UT-28 | test_classify_exception[error6-BROWSER_CLOSED] | core | ✅ Đạt |  |
| FW-UT-29 | test_classify_exception[error7-NETWORK_ERROR] | core | ✅ Đạt |  |
| FW-UT-30 | test_classify_exception[error8-WEBDRIVER_ERROR] | core | ✅ Đạt |  |
| FW-UT-31 | test_classify_exception[error9-DATA_OR_CONTRACT_ERROR] | core | ✅ Đạt |  |
| FW-UT-32 | test_classify_exception[error10-DATA_OR_CONTRACT_ERROR] | core | ✅ Đạt |  |
| FW-UT-33 | test_classify_exception[error11-UNEXPECTED_ERROR] | core | ✅ Đạt |  |
| FW-UT-34 | test_classify_report_text[selenium.common.exceptions.TimeoutException: Message:-TIMEOUT] | core | ✅ Đạt |  |
| FW-UT-35 | test_classify_report_text[E   AssertionError: assert 'Products' == 'Your Cart'-ASSERTION_FAILED] | core | ✅ Đạt |  |
| FW-UT-36 | test_classify_report_text[selenium.common.exceptions.UnexpectedAlertPresentException: Alert Text: Sorting is broken!-UNEXPECTED_ALERT] | core | ✅ Đạt |  |
| FW-UT-37 | test_classify_report_text[ValueError: Kh\xf4ng c\xf3 s\u1ea3n ph\u1ea9m-DATA_OR_CONTRACT_ERROR] | core | ✅ Đạt |  |
| FW-UT-38 | test_classify_report_text[-UNEXPECTED_ERROR] | core | ✅ Đạt |  |
| FW-UT-39 | test_resolve_data[${user.count}-2] | core | ✅ Đạt |  |
| FW-UT-40 | test_resolve_data[Xin ch\xe0o ${user.name}-Xin ch\xe0o standard_user] | core | ✅ Đạt |  |

