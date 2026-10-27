# Sản xuất tập trung, có đầy đủ bằng chứng

Áp dụng cho mọi lượt làm phim. Đây là quy tắc ưu tiên hơn demo và ví dụ cũ.

## Chỉ dùng style có sẵn

- Chỉ chọn trong thư viện hoặc style riêng đã tồn tại trước lượt sản xuất.
  Cấm tạo, fork, đăng ký, đổi tên hoặc code thêm style trong lúc làm phim;
  kể cả tạo biến thể để vượt QA. Không tự ghi vào `~/lemo-my-styles/`.
- Yêu cầu người dùng về giọng, âm thanh, phụ đề và nền ưu tiên hơn demo.
  Không tranh luận nhiều lượt để giữ mặc định demo trái yêu cầu. Nếu bất
  biến thị giác vẫn không phù hợp, đổi sang style có sẵn tương thích.
- Code nội dung/hoạt cảnh của phim theo style đã chọn vẫn cần thiết;
  không biến việc này thành xây engine, thiết kế style mới hay viết lại renderer.
- Không mặc định chọn bảng neon/HUD. Đề xuất tối đa ba style có sẵn, ưu tiên
  ít nhất hai lựa chọn không neon và không giấy trắng nếu thư viện phù hợp.
  Glow chỉ làm điểm nhấn cần thiết; không phủ cả bài bằng bảng phát sáng.

## Giới hạn công việc và xử lý lỗi

- Dùng renderer, TTS, mix/mux hiện có. Không refactor, nâng cấp, benchmark,
  cài lại toàn bộ stack hoặc xây công cụ thay thế chỉ để làm một phim.
- Kế hoạch style khoảng 300–500 từ ngoài bản STYLE.md nguyên gốc; treatment
  ngắn, ba cấu trúc chỉ cần phác thảo. Không viết lại quy tắc ở nhiều tài liệu.
- Xác minh công cụ bằng một frame đại diện trước khi dựng đầy đủ. Kiểm
  văn bản UTF-8, công thức, font, đường dẫn và layout trước gọi vision.
- Khi công cụ lỗi: đọc lỗi, sửa cục bộ tối thiểu trong output phim, tối đa
  hai lần thử cho cùng nguyên nhân hoặc 10 phút chẩn đoán/sửa tích cực,
  tùy ngưỡng nào đến trước (không tính chờ provider/render). Sau đó dùng
  đường chạy hiện có đã biết hoạt động; nếu không có thì báo blocker cụ thể
  và bằng chứng. Không viết lại công cụ hoặc ngồi sửa vô hạn.
- Không áp giới hạn này để bỏ qua sai toán, chữ không đọc được, nội dung bị
  che hoặc yêu cầu bắt buộc. Lỗi thật chưa xử lý thì chưa được giao là PASS.
- Với phim đơn giản, lấy dưới 60 phút làm mục tiêu điều phối, không phải lời
  hứa hay lý do giảm chất lượng. Ghi thời lượng phim thực, thời gian chạy từng
  phase, số lần gọi QA, render, mux và sinh cover. Báo sớm khi vượt kế hoạch.

## QA đủ phạm vi, tránh kiểm lặp

- Chỉ gọi AI khi `AI_QA_REQUIRED=true`. Style tham vấn ngắn ngay đầu;
  xử lý blocker/fix theo bằng chứng, suggestion không tự thành vòng sửa bắt buộc.
- QA nội dung hoàn chỉnh trước full render. Gom lỗi vào một lượt sửa.
  Lượt sau chỉ gửi cảnh/tài liệu thay đổi và ngữ cảnh phụ thuộc cần thiết;
  giữ liên kết/hash đến các batch đã duyệt không đổi để chứng minh đủ phạm vi.
- Không gửi lại toàn bộ cảnh để kiểm cover. Cover dùng manifest và thư mục
  batch riêng, không ghi đè kết quả QA video. Tránh yêu cầu AI sinh lưới đếm,
  sơ đồ hoặc chữ toán chính xác khi có thể dùng hình học code-native của phim.
- Chỉ render toàn bộ sau khi preview/nội dung đạt. Sau MP4 chỉ kiểm logo;
  sửa logo thì mux từ video sạch. Thay nội dung mới quay về assets phần liên quan.
- Mỗi lượt QA giữ request/response/result riêng, kể cả fail/error. Snapshot
  mới không thay lịch sử. Pass cũ hết giá trị với đầu vào đã thay đổi; không
  lấy report/qa HTML viết trước lần sửa cuối làm trạng thái bàn giao.

## Toàn bộ log thực thi

- Bắt đầu ghi ngay từ lệnh đầu: thời gian thật ISO 8601 có timezone, cwd,
  argv/lệnh đầy đủ, phase, stdout và stderr đầy đủ (kể cả lỗi), exit code,
  thời điểm kết thúc và thời lượng. Không cắt output vì dài hoặc chỉ chép
  dòng thành công. Che secret trước lưu; không dump env hay đọc/in `.env`.
- Bắt buộc chạy lệnh sản xuất qua logger sẵn có, hoặc cơ chế tương đương:

  ```powershell
  python tools/film_run.py --film "<film-output>" --cwd "<library-root>" --phase render -- node core/render/video.mjs <actual-arguments>
  ```

  Với shell syntax, truyền interpreter rõ ràng, ví dụ `powershell -NoProfile
  -Command <command>` hoặc `bash <script>`. Không dựng thêm logger riêng mỗi phim.
  Bí mật dùng biến môi trường, không truyền literal trong argv. Wrapper che
  secret đã biết từ môi trường và mẫu token thông dụng; không bảo đảm phát
  hiện mọi secret tự do, nên tuyệt đối không chủ động in credential.
- Logger lưu từng lệnh tại `project/logs/commands/<id>/`: command.json,
  output.txt (stdout/stderr gộp theo thứ tự nhận), index.html mở xem toàn văn.
  Mở log trước gọi tiến trình; nếu bị ngắt, trạng thái running chưa có exit
  phải được ghi nhận interrupted/unknown, không suy là thành công.
- Tool không qua shell (read/write/edit/browser/provider) cũng lưu sự kiện
  và kết quả thật trong nhật ký append-only, kèm diff/ảnh/artifact cần thiết.
  Xuất transcript phiên đầy đủ nếu host hỗ trợ; nếu không, nói rõ giới hạn,
  giữ mọi dữ liệu thực quan sát được. Không yêu cầu hay giả tạo suy nghĩ nội bộ.
- `report.html` phải có bảng tất cả lệnh, kết quả, thời lượng và liên kết
  output đầy đủ, cùng lịch sử hành động và tổng kết. Không tự bịa giờ tròn,
  suy thời gian thực thi từ mtime hay tái tạo output không còn lưu.
- Hai phim cũ thiếu dữ liệu phải ghi thiếu; các thay đổi này không phục hồi
  được những log chưa từng thu thập. Không tuyên bố đã xuất đầy đủ quá khứ.
