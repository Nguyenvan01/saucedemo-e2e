# Danh mục Test Case

> Tự sinh bởi `.venv/bin/python scripts/gen_test_cases.py` từ lần chạy **prod** lúc 8:34:32 12/10/2026. Đừng sửa tay.

## Tổng quan

| Module | Tổng | ✅ Đạt | 🐞 Bug đã biết | ❌ Lỗi | ⏭️ Bỏ qua | ⚠️ Bug đã sửa? |
|---|---|---|---|---|---|---|
| UI - Smoke | 1 | 1 |  |  |  |  |
| UI - Đăng nhập / Đăng xuất | 16 | 16 |  |  |  |  |
| UI - Danh sách & chi tiết sản phẩm | 15 | 9 | 6 |  |  |  |
| UI - Giỏ hàng | 5 | 5 |  |  |  |  |
| UI - Thanh toán | 11 | 9 | 2 |  |  |  |
| UI - Menu | 3 | 3 |  |  |  |  |
| Kịch bản Keyword-driven (Excel) | 10 | 8 | 2 |  |  |  |
| Framework - unit test | 79 | 79 |  |  |  |  |
| **Tổng** | **140** | **130** | **10** | **0** | **0** | **0** |

Chú thích: 🐞 test đúng nhưng app còn bug (đánh dấu `xfail(strict=True)` / `knownBug`) · ❌ test fail · ⏭️ thiếu điều kiện (SAUCE_PASSWORD) · ⚠️ test PASS dù đánh dấu bug (bug có thể đã được sửa).

## Bug phát hiện

**10** test đang ghi nhận bug của app (`xfail`).

### Bug chức năng / giao diện (8 bug, gom theo mô tả)

| # | Module | Bug | Test |
|---|---|---|---|
| 1 | UI - Danh sách & chi tiết sản phẩm | visual_user hiển thị giá ngẫu nhiên mỗi lần tải trang | UI-DSCT-01 |
| 2 | UI - Danh sách & chi tiết sản phẩm | error_user sắp xếp hiện alert 'Sorting is broken!' và thứ tự không đổi | UI-DSCT-08 |
| 3 | UI - Danh sách & chi tiết sản phẩm | error_user bấm Remove trên danh sách không bỏ được sản phẩm | UI-DSCT-11 |
| 4 | UI - Danh sách & chi tiết sản phẩm | problem_user không thêm được Bolt T-Shirt / Fleece Jacket / Red T-Shirt | UI-DSCT-13 |
| 5 | UI - Danh sách & chi tiết sản phẩm | problem_user bấm Backpack lại mở chi tiết sản phẩm id=5 (Fleece Jacket) | UI-DSCT-14 |
| 6 | UI - Danh sách & chi tiết sản phẩm | problem_user chọn kiểu sắp xếp nhưng thứ tự sản phẩm không đổi | UI-DSCT-15, UI-KBKD-06 |
| 7 | UI - Thanh toán | problem_user gõ Last Name lại ghi đè vào First Name -> báo 'Last Name is required' | UI-TT-06 |
| 8 | UI - Thanh toán | error_user bấm Finish không có tác dụng, đứng ở checkout-step-two | UI-TT-11, UI-KBKD-03 |

## UI - Smoke

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-S-01 | test_smoke_purchase[chromium-SMOKE-01] | chromium | ✅ Đạt |  |

