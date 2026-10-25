# Video dạy toán: bộ quy tắc

Quy tắc cho phim **dạy toán** (mọi cấp: tiểu học, THCS, THPT, Olympic) làm bằng
thư viện này. **Chỉ đọc bộ quy tắc này khi yêu cầu là video dạy toán / giải
toán / có từ "toán" / làm cho kênh Toán**; phim chủ đề khác dùng quy trình
thường của thư viện và **không** đọc tài liệu này, **không** chèn logo kênh
Toán. Nguồn sư phạm gốc nằm trong [`docs/math/`](docs/math/) — quy tắc
dưới đây đã được chuyển thể cho quy trình Lemo (treatment → style → TTS →
render → mux, rồi cover, `upload.md` và đăng ký lịch đăng sau khi video hoàn
tất). Khi có mâu thuẫn, ưu tiên mục "Rà soát trước khi gọi TTS".

Vì là phim của người dùng (ngoài `styles/`), phim toán **không có credit
LemoLab**; watermark logo kênh Toán được chèn ở bước mux theo mục
"Logo / watermark kênh".

## Cấu hình riêng cho video toán

Cấu hình dịch vụ dùng chung nằm trong `.env` tại root repository. `.env.math`
chứa `OUTPUT_DIR` và có thể ghi đè riêng `AI_QA_REQUIRED`, `AI_QA_URL`,
`AI_QA_KEY`, `AI_QA_MODEL` cho QA Toán. File `.example` chỉ là mẫu, không
được công cụ đọc khi chạy. Không ghi key thật vào file mẫu.

Công cụ QA hợp nhất cấu hình theo từng key: biến môi trường → `.env` →
`.env.math` (file project ghi đè). Chỉ chuỗi `true` (không phân biệt hoa/thường)
bật QA. Thiếu cờ hoặc giá trị khác: bỏ qua hoàn toàn, không kiểm tra key,
không gọi API. Khi đã bật, thiếu cấu hình phải dừng, không fallback provider.

Công cụ core hiện đọc `.env` và không tự đọc `.env.math`; truyền đúng đường
 dẫn/thư mục đầu ra cho công cụ đang dùng. Không giả định biến QA được core xử lý.

## QA vision có điều kiện — bắt buộc khi AI_QA_REQUIRED=true

Agent áp dụng hai cổng kiểm tra bằng `tools/math_qa.py`:

1. `assets`: sau khi có đề gốc, lời giải, lời thoại và ảnh tài nguyên thật,
   trước khi dựng/render toàn bộ video.
2. `final`: sau khi mux và sinh cover, trước khi ghi `calendar.json` và bàn giao.
   Lấy khung hình từ MP4 cuối bằng FFmpeg, ở mỗi bước giải, trước/sau chuyển
   cảnh và lúc hiện đáp án; đưa cả cover vào bộ kiểm tra. Gắn timestamp giây
   thật và ghi rõ cover trong nhãn. Nếu nhiều hơn 40 ảnh, chia thành nhiều
   manifest/batch, chạy và lưu báo cáo từng batch riêng; tất cả phải đạt.

Tạo manifest trong thư mục phim (đường dẫn tương đối với manifest):

```json
{
  "mode": "answer",
  "grade": "Lớp 2",
  "problem": "problem.md",
  "solution": "solution.md",
  "narration": "narration-timeline.md",
  "images": [
    {"path": "qa/frame-12.png", "timestamp": 12, "label": "Đọc đề"},
    {"path": "cover.png", "timestamp": 0, "label": "Cover, không phải frame video"}
  ]
}
```

`problem.md` giữ nguyên đề và dữ kiện gốc; đề dạng ảnh phải được đưa vào bộ
ảnh `assets` để đối chiếu bản chép. `narration-timeline.md` ghi lời thoại kèm
mốc bắt đầu/kết thúc thật. Manifest final dùng khung hình mới trích từ bản
render cuối, không lấy lại ảnh preview. Tách manifest assets và final.

```powershell
python tools/math_qa.py --manifest films/<phim>/qa-input-assets.json --stage assets --dry-run
python tools/math_qa.py --manifest films/<phim>/qa-input-assets.json --stage assets
python tools/math_qa.py --manifest films/<phim>/qa-input-final.json --stage final
```

