# Quy tắc thư mục đầu ra và hồ sơ sản xuất

Áp dụng cho thư mục phim của người dùng, gồm video Toán. Quy tắc này ghi đè
các ví dụ cũ đặt source, upload.md, poster, TREATMENT, CREDITS hoặc file tạm
ngay ngoài cùng. Không áp dụng để di chuyển demo trong `styles/`.

## Hợp đồng bàn giao

Ngoài cùng chỉ có đúng sáu tệp sau, cộng thư mục con phục vụ sản xuất:

```text
<yyyy-mm-dd>_<slug>/
├── cover.png
├── calendar.json
├── <slug>.mp4
├── preview.html
├── report.html
├── qa.html
└── project/
    ├── index.html
    ├── TREATMENT.md
    ├── problem.md / solution.md
    ├── lines.json / timeline.json / narration-timeline.md
    ├── upload.md / CREDITS
    ├── build.sh / build_audio.py / mix.py
    ├── audio_raw/ / audio/
    ├── build/ / assets/ / qa/
    └── logs/
```

- Một cover, một MP4 cuối; giữ tên video đang dùng nếu tái cấu trúc phim cũ.
  Không để video sạch, bản thử, backup, WAV, ảnh QA, Markdown hay script ở root.
- Cấu trúc bên trong tự chọn theo công cụ; `project/` là mặc định. Không xóa
  bằng chứng QA, lịch sử hoặc nguồn cần tái dựng chỉ để thư mục trông gọn.
- `calendar.json` ở root, đường dẫn video/cover trỏ đúng các file root thực tế.
- Bắt đầu bằng cách đọc và sao chép [docs/templates/calendar.json](docs/templates/calendar.json), không tự viết schema rút gọn hoặc lấy từ phim khác. Điền theo mục đăng ký lịch trong MATH-VIDEOS.md; kiểm đủ khóa/kiểu dữ liệu, hết placeholder, có nội dung đăng thật, metadata MP4 đã đo và đường dẫn tồn tại; lưu UTF-8 không BOM. Với file đã có, bảo toàn dữ liệu lịch/xuất bản thật thay vì ghi đè mặc định mẫu.
- Calendar phải theo schema tích hợp trong MATH-VIDEOS.md (phim Toán), có nội dung đăng bài thật và metadata MP4 đo sau mux cuối; JSON hợp lệ hoặc file tồn tại chưa đủ nghiệm thu. Không thay `koc`/`video_meta.path`/`cover_path` bằng `channel`/`video_file`/`cover_file`. Ghi rõ kiểm file hay đã xác minh trên app.
  Nội dung đăng lấy từ `project/upload.md`, đồng thời trình bày trong report.html.
- Các file phụ đề, poster, giấy phép và tài liệu nguồn của phim thường đặt
  trong project/ và liên kết từ report. Video Toán vẫn không tạo phụ đề.
- Không để secret, `.env`, token hay thông tin xác thực vào trang HTML bàn giao.

## Script riêng của phim và bản kế thừa công cụ

- Kho đầu ra không phải thư viện tham khảo. Trong lúc sản xuất, cấm liệt kê,
  quét, tìm kiếm, đọc hoặc lập chỉ mục `OUTPUT_DIR` và các phim khác, kể cả
  phim đã hoàn thiện, để lấy code, script, tài nguyên, báo cáo hoặc QA cũ.
  Chỉ truy cập đúng thư mục phim đang làm; được kiểm tra tồn tại của một tên
  thư mục cụ thể để tránh trùng tên, không liệt kê kho đầu ra. Chỉ tham khảo
  tài liệu/công cụ dùng chung và demo style theo quy trình của repository.
  Cấm sao chép hoặc chạy script từ phim đã sản xuất. Khi người dùng yêu cầu
  kiểm tra một phim cụ thể, phạm vi đọc chỉ mở cho phim được chỉ định.

- Trong lúc sản xuất phim/video, mọi script chỉ phục vụ một lượt làm phim
  phải được viết ngay trong thư mục đầu ra của phim, bên trong thư mục con
  (mặc định `project/scripts/`). Áp dụng cho Python, CMD/BAT, PowerShell,
  shell, JS/TS và mọi ngôn ngữ khác, kể cả script tạm, thử nghiệm, kiểm tra,
  sửa dữ liệu, build/mix/mux và dựng báo cáo. Quy tắc cũng áp dụng cho HTML
  khôi phục, backup, file thử, file rác và mọi đầu ra trung gian. Không để
  chúng ở root repository, `tools/` hoặc thư mục phim khác.
- Nếu tệp tạm không thể lưu trong thư mục phim hiện tại, chỉ được lưu tại
  `<library-root>/.scratch/<current-film-id>/`. Mỗi phim dùng một thư mục riêng;
  không đọc/tái sử dụng scratch của phim khác, không dùng thư mục tạm khác.
  Trước bàn giao, đưa các tệp cần để tái dựng hoặc làm bằng chứng QA về
  `project/` của phim và ghi đường dẫn cùng lý do dùng scratch trong report.