## UI - Đăng nhập / Đăng xuất

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-DNDX-01 | test_login_valid[chromium-AUTH-01] | chromium | ✅ Đạt |  |
| UI-DNDX-02 | test_login_invalid[chromium-AUTH-E01] | chromium | ✅ Đạt |  |
| UI-DNDX-03 | test_protected_page[chromium-AUTH-P01] | chromium | ✅ Đạt |  |
| UI-DNDX-04 | test_logout[chromium-AUTH-L01] | chromium | ✅ Đạt |  |
| UI-DNDX-05 | test_login_valid[chromium-AUTH-02] | chromium | ✅ Đạt |  |
| UI-DNDX-06 | test_login_invalid[chromium-AUTH-E02] | chromium | ✅ Đạt |  |
| UI-DNDX-07 | test_login_valid[chromium-AUTH-03] | chromium | ✅ Đạt |  |
| UI-DNDX-08 | test_protected_page[chromium-AUTH-P02] | chromium | ✅ Đạt |  |
| UI-DNDX-09 | test_login_invalid[chromium-AUTH-E03] | chromium | ✅ Đạt |  |
| UI-DNDX-10 | test_protected_page[chromium-AUTH-P03] | chromium | ✅ Đạt |  |
| UI-DNDX-11 | test_login_valid[chromium-AUTH-05] | chromium | ✅ Đạt |  |
| UI-DNDX-12 | test_login_invalid[chromium-AUTH-E05] | chromium | ✅ Đạt |  |
| UI-DNDX-13 | test_login_valid[chromium-AUTH-04] | chromium | ✅ Đạt |  |
| UI-DNDX-14 | test_login_invalid[chromium-AUTH-E04] | chromium | ✅ Đạt |  |
| UI-DNDX-15 | test_protected_page[chromium-AUTH-P04] | chromium | ✅ Đạt |  |
| UI-DNDX-16 | test_login_invalid[chromium-AUTH-E06] | chromium | ✅ Đạt |  |

## UI - Danh sách & chi tiết sản phẩm

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-DSCT-01 | test_product_listing[chromium-INV-L02] | chromium | 🐞 Bug đã biết | BUG: visual_user hiển thị giá ngẫu nhiên mỗi lần tải trang |
| UI-DSCT-02 | test_product_listing[chromium-INV-L01] | chromium | ✅ Đạt |  |
| UI-DSCT-03 | test_sort[chromium-INV-S01] | chromium | ✅ Đạt |  |
| UI-DSCT-04 | test_add_remove_updates_badge[chromium-INV-C01] | chromium | ✅ Đạt |  |
| UI-DSCT-05 | test_open_product_detail[chromium-INV-D01] | chromium | ✅ Đạt |  |
| UI-DSCT-06 | test_sort[chromium-INV-S02] | chromium | ✅ Đạt |  |
| UI-DSCT-07 | test_add_remove_updates_badge[chromium-INV-C02] | chromium | ✅ Đạt |  |
| UI-DSCT-08 | test_sort[chromium-INV-S06] | chromium | 🐞 Bug đã biết | BUG: error_user sắp xếp hiện alert 'Sorting is broken!' và thứ tự không đổi |
| UI-DSCT-09 | test_open_product_detail[chromium-INV-D02] | chromium | ✅ Đạt |  |
| UI-DSCT-10 | test_sort[chromium-INV-S04] | chromium | ✅ Đạt |  |
| UI-DSCT-11 | test_add_remove_updates_badge[chromium-INV-C04] | chromium | 🐞 Bug đã biết | BUG: error_user bấm Remove trên danh sách không bỏ được sản phẩm |
| UI-DSCT-12 | test_sort[chromium-INV-S03] | chromium | ✅ Đạt |  |
| UI-DSCT-13 | test_add_remove_updates_badge[chromium-INV-C03] | chromium | 🐞 Bug đã biết | BUG: problem_user không thêm được Bolt T-Shirt / Fleece Jacket / Red T-Shirt |
| UI-DSCT-14 | test_open_product_detail[chromium-INV-D03] | chromium | 🐞 Bug đã biết | BUG: problem_user bấm Backpack lại mở chi tiết sản phẩm id=5 (Fleece Jacket) |
| UI-DSCT-15 | test_sort[chromium-INV-S05] | chromium | 🐞 Bug đã biết | BUG: problem_user chọn kiểu sắp xếp nhưng thứ tự sản phẩm không đổi |

## UI - Giỏ hàng

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-GH-01 | test_cart_persists_after_reload[chromium-CART-01] | chromium | ✅ Đạt |  |
| UI-GH-02 | test_remove_from_cart[chromium-CART-02] | chromium | ✅ Đạt |  |
| UI-GH-03 | test_continue_shopping[chromium-CART-04] | chromium | ✅ Đạt |  |
| UI-GH-04 | test_reset_app_state[chromium-CART-05] | chromium | ✅ Đạt |  |
| UI-GH-05 | test_remove_from_cart[chromium-CART-03] | chromium | ✅ Đạt |  |