Báo cáo `qa-assets.json` / `qa-final.json` được ghi cạnh manifest. Dùng tên
manifest `qa-input-assets.json` và `qa-input-final.json`. Mã thoát: 0 = đạt hoặc QA tắt,
1 = không đạt/chưa đủ bằng chứng, 2 = lỗi cấu hình/API/đầu vào. Khi bật QA,
agent chỉ qua cổng khi báo cáo có `verdict=pass`, đúng stage và SHA-256
khớp mọi đầu vào hiện tại. Sau sửa phải chạy lại những cổng bị ảnh hưởng.
Lỗi API, từ chối, kết quả thiếu hoặc chưa đủ bằng chứng đều chặn bàn giao;
không tự retry request có trạng thái chưa rõ, không đổi model ngầm.

Đây là cổng trong quy trình do agent thực hiện; các lệnh render/mux chạy
riêng không tự gọi QA. Vision chỉ xác nhận các ảnh đã xem, không chứng nhận
mọi frame hay audio. Agent vẫn nghe lời đọc, kiểm tra đồng bộ thực tế và
kiểm chứng phép tính bằng code trước khi giao.

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

- Giọng **nam** (VieNeu qua `core/tts/tts_vi.py`), gọi người học là **các em /
  các con / các bạn nhỏ**.
- **Không bao giờ xưng hô ngôi thứ nhất khi nói về mình** — không "tôi", không
  "mình", không "thầy", không "cô", không bất kỳ cách tự xưng nào khác. Người
  giảng không tự nhắc đến chính mình; viết câu không cần chủ ngữ: "Trừ năm ở
  cả hai vế…", "Chào các em…", "Chúc các em học tốt…". Quy tắc này áp dụng cho
  **mọi lời thoại** (lời giảng, hook, đọc đề, check, practice, quảng cáo kênh,
  lời chúc) và **ghi đè** quy tắc xưng "thầy" trong `docs/math/voice-text-rules.md`.
- Xưng hô kiểu rủ cùng làm như **"Nào chúng ta cùng đi tìm lời giải"** là bình
  thường (nói chung, không nhân danh mình) và được dùng thoải mái.
- Viết số và ký hiệu thành chữ trong lời đọc: `2x + 5 = 17` → "hai nhân x cộng
  năm bằng mười bảy"; `1/2` → "một phần hai"; `30%` → "ba mươi phần trăm";
  `12 cm²` → "mười hai xăng ti mét vuông". Không đưa LaTeX vào `voiceText`.
- Không emoji, Markdown, URL trong lời đọc; kết thúc câu bằng dấu chấm/dấu hỏi.
- Text trên hình giữ chữ số, ký hiệu, icon — hai phần riêng biệt.

Bảng đổi đầy đủ: [`docs/math/voice-text-rules.md`](docs/math/voice-text-rules.md).

## Giải thích rõ ràng theo cấp học

- Luôn giải thích **rõ ràng, đầy đủ, phù hợp với cấp học** của người xem —
  **không nói vắn tắt**, không lướt qua bước nào "vì nhanh". Mỗi phép biến đổi
  quan trọng phải nêu được vì sao làm và điều kiện gì cho phép làm.
- Mức độ chi tiết theo lớp đã chọn: lớp nhỏ giải thích từng thao tác nhỏ bằng
  ngôn ngữ đời thường; lớp lớn có thể gọn hơn nhưng vẫn đủ lý do ở mỗi bước
  suy luận then chốt. Không bỏ bước trung gian vì "các em tự hiểu".
- Câu kiểm tra: người xem của lớp đó nghe một lần có thể theo được trọn vẹn
  mà không cần đoán bước bị nhảy qua.

## Phụ đề: luôn tắt

Video Toán **luôn luôn tắt phụ đề**: không xuất `.srt`, không vẽ phụ đề/caption
trong trang, không burn chữ lời thoại vào hình. Chữ trên màn hình chỉ là nội
dung bài giảng (đề, công thức, sơ đồ, tiêu đề bước) do style quy định, không
phải lời thoại. Quy tắc này ghi đè các bước subtitle trong `TECHNIQUE.md`.

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

Trước lời chúc cuối, video cho kênh Toán phải đọc đúng câu quảng cáo kênh sau:
"Hãy Đăng ký kênh Toán Olympic cùng con để cùng nhau giải các bài toán khó
nhé." Không lặp nhiều lần trong một video, không đặt giữa bài giảng.

## Cover (thumbnail): sinh ảnh riêng, sau khi video hoàn tất

