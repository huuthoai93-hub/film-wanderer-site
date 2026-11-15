# Bật nút Google Play khi app lên production

Code nút "Get it on Google Play" đã viết sẵn nhưng đang nằm trong comment HTML, nên trang đang chạy vẫn hiện nút "Notify me". Khi một app lên production, làm theo các bước dưới cho app đó (FilmDesk và FilmTrail bật riêng, không cần bật cùng lúc).

Mọi chỗ cần sửa nằm trong `_build/` (nguồn để sinh trang). **Không sửa tay các file `index.html`**: lần build sau sẽ ghi đè.

## Bước 1. Tải badge Google Play chính thức (làm một lần)

Theo hướng dẫn của Google, badge phải là ảnh gốc của Google, không vẽ lại, không đổi màu. Ảnh được để ngay trong repo (không tải từ máy chủ Google mỗi lần mở trang, vì trang cam kết không theo dõi người xem).

Tải 7 file sau và lưu vào thư mục `assets/play-badge/` ở gốc repo, đúng tên file:

| Lưu thành | Tải từ |
|---|---|
| `en.png` | https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png |
| `de.png` | https://play.google.com/intl/en_us/badges/static/images/badges/de_badge_web_generic.png |
| `fr.png` | https://play.google.com/intl/en_us/badges/static/images/badges/fr_badge_web_generic.png |
| `zh-tw.png` | https://play.google.com/intl/en_us/badges/static/images/badges/zh-tw_badge_web_generic.png |
| `ja.png` | https://play.google.com/intl/en_us/badges/static/images/badges/ja_badge_web_generic.png |
| `ko.png` | https://play.google.com/intl/en_us/badges/static/images/badges/ko_badge_web_generic.png |
| `vi.png` | https://play.google.com/intl/en_us/badges/static/images/badges/vi_badge_web_generic.png |

Trên Windows (PowerShell, đứng ở thư mục gốc repo):

```powershell
New-Item -ItemType Directory -Force assets/play-badge | Out-Null
foreach ($l in "en","de","fr","zh-tw","ja","ko","vi") { Invoke-WebRequest "https://play.google.com/intl/en_us/badges/static/images/badges/${l}_badge_web_generic.png" -OutFile "assets/play-badge/$l.png" }
```

Mở thử một file: phải là badge đen chữ trắng "GET IT ON Google Play" (bản tiếng Việt là "TẢI NỘI DUNG TRÊN Google Play"), kích thước 646 × 250.

## Bước 2. Kiểm tra link Play Store

Link nằm ở `_build/site.json`:

```json
"filmdesk_play": "https://play.google.com/store/apps/details?id=io.github.huuthoai93.filmdesk",
"filmtrail_play": "https://play.google.com/store/apps/details?id=DIEN_PACKAGE_FILMTRAIL"
```

- FilmDesk: đã điền sẵn theo package `io.github.huuthoai93.filmdesk`. Mở link trên trình duyệt (đăng xuất hoặc cửa sổ ẩn danh) để chắc trang Play hiện ra.
- FilmTrail: thay `DIEN_PACKAGE_FILMTRAIL` bằng package của FilmTrail (`applicationId` trong `app/build.gradle.kts` của repo FilmTrail), hoặc dán nguyên link copy từ Play Console → Grow → Store presence → "View on Google Play".

## Bước 3a. Đổi nút: cách nhanh (một lệnh)

```
python3 _build/play_release.py filmdesk      # hoặc: filmtrail
```

Lệnh này làm đúng các việc ở Bước 3b bên dưới, rồi build lại toàn bộ trang. Nó dừng lại và báo lỗi nếu thiếu file badge hoặc link FilmTrail còn để trống. Xong thì xem `git diff`, rồi sang Bước 4.

## Bước 3b. Đổi nút: cách thủ công (nếu không dùng lệnh ở 3a)

Trong mỗi file dưới đây có các cặp khối được đánh số:

- `<!-- [GOOGLE PLAY n/N] ... xoá dòng này` … `[/GOOGLE PLAY n/N] xoá dòng này -->`: **chỉ xoá hai dòng đánh dấu này** (dòng mở comment và dòng đóng comment), giữ nguyên code ở giữa. Code ở giữa chính là nút mới.
- `<!-- [NOTIFY ME n/N] ... xoá từ dòng này -->` … `<!-- [/NOTIFY ME n/N] xoá tới dòng này -->`: **xoá cả khối**, từ dòng mở tới dòng đóng, kể cả hai dòng đó. Đây là nút "Notify me" cũ và chữ "sắp ra mắt".

Tìm nhanh bằng Ctrl+F với chữ `GOOGLE PLAY` và `NOTIFY ME`. Số dòng ghi dưới đây là lúc viết hướng dẫn, có thể lệch vài dòng.

### FilmDesk: `_build/filmdesk/template.html`