- Được gọi công cụ dùng chung hiện có mà không sửa nguồn; truyền đường dẫn
  để đầu ra/cache riêng của phim nằm trong phim khi công cụ hỗ trợ.
- Nếu công cụ của project chính cần sửa mới chạy được: tạo lớp kế thừa,
  wrapper hoặc bản sao trong đầu ra phim rồi sửa bản cục bộ đó. Không sửa
  trực tiếp nguồn dùng chung, demo hoặc cấu hình project chính để phục vụ
  lượt sản xuất. Không để bản kế thừa ghi ngược thay đổi vào repository.
- Giữ nguồn gốc: file gốc, revision Git hoặc hash nếu không có revision,
  phần thay đổi, lý do và các phụ thuộc cần thiết. Sửa import/đường dẫn tài
  nguyên cho đúng; ghi lệnh chạy thật để có thể tái dựng bằng bản cục bộ.
- Trong `report.html`, bắt buộc có mục **Điều chỉnh công cụ và đề xuất cho
  project chính**: liên kết bản cục bộ, nguồn gốc, lỗi/nhu cầu, thay đổi đã
  làm, bằng chứng kiểm chứng và giới hạn, cùng đề xuất sửa nguồn dùng chung
  cụ thể để người dùng xem xét. Phân biệt rõ bản cục bộ đã áp dụng với đề
  xuất chưa áp dụng; không tự đưa thay đổi trở lại project chính. Nếu không
  có điều chỉnh công cụ, ghi rõ không phát sinh.
- Yêu cầu sửa/bảo trì project chính do người dùng giao riêng là phạm vi
  khác; chỉ thực hiện khi có chỉ thị rõ, không suy từ việc cần hoàn tất phim.

## preview.html — mở được và xem được

- Nằm ở root; dùng source bên trong, ví dụ iframe `project/index.html` và
  audio `project/audio/mix.wav`. Không cần MP4 để chạy preview trước render.
- Hiện ngay khung đầu; có phát/dừng, tua, thời gian, tỷ lệ khung đúng và lời đọc.
  Đồng bộ hình theo audio cuối; kiểm tra tua được khi dùng server HTTP cục bộ.
- Ghi rõ preview trước mux hay đang có logo; không để người xem nhầm với MP4 cuối.
- Dùng URL tương đối, không hardcode ổ D:, đường dẫn máy, hoặc localhost:port.
  Phục vụ HTTP từ thư mục phim; chuyển cả thư mục vẫn mở được các liên kết.

## report.html — lịch sử làm việc và báo cáo tổng kết

Tuân thủ [PRODUCTION-EFFICIENCY.md](PRODUCTION-EFFICIENCY.md). **Lịch sử đầy
đủ không phải bản tóm tắt do agent viết lại:** phải lưu mọi lệnh, cwd, thời
gian thật, exit code và toàn bộ stdout/stderr (che secret), kể cả lệnh thất
bại. Dùng `tools/film_run.py` hoặc logger tương đương ngay từ đầu. Trang
report liệt kê tất cả lượt chạy và liên kết transcript HTML/output đầy đủ
trong `project/logs/commands/`; không truncate hoặc thay output bằng mô tả.
Lưu cả hành động/tool ngoài shell và kết quả thực; ghi rõ phần host không
cho xuất. Lịch sử là dữ liệu thực thi, không yêu cầu suy nghĩ nội bộ model.

Một trang HTML UTF-8 đọc được bằng trình duyệt, không cần thư viện/CDN bên
ngoài. Cập nhật trong quá trình làm, không chỉ tạo bản tóm tắt lúc bàn giao.

Bắt buộc có:

1. **Yêu cầu và quyết định:** đề/chủ đề, phong cách, cấp học/chế độ Toán,
   yêu cầu giọng/nhịp/âm thanh, thay đổi phạm vi và quyết định của người dùng.
2. **Lịch sử làm việc theo thời gian:** mốc ISO 8601 có timezone, bước thực
   hiện, đầu vào/đầu ra, công cụ/provider/model thật, lệnh đã chạy (che secret),
   kết quả thành công/thất bại và lần sửa. Phân biệt dự định và việc đã làm.
   Giữ sự kiện cũ, thêm diễn biến mới; không ghi đè lịch sử sau mỗi lần sửa.
3. **Tổng kết:** sản phẩm, thông số MP4 đo thực tế, thay đổi chính, kiểm chứng
   đã chạy và bằng chứng, trạng thái QA từng cổng, lỗi tồn đọng/giới hạn.
   Phân biệt đã sản xuất, đã kiểm tra và đủ điều kiện bàn giao.
4. **Nội dung đăng:** tiêu đề, mô tả/caption/hashtag từ upload.md; cover gồm
   ba ý tưởng, lựa chọn/lý do, prompt và provider thực tế theo quy tắc Toán.
5. **Tái dựng và nguồn:** liên kết source, treatment, credits/license, lệnh
   build/mix/mux đúng với vị trí mới; liên kết preview, MP4, cover, lịch và qa.html.