Sau khi mux xong, phim làm cho **kênh Toán** phải có ảnh cover `cover.png`
(ngang 16:9, 1280×720, dưới 2 MB) đặt cạnh file `.mp4` — thay cho `poster.jpg`
của phim thường. Cover là ảnh được **thiết kế riêng bằng công cụ sinh ảnh AI**, sinh **sau
khi video đã hoàn tất**: không cắt frame từ video, không chụp màn hình trang
phim, không lấy still từ phim làm cover.

Chuỗi skill bắt buộc: **image-generate → api-image → muse-image**, dùng chung
mọi loại phim. Đọc hướng dẫn skill hiện tại. image-generate gọi tool built-in trước;
khi không có/không khả dụng mới dùng api-image. api-image đọc cấu hình
`API_IMAGE_*` trong `.env`, tự quản lý gateway theo `API_IMAGE_PROVIDER`.
Không gọi lại api-image nếu image-generate đã chuyển sang nó.
Chỉ fallback sang muse-image sau khi API hết lựa chọn vì lỗi cho phép chuyển tầng.
Mọi skill đọc global trước, project ghi đè từng giá trị; thiếu cấu hình thì dừng và báo người dùng bổ sung, không chuyển tầng vì thiếu cấu hình.
Giữ nguyên prompt và yêu cầu ảnh. Lỗi đầu vào phải sửa; từ chối an toàn hoặc
job chưa rõ trạng thái phải dừng, không tự gửi lại. Hết tầng thì cover pending,
không thay bằng frame video. `.env.math` chứa thư mục đầu ra và cấu hình QA riêng nếu cần.

Agent phải gọi built-in trước. Khi đã xác minh built-in không có/không khả dụng,
có thể chạy fallback cho cover mới (không có ảnh tham chiếu):
```powershell
python tools/math_cover.py --prompt-file films/<ten-phim>/cover-prompt.txt --output films/<ten-phim>/cover.png --builtin-unavailable not-present
python tools/math_cover.py --dry-run
```
Chọn lý do thực tế, không dùng `not-present` khi tool có sẵn. Script không gọi
được tool built-in của host. `cover.result.json` ghi kết quả kỹ thuật;
agent vẫn phải xem ảnh và ghi skill/provider thực tế cùng lý do fallback trong upload.md.

Trước khi sinh ảnh, nghĩ **ba ý tưởng hook khác nhau** từ chính đề toán của
phim; mỗi ý tưởng gồm: dữ kiện thật từ đề, câu hỏi cụ thể khiến người xem muốn
biết đáp án, hành động/tương quan hình ảnh thể hiện câu hỏi đó, và tiêu đề
ngắn (không bắt buộc). Chọn ý tưởng mạnh nhất và ghi lý do chọn. Hook phải thể
hiện một câu hỏi, quan hệ bất ngờ hoặc thử thách **cụ thể**; tên chủ đề, chữ
"bí ẩn" chung chung hay dấu hỏi trang trí một mình là chưa đủ. Không bịa dữ
kiện, độ khó hay lời hứa để gây tò mò.

Dùng prompt mẫu sau, chỉ điền `{{HOOK_SCENE}}` bằng ý tưởng đã chọn (gồm dữ
kiện nguồn, câu hỏi người xem, nhân vật/đạo cụ/bối cảnh và quan hệ chưa được
giải đáp):

```
Tạo thumbnail YouTube ngang 16:9 cho kênh "Toán Olympic cùng con".
Ý TƯỞNG CẢNH: {{HOOK_SCENE}}
Phong cách hoạt hình sách truyện cao cấp, thân thiện với trẻ em. Nhân vật
biểu cảm rõ, đồ vật chính nổi bật; bối cảnh thật, mạch lạc, có chiều sâu,
chất liệu và ánh sáng ấm. Bố cục dễ hiểu khi xem nhỏ trên điện thoại,
tương phản tốt.
Ưu tiên hook: hình phải thể hiện một câu hỏi, quan hệ bất ngờ hoặc thử thách
CỤ THỂ từ dữ kiện thật trong Ý TƯỞNG CẢNH. Dùng hành động hoặc tương quan
giữa đồ vật để người xem hiểu điều chưa được giải đáp ngay ở kích thước
320×180. Khuôn mặt biểu cảm, bong bóng suy nghĩ và dấu hỏi chỉ hỗ trợ, không
thay thế câu hỏi cụ thể. Nếu thêm chữ: chỉ một tiêu đề tiếng Việt ngắn 3–5
từ làm rõ thử thách, đúng dấu, dễ đọc, cách mép an toàn; không chỉ gọi tên
chủ đề/đồ vật hoặc viết "bí ẩn" chung chung. Không tự thêm lời hứa, độ khó
hay dữ kiện để gây tò mò.
Không đưa đáp án, lời giải, toàn bộ đề bài hoặc bảng dữ kiện. Không làm ảnh
giống worksheet, slide bài giảng hay khung chữ. Không tự thêm điều kiện
toán học.
```

