# saucedemo-e2e

Framework kiểm thử tự động **hướng dữ liệu (Data-Driven)** với **Selenium WebDriver**, ứng dụng cho website
https://www.saucedemo.com (Swag Labs). Viết bằng Python + pytest + Selenium 4 (Google Chrome), kết hợp Page Object Model.

- Kiến trúc bên trong: [ARCHITECTURE.md](ARCHITECTURE.md)
- Khảo sát trang thật (data-test, URL, thông báo nguyên văn): [docs/site-survey.md](docs/site-survey.md)
- Danh mục test case + kết quả lần chạy gần nhất (tự sinh): [TEST_CASES.md](TEST_CASES.md)

## Cài đặt

Cần Python 3.11+ và Google Chrome. Selenium Manager (đi kèm selenium) tự tải chromedriver khớp phiên bản Chrome.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env      # rồi điền SAUCE_PASSWORD (mật khẩu chung hiển thị ở trang login)
```

> Nếu máy có chromedriver cũ trong `PATH` (vd `/usr/local/bin/chromedriver`), Selenium sẽ dùng nó và báo
> `This version of ChromeDriver only supports Chrome version ...` → xoá/cập nhật file đó để Selenium Manager tự tải bản đúng.

`.env` đã được gitignore. Thiếu `SAUCE_PASSWORD` thì các test cần đăng nhập tự **skip**, phần còn lại vẫn chạy.

| Biến | Ý nghĩa | Mặc định |
|---|---|---|
| `SAUCE_PASSWORD` | Mật khẩu chung của các tài khoản saucedemo | (trống) |
| `BASE_URL` | URL trang cần test | `https://www.saucedemo.com` |
| `TEST_LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` / `ERROR` | `INFO` |

## Chạy test

```bash
.venv/bin/python -m pytest --collect-only -q          # kiểm tra dữ liệu + thu thập (không mở browser)
.venv/bin/python -m pytest tests/framework            # unit test framework, không cần mạng
.venv/bin/python -m pytest -n 4                       # toàn bộ, 4 worker song song
.venv/bin/python -m pytest -n 4 -m e2e                # chỉ UI
.venv/bin/python -m pytest -m smoke                   # bộ smoke
.venv/bin/python -m pytest -k CHK-01 --headed         # 1 case, mở cửa sổ Chrome (mặc định headless)
```

Kết quả nằm trong `artifacts/prod/`:

```text
logs/            run_<run_id>[_gwN].log
screenshots/     <run_id>/*.png      (khi FAIL)
page_sources/    <run_id>/*.html     (khi FAIL)
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
data/                auth/ inventory/ cart/ checkout/ *.json  (test case = dữ liệu)
pages/               Page Object Selenium (locator CHỈ nằm ở đây)
utils/               logging, phân loại lỗi, evidence, đọc dữ liệu, storage, thông báo
tests/framework/     unit test framework
tests/e2e/           smoke, auth, inventory, cart, checkout, menu
scripts/             sinh TEST_CASES.md
.github/workflows/   CI
```

## Viết test (data-driven)

### 1. Thêm case = thêm dữ liệu

Mỗi phần tử JSON trong `data/` là một test case; thêm case không cần sửa code. Ví dụ `data/checkout/checkout.json`:

```json
{"id": "CHK-06", "title": "Mua áo khoác + onesie", "session": "standard_user",
 "products": ["Sauce Labs Fleece Jacket", "Sauce Labs Onesie"], "itemTotal": "$57.98"}
```

| Khoá | Ý nghĩa |
|---|---|
| `id`, `title` | Bắt buộc. id duy nhất, hiện trong report và chọn được bằng `-k` |
| `session` | Chạy với phiên đăng nhập sẵn của user (đăng nhập qua UI 1 lần mỗi worker, dùng lại cookie) |
| `tags` | `["@smoke"]` → marker `smoke` |
| `requires` | `["password"]` → skip nếu thiếu `SAUCE_PASSWORD` |
| `knownBug` | Mô tả bug cố ý → `xfail(strict=True)` |

Giá trị có thể dùng biến: `"${msg.login.lockedOut}"` (thông báo nguyên văn trong `utils/messages.py`),
`"${env.password}"`, `"${uid}"`, `"@data:inventory/sorting.json#za.names"` (nạp từ file khác).

### 2. Test = luồng + so sánh với dữ liệu

Test nạp dữ liệu, tham số hoá bằng `case_params`, thao tác qua Page Object (fixture `po`) và `assert` với dữ liệu:

```python
DATA = load_data("auth/login.json")

@pytest.mark.parametrize("case", case_params(DATA["invalid"]))
def test_login_invalid(po, ctx, case):
    c = resolve_data(case, ctx)
    po.login.open()
    po.login.login(c["username"], c["password"])
    assert po.login.error_message() == c["error"]
```

### 3. Page Object mới

1. Lớp con `BasePage` trong `pages/`: `path`, `landmark`, locator dạng `by_test("data-test-value")`.
2. Thao tác nghiệp vụ bọc `@step('Mô tả "{tham_so}"')` → hiện thành Allure step + log.
3. Thêm vào `pages/page_objects.py` để dùng qua `po.<tên>`.

## Tài liệu tự sinh

```bash
.venv/bin/python scripts/gen_test_cases.py       # -> TEST_CASES.md (từ allure-results lần chạy gần nhất)
```

## CI

[.github/workflows/e2e.yml](.github/workflows/e2e.yml) chạy khi push/PR vào `main` hoặc chạy tay (chọn marker):
collect-only → `pytest -n 4` (Chrome có sẵn trên runner ubuntu) → bảng tóm tắt JUnit → upload `artifacts/prod/`.
Cần secret `SAUCE_PASSWORD` trong Settings → Secrets and variables → Actions.