6. **Điều chỉnh công cụ và đề xuất cho project chính:** theo mục script ở
   trên; giữ lịch sử bản kế thừa và đề xuất để người dùng xem xét.

Lưu nhật ký máy đọc được ở project/logs/ (ví dụ work.jsonl) để dựng lại trang.
Với phim cũ thiếu log, chỉ ghi lịch sử truy được từ bằng chứng và đánh dấu
phần không có dữ liệu; không bịa hội thoại, lệnh hay timestamp quá khứ.

## qa.html — lịch sử trao đổi với AI QA

Trang HTML UTF-8 độc lập, dễ đọc; mặc định hiển thị trạng thái mới nhất và
danh sách mọi lượt trao đổi theo thời gian, mở rộng được chi tiết từng lượt.

Mỗi lượt lưu đủ:

- Thời gian, ID lượt, stage/scope, model/provider thực tế và trạng thái request.
- **Nội dung đã gửi:** system prompt, user prompt/context thật; danh sách ảnh
  có thumbnail/liên kết file, ID, timestamp và hash; không nhúng chuỗi base64 dài.
- **Phản hồi QA nguyên văn:** verdict, từng lỗi, vị trí, evidence và hướng sửa.
  Giữ cả response lỗi/không hợp lệ nếu có, sau khi loại secret; timeout không có
  response thì ghi đúng là chưa nhận được, không tự tạo lời đáp của model.
- **Trao đổi xử lý:** agent đã sửa gì, phản hồi/gửi lại QA nội dung nào, liên kết
  lượt kiểm tra tiếp theo và kết quả. Không ghi sửa xong nếu mới đề xuất.
- Trạng thái hiện tại và phạm vi bằng chứng: pass nội dung trước render khác
  pass vị trí logo sau mux; không lấy lượt pass cũ làm bằng chứng cho bản mới.

Lưu request/response và lịch sử xử lý trong project/qa/ hoặc project/logs/,
mỗi lượt một ID riêng, không ghi đè. Snapshot báo cáo hiện tại qa-assets.json /
qa-final.json không thay thế lịch sử. Không lưu Authorization/API key hay
dump môi trường; HTML phải escape nội dung prompt/response, không thực thi
HTML/script từ model. Ảnh được liên kết bằng đường dẫn tương đối.

Nếu `AI_QA_REQUIRED` không true: vẫn tạo qa.html, ghi **QA đã tắt, không gọi
AI**, không trình bày như đã đạt QA. Chỉ ghi các kiểm tra thủ công đã thực hiện.

## Luồng thực hiện và điều kiện hoàn tất

1. Tạo source/tài nguyên/audio/log trong thư mục con ngay từ đầu. Tạo ba trang
   root preview/report/qa sớm và cập nhật trong suốt quá trình.
2. QA nội dung và ảnh cảnh thực tế **trước render MP4**; Toán theo MATH-VIDEOS.md.
3. Build/mix ghi trung gian vào project/. Mux xuất duy nhất MP4 cuối ở root.
4. Sau MP4, AI kiểm tra vị trí/logo che nội dung và độ sạch bản giao toàn khung, không gửi lại đề/lời giải/
   narration để QA lại bài. Cover kiểm tra riêng, không lặp ảnh cảnh đã duyệt.
5. Hoàn thiện cover, lịch, tổng kết và lịch sử QA. Kiểm tra root chỉ có sáu file
   cho phép; tất cả liên kết HTML, ảnh/audio/video và đường dẫn calendar hợp lệ.
   Thiếu file hoặc thiếu lịch sử thật thì báo chưa hoàn tất, không tự điền pass.

## Tái cấu trúc phim đã có

- Kiểm kê file, script, các đường dẫn và báo cáo; lưu bản sao/mapping bên trong
  thư mục con trước khi di chuyển. Giữ nguyên MP4/cover root trong lúc chuyển.
- Cập nhật HTML asset URLs, build/mix/mux, cache/output, manifest QA, player,
  nguồn upload và calendar. Không giả định công cụ tự tìm ra đường dẫn mới.
- Script tự xác định thư mục theo vị trí file (`__file__`, `import.meta.url`,
  `$HERE`); khai báo `$LIB` đúng, không suy từ số cấp `../..` cũ sau khi chuyển.
- Việc chuyển file làm thay đổi manifest/hash: báo cáo cũ chỉ là lịch sử,
  không giả mạo thành một lượt QA mới. Có thể lưu mapping và hash chứng minh
  nội dung không đổi; không gọi AI lại toàn bài chỉ vì di chuyển đường dẫn.
- Thử preview (hình/phát/tua/audio), build, mix, mux bằng đầu ra kiểm thử bên
  trong project/; đối chiếu thông số và ảnh đại diện. Chỉ thay file bàn giao
  sau khi kiểm chứng, giữ bản cũ trong project/ cho tới khi nghiệm thu.
- Không xóa file không rõ nguồn gốc. Chỉ dọn cache tái tạo được sau nghiệm thu;
  không xóa nguồn hoặc lịch sử QA. Ghi thay đổi và kết quả vào report.html.
