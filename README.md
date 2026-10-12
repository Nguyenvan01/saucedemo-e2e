# saucedemo-e2e

Framework kiểm thử tự động cho https://www.saucedemo.com (Swag Labs) theo mô hình
**Hybrid = Page Object + Keyword-Driven + Data-Driven**, viết bằng Python + pytest + Playwright (Chromium).

- Kiến trúc bên trong: [ARCHITECTURE.md](ARCHITECTURE.md)
- Khảo sát trang thật (data-test, URL, thông báo nguyên văn): [docs/site-survey.md](docs/site-survey.md)
- Danh mục keyword (tự sinh): [KEYWORDS.md](KEYWORDS.md)
- Danh mục test case + kết quả lần chạy gần nhất (tự sinh): [TEST_CASES.md](TEST_CASES.md)

## Cài đặt

Cần Python 3.11+.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
cp .env.example .env      # rồi điền SAUCE_PASSWORD (mật khẩu chung hiển thị ở trang login)
```

`.env` đã được gitignore. Thiếu `SAUCE_PASSWORD` thì các test cần đăng nhập tự **skip**, phần còn lại vẫn chạy.

| Biến | Ý nghĩa | Mặc định |
|---|---|---|
| `SAUCE_PASSWORD` | Mật khẩu chung của các tài khoản saucedemo | (trống) |
| `BASE_URL` | URL trang cần test | `https://www.saucedemo.com` |
| `TEST_LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` / `ERROR` | `INFO` |
| `SLOW_MO` | Làm chậm thao tác (ms) để quan sát | — |

## Chạy test

```bash
.venv/bin/python -m pytest --collect-only -q          # kiểm tra dữ liệu + thu thập (không mở browser)
.venv/bin/python -m pytest tests/framework            # unit test framework, không cần mạng
.venv/bin/python -m pytest -n 4                       # toàn bộ, 4 worker song song
.venv/bin/python -m pytest -n 4 -m e2e                # chỉ UI
.venv/bin/python -m pytest -m smoke                   # bộ smoke
.venv/bin/python -m pytest -m keyword                 # kịch bản Excel
.venv/bin/python -m pytest -k CHK-01 --headed         # 1 case, mở trình duyệt
```

Kết quả nằm trong `artifacts/prod/`:

```text
logs/            run_<run_id>[_gwN].log
screenshots/     <run_id>/*.png      (khi FAIL)
page_sources/    <run_id>/*.html     (khi FAIL)
traces/          <run_id>/*/trace.zip, video (khi FAIL) -> xem: .venv/bin/python -m playwright show-trace <file>
junit/results.xml
allure-results/  -> xem: allure serve artifacts/prod/allure-results
```

## Tài khoản và bug cố ý

| User | Dùng để |
|---|---|
| `standard_user` | Luồng chuẩn |
| `locked_out_user` | Đăng nhập bị khoá |
| `performance_glitch_user` | Đăng nhập chậm ~5 s (không phải bug, chỉ cần timeout đủ) |
| `problem_user`, `error_user`, `visual_user` | Lỗi cố ý của site → khai báo `knownBug` trong dữ liệu, test hiện **xfail** |

`knownBug` = `xfail(strict=True)`: nếu một ngày site sửa lỗi, test PASS sẽ bị báo **FAIL (XPASS strict)**
để nhắc gỡ `knownBug`. Không sửa test cho pass.

## Cấu trúc

```text
config.py            cấu hình, đọc .env
data/                auth/ inventory/ cart/ checkout/ *.json ; scenarios/*.xlsx
pages/               Page Object (locator CHỈ nằm ở đây)
keywords/            7 nhóm keyword: common, auth, inventory, product, cart, checkout, menu
drivers/             driver_script.py: chạy kịch bản keyword-driven
utils/               logging, phân loại lỗi, evidence, đọc dữ liệu, storage, thông báo
tests/framework/     unit test framework
tests/e2e/           smoke, auth, inventory, cart, checkout, menu, keyword_driven
scripts/             sinh KEYWORDS.md, TEST_CASES.md, data/scenarios/*.xlsx
.github/workflows/   CI
```

## Viết test

### 1. Data-driven (JSON + pytest)

Thêm case = thêm phần tử JSON, không sửa code. Ví dụ `data/checkout/checkout.json`:

```json
{"id": "CHK-06", "title": "Mua áo khoác + onesie", "session": "standard_user",
 "products": ["Sauce Labs Fleece Jacket", "Sauce Labs Onesie"], "itemTotal": "$57.98"}
```

| Khoá | Ý nghĩa |
|---|---|
| `id`, `title` | Bắt buộc. id duy nhất, hiện trong report và chọn được bằng `-k` |
| `session` | Chạy với phiên đăng nhập sẵn của user (đăng nhập qua UI 1 lần, lưu `.auth/`) |
| `tags` | `["@smoke"]` → marker `smoke` |
| `requires` | `["password"]` → skip nếu thiếu `SAUCE_PASSWORD` |
| `knownBug` | Mô tả bug cố ý → `xfail(strict=True)` |

Giá trị có thể dùng biến: `"${msg.login.lockedOut}"` (thông báo nguyên văn trong `utils/messages.py`),
`"${env.password}"`, `"${uid}"`, `"@data:inventory/sorting.json#za.names"` (nạp từ file khác).

Test chỉ gọi keyword:

```python
@pytest.mark.parametrize("case", case_params(DATA["purchase"]))
def test_purchase(k, ctx, case):
    k.inventory.add_products_to_cart(case["products"])
    k.cart.open_cart()
    ...
```

### 2. Keyword-driven (Excel)

Kịch bản nằm trong `data/scenarios/*.xlsx`, **sinh bằng** `scripts/gen_scenarios_xlsx.py`
(sửa định nghĩa trong script rồi chạy lại, đừng sửa tay file .xlsx):

```bash
.venv/bin/python scripts/gen_scenarios_xlsx.py
```

- Sheet `TestSteps`: `template_id | step | keyword | args | note` — `args` là mảng JSON, placeholder `{cot}`.
- Sheet `TestData`: `case_id | template_id | title | tags | requires | known_bug | <cột placeholder...>` —
  mỗi dòng là 1 test case.
- Mỗi kịch bản phải có ít nhất 1 bước `verify*` / `…Expecting…`; sai schema / keyword lạ / thiếu placeholder
  báo lỗi ngay lúc `--collect-only`.

### 3. Keyword mới

1. Locator trong `pages/` (ưu tiên `get_by_test_id`, sau đó `get_by_role`).
2. Method có `@keyword("tenCamelCase")` + docstring 1 dòng trong `keywords/kw_<nhóm>.py`, thân bọc `with self.step(...)`.
3. Cập nhật tài liệu: `.venv/bin/python scripts/gen_keywords_doc.py`.

## Tài liệu tự sinh

```bash
.venv/bin/python scripts/gen_keywords_doc.py     # -> KEYWORDS.md
.venv/bin/python scripts/gen_test_cases.py       # -> TEST_CASES.md (từ allure-results lần chạy gần nhất)
```

## CI

[.github/workflows/e2e.yml](.github/workflows/e2e.yml) chạy khi push/PR vào `main` hoặc chạy tay (chọn marker):
collect-only → `pytest -n 4` → bảng tóm tắt JUnit → upload `artifacts/prod/`.
Cần secret `SAUCE_PASSWORD` trong Settings → Secrets and variables → Actions.
