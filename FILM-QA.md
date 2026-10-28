# QA cho mọi loại phim

Áp dụng cho tất cả phim được sản xuất, mọi chủ đề, style và ngôn ngữ.
Cấu hình hợp nhất theo từng key: biến môi trường → `.env` của repository.
Riêng phim giải toán đọc `.env.math` **sau cùng**, kể cả cờ bật/tắt;
phim khác không đọc file này. File mẫu không được nạp khi chạy.
Chỉ chuỗi `true` (không phân biệt hoa thường, bỏ khoảng trắng) bật QA.
Khi tắt: không gọi API, không kiểm tra cấu hình dịch vụ; agent vẫn tự kiểm.
Khi bật: cần `AI_QA_URL`, `AI_QA_KEY`, `AI_QA_MODEL`; thiếu cấu hình,
API lỗi, từ chối, fail hoặc insufficient_evidence đều chặn cổng liên quan.
Không tự đổi provider/model, không retry khi trạng thái job chưa rõ.

## Ba cổng bắt buộc khi bật

1. `style`: gửi brief, toàn văn style có sẵn và đề xuất cụ thể trước khi
   chốt hướng hình ảnh, tạo ảnh, TTS hoặc animation. Giữ style người dùng chọn
   và các override về giọng/nhạc/SFX/phụ đề. Sửa blocker/fix rồi duyệt lại.
2. `assets`: kiểm nội dung, dữ kiện/nguồn, diễn tiến, lời thoại có timeline,
   style và ảnh preview thực tế của từng bố cục/bước quan trọng, gồm cover
   ở batch riêng. Đủ sáu kiểm tra hình ảnh như QA toán. Duyệt trước full render.
   Agent kiểm âm thanh thực tế riêng; ảnh tĩnh không chứng nhận âm thanh/chuyển động.
3. `final`: công cụ trích frame từ MP4 sau mux để kiểm logo nếu có và độ sạch
   toàn khung. Lấy timestamp đại diện mọi bố cục, không suy diễn khoảng chưa xem.
   Không yêu cầu logo ở phim không có brief yêu cầu logo; logo xuất hiện vẫn
   không được che nội dung. Không thêm watermark/credit LemoLab cho phim người dùng.

Manifest phim thường, đường dẫn tương đối với manifest, nằm trong folder phim:

```json
{
  "brief": "brief.md",
  "style": "style-spec.md",
  "proposal": "style-proposal.md",
  "narration": "narration-timeline.md",
  "logo_required": false,
  "images": [{"path": "preview/scene-1.png", "timestamp": 0}]
}
```

Ở `style`, bỏ `images` và `narration`. Brief chứa yêu cầu, dữ kiện/nguồn,
ngôn ngữ và cấu hình âm thanh/phụ đề; proposal chứa bố cục, nhịp và override.
Phim không lời vẫn cung cấp tài liệu narration ghi rõ không có lời và timeline cảnh.
Ở `final`, chỉ cần `video`, `logo_required` và `images` (ID duy nhất + timestamp
không âm); không gửi lại brief/nội dung. Logo bắt buộc thì đặt `logo_required=true`.

```powershell
python tools/film_qa.py --manifest <film>/project/qa-input-style.json --stage style
python tools/film_qa.py --manifest <film>/project/qa-input-assets.json --stage assets
python tools/film_qa.py --manifest <film>/project/qa-input-final.json --stage final
```

Thêm `--dry-run` để kiểm đầu vào/cấu hình mà không gọi API; không coi là PASS.
Phim giải toán dùng `--film-type math` hoặc lệnh tương thích `tools/math_qa.py`,
với manifest và toàn bộ yêu cầu riêng trong [MATH-VIDEOS.md](MATH-VIDEOS.md).
Không áp giọng Minh Quân Pro, cấm nhạc, lớp hoặc chế độ giải toán lên phim thường.

Mỗi batch tối đa 40 ảnh, không tự cắt bớt. Cơ chế hash, lưu từng request/response,
manifest/result và mã thoát dùng chung: 0 đạt hoặc tắt; 1 fail/thiếu bằng chứng;
2 lỗi. Giữ lịch sử thực trong qa.html, không ghi PASS cứng. Chỉ đầu vào hiện tại
đã được duyệt mới có hiệu lực; sửa phần nào QA lại phần đó và ngữ cảnh liên quan.
Đây là cổng agent bắt buộc thực hiện; chạy render/mux trực tiếp không tự gọi QA.
