## Goal
Xây dựng báo cáo khoa học dự báo tỷ lệ sử dụng trạm sạc xe điện (EV utilization rate) từ dữ liệu `EV-pro1_forcast.csv` và hỗ trợ Tư lệnh nắm vững kiến thức chuyên sâu để bảo vệ đồ án thành công.

## Constraints
- Resample dữ liệu về 1 hour/step. Dự báo t+24 hours.
- So sánh RF, LSTM, LGBM, XGBoost.
- Sử dụng Custom Loss Function để bắt peak fluctuation.
- Báo cáo phải được viết bằng LaTeX, theo cấu trúc 4 phần (Intro, Material/Method, Results/Discussion, Conclusion).
- Thêm file `defense_qa.md` để giải thích chuyên sâu các quyết định thiết kế.

## Progress & Changelog
- Khởi tạo chiến dịch: Xác định bài toán, biến mục tiêu và phương pháp luận chính.
- **Pivot/Cập nhật:** Tư lệnh bổ sung yêu cầu không chỉ viết báo cáo mà còn cần hiểu sâu sắc (deeply understand) để bảo vệ đồ án (final exam). Cập nhật lại Idea.md để bổ sung luồng tài liệu "Defense Q&A".
- **Pivot/Cập nhật:** Cấu trúc code chuyển sang Functional/Procedure (TUYỆT ĐỐI KHÔNG DÙNG OOP).
- Bổ sung **Task 1.5 (Feature Engineering):** Đã tạo các biến Lag (1, 2, 24) và Rolling Window (3h, 6h) trước khi chia tập dữ liệu.
- Hoàn thành **Task 2 (Custom Loss):** Triển khai hàm `peak_weighted_objective` phạt nặng (x5) sai số tại các ngưỡng Peak (>= 0.8).
- Hoàn thành **Task 3 (Modeling & Tuning):** Khắc phục lỗi tương thích dtype của PyTorch LSTM và LightGBM. Toàn bộ 4 mô hình (RF, LGBM, XGBoost, LSTM) đã được Optuna tuning thành công với Features và Custom Loss mới. Cất cánh sang Task 4.
- **[TRẠNG THÁI HIỆN TẠI]:** Hệ thống đang TẠM DỪNG (PAUSED) theo lệnh của Tư lệnh để tiêu hóa kết quả trước khi sang Task 4.

## Key Decisions
- Biến mục tiêu: `utilization_rate`.
- Phương pháp luận: Custom Loss được dùng trực tiếp trong training/tuning thay vì chỉ dùng metric chuẩn trên peak hours.
- Output: LaTeX Report + Defense Q&A Documentation.
- Cấu trúc Code: Kiến trúc 3-file (`main.py`, `core_functions.py`, `utils.py`), **NO OOP**.

## Next Steps
- Lập ACTION_PLAN.md (Phân rã công việc chi tiết - Breakdown tasks) theo kỹ năng `planning-and-task-breakdown`.

## Critical Context
- Dữ liệu `EV-pro1_forcast.csv` có mẫu 30-phút, cần resample về 1 giờ.

## Folder Structure Summary
- `workspace/Idea.md`: Đặc tả dự án.
- `agy-memory/SESSION_STATE.md`: Quản lý bộ nhớ hiện tại.
- (Dự kiến) `workspace/ACTION_PLAN.md`: Kế hoạch hành động.

## Asset Pointers
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\Idea.md`
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\agy-memory\SESSION_STATE.md`