Rà soát **ảnh thật** ở kích thước nhỏ (~320×180, thu nhỏ xem thử), không chỉ
đọc prompt:

- Người xem nhận ra một câu hỏi cụ thể của chính đề này chỉ qua ảnh nhỏ? Ảnh
  đẹp nhưng hook mơ hồ là **rơi** — chọn ý tưởng khác hoặc sinh lại hình.
- Không lộ đáp án, phép giải hoàn chỉnh, kết quả khoanh tròn (cả hai chế độ;
  với `guided` thì tuyệt đối).
- Chữ trên ảnh (nếu có): đúng dấu tiếng Việt, đọc được ở ảnh nhỏ, cách mép
  an toàn; AI vẽ sai dấu thì sinh lại hoặc bỏ chữ.
- Số và đơn vị xuất hiện trên ảnh (nếu có) phải đúng với đề.

Ghi vào cuối `upload.md` (mục "Cover"): ba ý tưởng, ý tưởng được chọn kèm lý
do, **nguyên văn prompt** và provider đã dùng thật (`muse-image` hay
`image-generate`, `api-image`, kèm lý do nếu đã fallback).

## Tiêu đề, mô tả, caption khi đăng (`upload.md`)

Làm cùng lúc với cover: viết file `upload.md` trong thư mục phim, tiếng Việt,
sẵn sàng copy-paste khi đăng. Mọi câu chữ bám **nội dung thật** của phim (đề,
`solution.md`); không bịa nguồn, số liệu, đáp án.

- **Tiêu đề (YouTube, tối đa 60 ký tự):** hook cụ thể từ chính bài toán,
  không lộ đáp án, không câu view giả. Ví dụ "Cắt sợi dây 84 m thành ba đoạn
  bằng nhau?" tốt hơn "Bài toán về dây hay".
- **Mô tả (YouTube):** mở bằng câu hook → **đề bài đầy đủ** (nếu đề gốc
  tiếng Anh: dẫn nguyên văn tiếng Anh, kèm bản dịch tiếng Việt trung thực;
  giữ mọi điều kiện, đơn vị) → dòng `Nguồn đề:` riêng, dễ tìm kiếm: tên đầy
  đủ kỳ thi/sách kèm viết tắt chính thức (nếu đã xác minh), năm, vòng thi,
  lớp, số câu — thiếu trường nào bỏ trường đó, không rõ thì ghi "nguồn chưa
  xác minh", không đoán tên đầy đủ từ viết tắt → nội dung video dạy gì
  (kiến thức, kỹ năng) → lời mời đăng ký (dùng câu quảng cáo kênh ở mục
  "Quảng cáo kênh") → hashtag. Mốc chương (nếu thêm) phải lấy từ thời lượng
  thật của cảnh (`events.json`), không ước lượng.
- **Caption (Facebook/TikTok):** viết **độc lập** với mô tả YouTube — hook
  diễn đạt khác đi, kèm câu mời bình luận; vẫn giữ nguyên văn đề bài và dòng
  `Nguồn đề:` đầy đủ dù caption vì thế dài hơn.
- **Hashtag:** ít và đúng chủ đề — luôn có `#ToanOlympicCungCon`, thêm
  hashtag chủ đề toán (phân số, hình học…) và lớp/độ tuổi đã chọn; không tag
  trending không liên quan, không bịa tên kỳ thi.
- **Không tự chèn link ngoài** (nguồn đề, Scribd…); người dùng tự thêm tay.
- **Không xưng ngôi thứ nhất** ở mọi câu chữ (không "tôi", "mình", "thầy",
  "cô") — đồng bộ với quy tắc lời đọc.
- **Không tiết lộ đáp án hay lời giải hoàn chỉnh** trong tiêu đề, hook, đề
  bài đăng kèm — áp dụng cho cả hai chế độ.

## Đăng ký vào lịch đăng (`calendar.json`)

Bước cuối, sau cover và `upload.md`: ghi `calendar.json` **ngay trong thư mục
phim**, cạnh file `.mp4` và `cover.png` — không tạo thư mục riêng, không copy
file đi đâu. Thư mục phim nằm trong `<OUTPUT_DIR>/`, nên:

