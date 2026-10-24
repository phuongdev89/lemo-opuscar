# Video dạy toán: bộ quy tắc

Quy tắc cho phim **dạy toán** (mọi cấp: tiểu học, THCS, THPT, Olympic) làm bằng
thư viện này. **Chỉ đọc bộ quy tắc này khi yêu cầu là video dạy toán / giải
toán / có từ "toán" / làm cho kênh Toán**; phim chủ đề khác dùng quy trình
thường của thư viện và **không** đọc tài liệu này, **không** chèn logo kênh
Toán. Nguồn sư phạm gốc nằm trong [`docs/math/`](docs/math/) — quy tắc
dưới đây đã được chuyển thể cho quy trình Lemo (treatment → style → TTS →
render → mux). Khi có mâu thuẫn, ưu tiên mục "Rà soát trước khi gọi TTS".

Vì là phim của người dùng (ngoài `styles/`), phim toán **không có credit
LemoLab**; watermark logo kênh Toán được chèn ở bước mux theo mục
"Logo / watermark kênh".

## Trách nhiệm của agent

Agent đọc đề, **giải và kiểm chứng độc lập trước** khi viết kịch bản. Kiểm tra
bằng phép thay nghiệm, tính ngược, đơn vị, điều kiện xác định, từng trường
hợp. Khi thiếu dữ kiện, ảnh mờ hoặc chưa kiểm chứng được đáp án: báo rõ, không
dựng video khẳng định kết quả chưa có căn cứ. Trình bày **lời giải đầy đủ cho
người tạo** trong chat trước khi sản xuất; với chế độ hướng dẫn, phần này không
được lọt vào video.

## Xác định lớp trước khi giải

Nếu người dùng chưa nêu lớp/trình độ: phân tích từ đề (chủ đề, kiến thức tiên
quyết, loại phép toán, ký hiệu) rồi hỏi người dùng chọn lớp trong khoảng phù
hợp, đánh dấu lớp khuyến nghị kèm lý do ngắn. Không suy lớp từ độ lớn con số
hay tên file. Sau khi có lớp, điều chỉnh thuật ngữ, phương pháp và mức gợi ý
theo lớp đó; không khẳng định bài thuộc chương trình lớp cụ thể nếu chỉ suy đoán.

## Hai chế độ giải — hỏi trước khi làm

Trước khi giải, hỏi người dùng đúng hai lựa chọn:

| Chế độ | Cách dạy |
|---|---|
| **Giải ra đáp án** (`answer`) | Trình bày đủ bước và lý do, kiểm tra, công bố đáp án trước lời chúc |
| **Hướng dẫn và để ngỏ** (`guided`) | Giải thích phương pháp, các bước cần thiết; chừa lại đúng một bước suy luận/tính toán có ý nghĩa để người học tự làm; **không** công bố kết quả cuối |

Với `guided`: không phải giải hết rồi che con số cuối. Lời giải đầy đủ lưu
riêng trong `solution.md` của thư mục phim để kiểm chứng nội bộ; rà soát lời
đọc, phụ đề, tiêu đề, sơ đồ, công thức, lựa chọn trắc nghiệm để không lộ đáp
án ở bất kỳ đâu. Kết thúc bằng nhiệm vụ tự làm (`practice`) rồi lời chúc.

## Nguyên tắc sư phạm (từ docs/math)

1. **Giải thích lý do.** Nêu ý nghĩa và điều kiện của phép biến đổi quan trọng,
   không chỉ đọc công thức; mô tả vì sao chọn hướng giải này.
2. **Làm rõ ký hiệu.** Giải thích biến, đơn vị, quan hệ sơ đồ với công thức.
   Không suy ra tính chất chỉ vì hình trông đúng.
3. **Phù hợp kiến thức nền.** Chỉ dùng thuật ngữ/method người học của lớp đó
   theo được; nhắc kiến thức mới trước khi dùng; không dùng mẹo vượt cấp làm
   lời giải chính khi chưa giải thích cơ sở.
4. **Gợi ý vừa đủ.** Nhận diện dữ kiện → chọn hướng → gợi ý bước cụ thể; chọn
   mức gợi ý theo trình độ dự kiến.
5. **Xử lý hiểu lầm có mục đích.** Nếu có lỗi dễ gặp, chỉ rõ vì sao sai và cách
   sửa; không dùng lời chê.
6. **Chừa cơ hội suy nghĩ.** Mời người học tạm dừng video để tự làm; đặt câu
   hỏi cụ thể ("Vì sao cần trừ ở cả hai vế?") thay vì "Các em hiểu chưa?".
7. **Giữ mạch bài rõ.** Mỗi cảnh một ý chính; lời giảng khớp với công thức đang
   hiển thị; không thêm cảnh/hiệu ứng không giúp hiểu.