## UI - Thanh toán

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-TT-01 | test_purchase[chromium-CHK-01] | chromium | ✅ Đạt |  |
| UI-TT-02 | test_required_fields[chromium-CHK-V02] | chromium | ✅ Đạt |  |
| UI-TT-03 | test_cancel[chromium-CHK-C02] | chromium | ✅ Đạt |  |
| UI-TT-04 | test_required_fields[chromium-CHK-V01] | chromium | ✅ Đạt |  |
| UI-TT-05 | test_cancel[chromium-CHK-C01] | chromium | ✅ Đạt |  |
| UI-TT-06 | test_purchase[chromium-CHK-04] | chromium | 🐞 Bug đã biết | BUG: problem_user gõ Last Name lại ghi đè vào First Name -> báo 'Last Name is required' |
| UI-TT-07 | test_purchase[chromium-CHK-02] | chromium | ✅ Đạt |  |
| UI-TT-08 | test_required_fields[chromium-CHK-V04] | chromium | ✅ Đạt |  |
| UI-TT-09 | test_purchase[chromium-CHK-03] | chromium | ✅ Đạt |  |
| UI-TT-10 | test_required_fields[chromium-CHK-V03] | chromium | ✅ Đạt |  |
| UI-TT-11 | test_purchase[chromium-CHK-05] | chromium | 🐞 Bug đã biết | BUG: error_user bấm Finish không có tác dụng, đứng ở checkout-step-two |

## UI - Menu

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-M-01 | test_menu_items[chromium-MENU-01] | chromium | ✅ Đạt |  |
| UI-M-02 | test_all_items[chromium-MENU-02] | chromium | ✅ Đạt |  |
| UI-M-03 | test_all_items[chromium-MENU-03] | chromium | ✅ Đạt |  |

## Kịch bản Keyword-driven (Excel)

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| UI-KBKD-01 | test_scenario[chromium-KW-AUTH-01] | chromium | ✅ Đạt |  |
| UI-KBKD-02 | test_scenario[chromium-KW-AUTH-02] | chromium | ✅ Đạt |  |
| UI-KBKD-03 | test_scenario[chromium-KW-BUY-03] | chromium | 🐞 Bug đã biết | BUG: error_user bấm Finish không có tác dụng, đứng ở checkout-step-two |
| UI-KBKD-04 | test_scenario[chromium-KW-BUY-01] | chromium | ✅ Đạt |  |
| UI-KBKD-05 | test_scenario[chromium-KW-SORT-01] | chromium | ✅ Đạt |  |
| UI-KBKD-06 | test_scenario[chromium-KW-SORT-02] | chromium | 🐞 Bug đã biết | BUG: problem_user chọn kiểu sắp xếp nhưng thứ tự sản phẩm không đổi |
| UI-KBKD-07 | test_scenario[chromium-KW-RESET-01] | chromium | ✅ Đạt |  |
| UI-KBKD-08 | test_scenario[chromium-KW-CHK-01] | chromium | ✅ Đạt |  |
| UI-KBKD-09 | test_scenario[chromium-KW-AUTH-03] | chromium | ✅ Đạt |  |
| UI-KBKD-10 | test_scenario[chromium-KW-BUY-02] | chromium | ✅ Đạt |  |

## Framework - unit test