| Khối | Dòng (khoảng) | Nội dung |
|---|---|---|
| `[GOOGLE PLAY 1/4]` + `[NOTIFY ME 1/4]` | 11–16 | Mô tả khi chia sẻ link (`og:description`): "Coming soon" → "Free on Google Play" |
| `[GOOGLE PLAY 1/4, ảnh chia sẻ]` + `[NOTIFY ME 1/4, ảnh chia sẻ]` | 19–24 | Ảnh khi chia sẻ link: `og.png` (COMING SOON) → `og-play.png` (NOW ON GOOGLE PLAY, đã có sẵn trong `filmdesk/assets/`) |
| `[GOOGLE PLAY 2/4]` + `[NOTIFY ME 2/4]` | 62–81 | Đầu trang: nút "Notify me at launch" + nhãn "COMING SOON" + dòng email → badge Google Play |
| `[GOOGLE PLAY 3/4]` + `[NOTIFY ME 3/4]` | 229–252 | Cuối trang: tiêu đề "Be there on launch day." + đoạn "closed testing" + nút Notify me → tiêu đề, đoạn mới + badge |
| `[GOOGLE PLAY 4/4]` | 263–265 | Chân trang: dòng ghi chú nhãn hiệu "Google Play and the Google Play logo are trademarks of Google LLC." (Google yêu cầu khi dùng badge). Khối này không có NOTIFY ME đi kèm. |

### FilmTrail: `_build/filmtrail/landing.html`

| Khối | Dòng (khoảng) | Nội dung |
|---|---|---|
| `[GOOGLE PLAY 1/3]` + `[NOTIFY ME 1/3]` | 52–71 | Đầu trang: nút Notify me + nhãn "IN TESTING / Coming to Google Play" → badge |
| `[GOOGLE PLAY 2/3]` + `[NOTIFY ME 2/3]` | 116–135 | Cuối trang: đoạn "FilmTrail is in testing…" + nút Notify me → đoạn mới + badge (tiêu đề "Load the next roll." giữ nguyên) |
| `[GOOGLE PLAY 3/3]` | 146–148 | Chân trang: dòng ghi chú nhãn hiệu Google Play |

### Trang chủ Film Wanderer: `_build/home/home.html`

| Khối | Dòng (khoảng) | Nội dung |
|---|---|---|
| `[GOOGLE PLAY 1/2]` + `[NOTIFY ME 1/2]` | 62–67 | Nhãn trên thẻ FilmDesk: "Android · coming soon" → "Android · on Google Play" |
| `[GOOGLE PLAY 2/2]` + `[NOTIFY ME 2/2]` | 86–91 | Nhãn trên thẻ FilmTrail: "Android · in testing" → "Android · on Google Play" |

Chỉ làm khối 1/2 khi bật FilmDesk, khối 2/2 khi bật FilmTrail.

Sửa xong, build lại ở thư mục gốc repo:

```
python3 _build/build_all.py
```

## Bước 4. Kiểm tra rồi đăng

1. Chạy `git diff`: các file `index.html` của app đó (7 ngôn ngữ) và trang chủ phải đổi; không còn chữ `Notify me` trong `filmdesk/index.html` (hoặc `filmtrail/index.html`).
2. Xem thử trên máy: `python3 -m http.server 8000` ở gốc repo, mở `http://localhost:8000/filmdesk/` và `http://localhost:8000/filmdesk/vi/`. Badge hiện ở đầu và cuối trang, đúng ngôn ngữ, bấm vào mở trang Play của app. Thử cả bề ngang điện thoại.
3. Commit cả `_build/`, `assets/play-badge/` và các file `index.html` sinh ra, push lên `main` (GitHub Pages tự đăng sau vài phút).
4. Sau khi đăng, dán link trang vào Facebook Sharing Debugger (https://developers.facebook.com/tools/debug/) và bấm "Scrape Again" để Facebook/Zalo cập nhật ảnh và mô tả mới khi chia sẻ link (chỉ FilmDesk có ảnh chia sẻ đổi).

## Chữ mới nằm ở đâu

Các câu dùng sau khi phát hành đã dịch sẵn 7 ngôn ngữ, muốn sửa thì sửa ở:

- FilmDesk: `_build/filmdesk/i18n/<ngôn ngữ>.json`, các khoá `play_alt` (chữ thay thế của badge), `play_legal`, `og_description_live`, `closing_h_live`, `closing_p_live`.
- FilmTrail: `_build/filmtrail/i18n/<ngôn ngữ>.json`, các khoá `play_alt`, `play_legal`, `closing_p_live`.
- Trang chủ: `_build/home/i18n.json`, các khoá `fd_status_live`, `ft_status_live`.

Các khoá cũ (`notify`, `notify_small`, `notify_note`, `soon`, `status_small`, `mail_subject`, `mail_body`, `closing_p`…) không còn được dùng sau khi bật, có thể để nguyên hoặc dọn sau.

## Còn lại cần tự kiểm

- `PRODUCT.md` đang ghi "FilmDesk: sắp ra mắt trên Google Play. FilmTrail: đang thử nghiệm.": sửa tay khi phát hành.
- Trang chính sách (`privacy/`) vẫn dùng `og.png` cũ làm ảnh chia sẻ; không ảnh hưởng gì nếu không ai chia sẻ link chính sách.