Minh họa (đồ vật, đường cắt, nhóm vật) phải xuất hiện ngay khi lời giảng dùng
đến; cue theo từng ý: hiện vật → tô/nhóm đang nói tới → cắt/tách theo lời đọc →
giữ kết quả để quan sát. Icon đúng với đề (sticker, cốc, cây…); khi nói cắt/tách
thì diễn hoạt đúng phần được lấy ra. Trong `guided`, minh họa không được lộ
bước quyết định hoặc đáp án.

## Lời đọc tiếng Việt

- Giọng **nam** (VieNeu qua `core/tts/tts_vi.py`), xưng **thầy**, gọi **các em /
  các con / các bạn nhỏ**. Không dùng "cô".
- **Cấm mọi đại từ nhân xưng ngôi thứ nhất trong lời thoại** (tôi, mình, chúng
  ta, chúng tôi, tao…). "Thầy" là danh từ chỉ vai, không phải đại từ, nên là
  cách xưng duy nhất được dùng khi cần tự nhắc; ưu tiên viết câu không cần chủ
  ngữ ("Trừ năm ở cả hai vế…" thay vì "Thầy sẽ trừ…"). Quy tắc này áp dụng cho
  **mọi lời thoại**: lời giảng, hook, đọc đề, check, practice, quảng cáo kênh và
  lời chúc.
- Viết số và ký hiệu thành chữ trong lời đọc: `2x + 5 = 17` → "hai nhân x cộng
  năm bằng mười bảy"; `1/2` → "một phần hai"; `30%` → "ba mươi phần trăm";
  `12 cm²` → "mười hai xăng ti mét vuông". Không đưa LaTeX vào `voiceText`.
- Không emoji, Markdown, URL trong lời đọc; kết thúc câu bằng dấu chấm/dấu hỏi.
- Text trên hình giữ chữ số, ký hiệu, icon — hai phần riêng biệt.

Bảng đổi đầy đủ: [`docs/math/voice-text-rules.md`](docs/math/voice-text-rules.md).

## Cấu trúc video

Mở đầu bằng **hook là thử thách của chính bài toán**: chào ngắn → nhiệm vụ hôm
nay → điều kiện quan trọng → một câu hỏi khiến người học muốn thử. Không dùng
lời giới thiệu chung ("bài toán rất thú vị"), không tiết lộ đáp án.

Thứ tự cảnh: `introduction → problem (đọc nguyên văn đề) → strategy →
solution (mỗi cảnh một bước, đủ lý do) → check (cách tự kiểm tra) → answer
(chỉ ở chế độ answer) → closing (câu quảng cáo kênh, rồi lời chúc)`.

Với `guided`: `… → solution (chưa hoàn tất đáp án) → check → practice → closing`.

Không ép độ dài; không bỏ giả thiết, điều kiện xác định, trường hợp hay bước
kiểm tra. Kiểm tra chữ và thời gian đọc trên hình bằng
`node core/render/readcheck.mjs`.

## Logo / watermark kênh

Video làm cho **kênh Toán** phải được mux với `LEMO_LOGO=default` để chèn
watermark logo kênh ("Toán Olympic cùng con", file `core/assets/logo.png`):
góc trên bên trái theo mặc định, hoặc góc dưới bên phải qua `LEMO_LOGO_POS=br`;
đổi kích thước/độ mờ qua `LEMO_LOGO_SCALE` / `LEMO_LOGO_ALPHA`. Phim không
phải làm cho kênh Toán thì **không** chèn logo (để mặc định, không set
`LEMO_LOGO`). Không vẽ logo trong trang; logo chỉ nằm ở bước mux.

## Quảng cáo kênh

Trước lời chúc cuối, video cho kênh Toán phải đọc một câu quảng cáo kênh ngắn,
ví dụ: "Nếu video hữu ích, các em hãy Đăng ký kênh Toán Olympic cùng con và
bấm chuông để không bỏ lỡ bài mới nhé." Không lặp nhiều lần trong một video,
không đặt giữa bài giảng.

## Rà soát trước khi gọi TTS

- Không còn đại từ ngôi thứ nhất nào trong lời thoại (tôi, mình, chúng ta…;
  chỉ còn "thầy" khi cần tự nhắc)?
- Người học có đủ kiến thức nền cho cách giải đã chọn không?
- Các bước quan trọng có lý do, điều kiện đúng, thuật ngữ nhất quán không?
- Hình, lời đọc và công thức cùng diễn đạt một quan hệ toán học không?
- `answer`: lời giải đầy đủ, kết quả đã kiểm chứng, đáp án đúng yêu cầu đề?
- `guided`: phần tự làm có ý nghĩa và vừa sức; không lộ kết quả cuối qua bất
  kỳ kênh nào (lời đọc, phụ đề, hình, tiêu đề)?

Nguồn sư phạm: [`docs/math/math-pedagogy-rules.md`](docs/math/math-pedagogy-rules.md)
và các tài liệu gốc trong `docs/math/references/`.