| ID | Test case | Project | Kết quả | Ghi chú |
|---|---|---|---|---|
| FW-UT-01 | test_invalid_steps_rejected[<lambda>-th\u1ee9 t\u1ef1 step] | core | ✅ Đạt |  |
| FW-UT-02 | test_invalid_steps_rejected[<lambda>-case_id] | core | ✅ Đạt |  |
| FW-UT-03 | test_invalid_steps_rejected[<lambda>-keyword ch\u01b0a khai b\xe1o] | core | ✅ Đạt |  |
| FW-UT-04 | test_invalid_steps_rejected[<lambda>-args ph\u1ea3i l\xe0 m\u1ea3ng] | core | ✅ Đạt |  |
| FW-UT-05 | test_invalid_steps_rejected[<lambda>-note ph\u1ea3i l\xe0 chu\u1ed7i] | core | ✅ Đạt |  |
| FW-UT-06 | test_empty_scenario_rejected[steps0] | core | ✅ Đạt |  |
| FW-UT-07 | test_empty_scenario_rejected[None] | core | ✅ Đạt |  |
| FW-UT-08 | test_empty_scenario_rejected[abc] | core | ✅ Đạt |  |
| FW-UT-09 | test_scenario_needs_check_step | core | ✅ Đạt |  |
| FW-UT-10 | test_is_check_step[common.verifyUrl-True] | core | ✅ Đạt |  |
| FW-UT-11 | test_is_check_step[auth.loginExpectingError-True] | core | ✅ Đạt |  |
| FW-UT-12 | test_is_check_step[auth.login-False] | core | ✅ Đạt |  |
| FW-UT-13 | test_execute_resolves_runtime_variables | core | ✅ Đạt |  |
| FW-UT-14 | test_execute_reraises_with_context | core | ✅ Đạt |  |
| FW-UT-15 | test_bind_one_case | core | ✅ Đạt |  |
| FW-UT-16 | test_missing_placeholder | core | ✅ Đạt |  |
| FW-UT-17 | test_invalid_placeholder[{missing}] | core | ✅ Đạt |  |
| FW-UT-18 | test_invalid_placeholder[{product] | core | ✅ Đạt |  |
| FW-UT-19 | test_invalid_placeholder[name:{product}] | core | ✅ Đạt |  |
| FW-UT-20 | test_unknown_keyword_rejected | core | ✅ Đạt |  |
| FW-UT-21 | test_wrong_step_order_rejected | core | ✅ Đạt |  |
| FW-UT-22 | test_binding_is_independent | core | ✅ Đạt |  |
| FW-UT-23 | test_build_cases_meta_and_join | core | ✅ Đạt |  |
| FW-UT-24 | test_build_cases_rejects_bad_data[<lambda>-tr\xf9ng] | core | ✅ Đạt |  |
| FW-UT-25 | test_build_cases_rejects_bad_data[<lambda>-Template kh\xf4ng t\u1ed3n t\u1ea1i] | core | ✅ Đạt |  |
| FW-UT-26 | test_build_cases_rejects_bad_data[<lambda>-thi\u1ebfu title] | core | ✅ Đạt |  |
| FW-UT-27 | test_build_cases_rejects_bad_data[<lambda>-gi\xe1 tr\u1ecb chu\u1ed7i] | core | ✅ Đạt |  |
| FW-UT-28 | test_unused_template_rejected | core | ✅ Đạt |  |
| FW-UT-29 | test_parse_args[-expected0] | core | ✅ Đạt |  |
| FW-UT-30 | test_parse_args[["Sauce Labs Onesie", 2]-expected1] | core | ✅ Đạt |  |
| FW-UT-31 | test_parse_args[[[]]-expected2] | core | ✅ Đạt |  |
| FW-UT-32 | test_parse_args_rejects[{] | core | ✅ Đạt |  |
| FW-UT-33 | test_parse_args_rejects["chu\u1ed7i"] | core | ✅ Đạt |  |
| FW-UT-34 | test_parse_args_rejects[{"a": 1}] | core | ✅ Đạt |  |
| FW-UT-35 | test_resolve_data[${user.count}-2] | core | ✅ Đạt |  |
| FW-UT-36 | test_resolve_data[Xin ch\xe0o ${user.name}-Xin ch\xe0o standard_user] | core | ✅ Đạt |  |
| FW-UT-37 | test_resolve_data[${flag}/${items.1}-true/b] | core | ✅ Đạt |  |
| FW-UT-38 | test_resolve_data[value3-expected3] | core | ✅ Đạt |  |
| FW-UT-39 | test_resolve_data[kh\xf4ng c\xf3 bi\u1ebfn-kh\xf4ng c\xf3 bi\u1ebfn] | core | ✅ Đạt |  |
| FW-UT-40 | test_resolve_unknown_variable | core | ✅ Đạt |  |
| FW-UT-41 | test_resolve_uid_is_unique | core | ✅ Đạt |  |
| FW-UT-42 | test_resolve_messages_from_base_context | core | ✅ Đạt |  |
| FW-UT-43 | test_load_data_pointer_and_copy | core | ✅ Đạt |  |
| FW-UT-44 | test_load_data_via_reference | core | ✅ Đạt |  |
| FW-UT-45 | test_load_data_errors[missing.json] | core | ✅ Đạt |  |
| FW-UT-46 | test_load_data_errors[x.json#a.z] | core | ✅ Đạt |  |
| FW-UT-47 | test_mask_secrets | core | ✅ Đạt |  |
| FW-UT-48 | test_case_params_marks | core | ✅ Đạt |  |
| FW-UT-49 | test_case_params_rejects[cases0-tr\xf9ng] | core | ✅ Đạt |  |
| FW-UT-50 | test_case_params_rejects[cases1-thi\u1ebfu id] | core | ✅ Đạt |  |
| FW-UT-51 | test_case_params_rejects[cases2-tag ch\u01b0a khai b\xe1o] | core | ✅ Đạt |  |
| FW-UT-52 | test_case_params_rejects[cases3-requires kh\xf4ng h\u1ee3p l\u1ec7] | core | ✅ Đạt |  |
| FW-UT-53 | test_session_seconds_left | core | ✅ Đạt |  |
| FW-UT-54 | test_money[$29.99-expected0] | core | ✅ Đạt |  |
| FW-UT-55 | test_money[Total: $32.39-expected1] | core | ✅ Đạt |  |
| FW-UT-56 | test_money[$11.7-expected2] | core | ✅ Đạt |  |
| FW-UT-57 | test_money_rejects | core | ✅ Đạt |  |
| FW-UT-58 | test_classify_exception[error0-ASSERTION_FAILED] | core | ✅ Đạt |  |
| FW-UT-59 | test_classify_exception[error1-TIMEOUT] | core | ✅ Đạt |  |
| FW-UT-60 | test_classify_exception[error2-LOCATOR_AMBIGUOUS] | core | ✅ Đạt |  |
| FW-UT-61 | test_classify_exception[error3-NETWORK_ERROR] | core | ✅ Đạt |  |
| FW-UT-62 | test_classify_exception[error4-BROWSER_CLOSED] | core | ✅ Đạt |  |
| FW-UT-63 | test_classify_exception[error5-PLAYWRIGHT_ERROR] | core | ✅ Đạt |  |
| FW-UT-64 | test_classify_exception[error6-DATA_OR_CONTRACT_ERROR] | core | ✅ Đạt |  |
| FW-UT-65 | test_classify_exception[error7-DATA_OR_CONTRACT_ERROR] | core | ✅ Đạt |  |
| FW-UT-66 | test_classify_exception[error8-UNEXPECTED_ERROR] | core | ✅ Đạt |  |
| FW-UT-67 | test_classify_report_text[playwright._impl._errors.TimeoutError: Locator expected-TIMEOUT] | core | ✅ Đạt |  |
| FW-UT-68 | test_classify_report_text[E   AssertionError: Locator expected to have text-ASSERTION_FAILED] | core | ✅ Đạt |  |
| FW-UT-69 | test_classify_report_text[ValueError: Keyword ch\u01b0a khai b\xe1o-DATA_OR_CONTRACT_ERROR] | core | ✅ Đạt |  |
| FW-UT-70 | test_classify_report_text[-UNEXPECTED_ERROR] | core | ✅ Đạt |  |
| FW-UT-71 | test_groups | core | ✅ Đạt |  |
| FW-UT-72 | test_every_keyword_is_camel_case_and_documented | core | ✅ Đạt |  |
| FW-UT-73 | test_every_group_has_a_verify_keyword | core | ✅ Đạt |  |
| FW-UT-74 | test_duplicate_keyword_rejected | core | ✅ Đạt |  |
| FW-UT-75 | test_group_required | core | ✅ Đạt |  |
| FW-UT-76 | test_resolve_binds_method_without_browser | core | ✅ Đạt |  |
| FW-UT-77 | test_valid_steps_pass | core | ✅ Đạt |  |
| FW-UT-78 | test_invalid_steps_rejected[<lambda>-sai schema0] | core | ✅ Đạt |  |
| FW-UT-79 | test_invalid_steps_rejected[<lambda>-sai schema1] | core | ✅ Đạt |  |