- Nếu `OUTPUT_DIR` là thư mục do app lịch đăng quản trị (ví dụ
  `D:/Affiliate/02_Content_Production/Toán Olympic Cùng Con`), app quét
  filesystem sẽ **tự nhận thư mục phim thành một campaign trên lịch** — không
  cần đăng ký gì thêm.
- Với `OUTPUT_DIR` mặc định (`films/`), `calendar.json` vẫn luôn được ghi như
  một sản phẩm bàn giao: chuyển thư mục phim vào cây calendar sau bao lâu thì
  lịch tự có ngay.

`calendar.json` ghi đúng mẫu sau (bám mẫu thật của app; nhóm trường quảng
cáo/sản phẩm giữ trống nguyên), với đường dẫn trỏ tới file thật trong thư mục
phim:

```json
{
  "id": "<yyyy-mm-dd>_<slug>",
  "title": "<tiêu đề YouTube>",
  "idea": "<tiêu đề YouTube>",
  "scheduled_date": "<yyyy-mm-dd>",
  "koc": "Toán Olympic Cùng Con",
  "product_url": "",
  "created_at": "<ISO 8601>",
  "published_at": null,
  "ai_status": "",
  "status": "SCHEDULED",
  "scheduled_time": "",
  "published_url": "",
  "item_ids": [],
  "video_meta": {
    "filename": "<tên-file-mp4>",
    "size": 0,
    "duration": 0,
    "width": 1920,
    "height": 1080,
    "codec": "h264",
    "fps": 24,
    "bitrate": 0,
    "path": "<tên-file-mp4>"
  },
  "cover_path": "cover.png",
  "tryon_photo_path": "",
  "link_placement": "none",
  "published_links": [],
  "product_urls": [],
  "product_photo_paths": [],
  "affiliate_in_caption": false,
  "products": [],
  "share_affiliate": false,
  "comment_image_path": "",
  "reference_url": "",
  "reference_platform": "",
  "reference_video_id": "",
  "bgm_source": "",
  "bgm_path": "",
  "bgm_warning": "",
  "posting_at": "",
  "tryon_photo_paths": [],
  "planned_outfit_count": 0,
  "youtube_title": "<tiêu đề YouTube>",
  "youtube_description": "<mô tả YouTube>",
  "facebook_caption": "<caption Facebook/TikTok>"
}
```

- `id` = tên thư mục phim; `title`, `idea`, `youtube_title`,
  `youtube_description`, `facebook_caption` copy nguyên văn từ `upload.md` —
  một nguồn nội dung duy nhất.
- `scheduled_date` là ngày đăng dự kiến: dùng ngày người dùng đã hẹn, không có
  thì dùng ngày hoàn tất phim (đổi ngày sau bằng kéo thả trong app).
- `status` để `SCHEDULED`; không tự điền `published_url`, `published_links`,
  `published_at` — app ghi các trường này sau khi đăng thật.
- `video_meta` đo bằng ffprobe từ file `.mp4` cuối (size, duration, codec,
  fps, bitrate), không ước lượng; `path` và `filename` là tên file `.mp4`
  thật trong thư mục phim.

## Rà soát trước khi gọi TTS

- Không còn cách xưng ngôi thứ nhất nào khi nói về mình (tôi, mình, thầy, cô…)
  trong lời thoại? "Chúng ta cùng…" thì được phép?
- Mỗi bước quan trọng được giải thích rõ ràng, đủ lý do, phù hợp cấp học —
  không có bước nào bị nói vắn tắt hay nhảy qua?
- Phụ đề đã tắt hoàn toàn (không `.srt`, không caption trong trang, không
  burn lời thoại vào hình)?
- Người học có đủ kiến thức nền cho cách giải đã chọn không?
- Các bước quan trọng có lý do, điều kiện đúng, thuật ngữ nhất quán không?
- Hình, lời đọc và công thức cùng diễn đạt một quan hệ toán học không?
- `answer`: lời giải đầy đủ, kết quả đã kiểm chứng, đáp án đúng yêu cầu đề?
- `guided`: phần tự làm có ý nghĩa và vừa sức; không lộ kết quả cuối qua bất
  kỳ kênh nào (lời đọc, phụ đề, hình, tiêu đề)?

Nguồn sư phạm: [`docs/math/math-pedagogy-rules.md`](docs/math/math-pedagogy-rules.md)
và các tài liệu gốc trong `docs/math/references/`.
