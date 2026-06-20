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
- **Pivot/Cập nhật:** Cấu trúc code chuyển sang Functional/Procedure (TUYỆT ĐỐI KHÔNG DÙNG OOP).
- Hoàn thành **Task 1.5 & Task 2 & Task 3**: Tích hợp Lag/Rolling Window, Custom Loss (phạt 50x tại peak >= 0.7) và tuning 4 mô hình (RF, LGBM, XGBoost, LSTM).
- Hoàn thành **Task 4 (Đánh giá Base)**: Xuất 8 biểu đồ Base để tạo baseline.
- **Pivot/Cập nhật (Task 4.1 & 4.2)**: Thử nghiệm thuật toán SMOGN (Synthetic Minority Over-sampling) để nhân bản vùng đỉnh. Tuy nhiên, SMOGN nội suy tuyến tính làm hỏng các biến Categorical/Ordinal (`hour_of_day`, `is_weekend`) gây nhiễu loạn mô hình (Bẫy nội suy dữ liệu tĩnh). **Kết quả: TỪ CHỐI SMOGN.**
- **Kiến trúc mới (Task 4.3)**: Sáng tạo ra cấm thuật **Target Power Transformation (TPT)**. Lũy thừa bậc 3 biến mục tiêu ($y^3$) để bóp méo khoảng cách vùng đỉnh kết hợp với Custom Loss (ngưỡng mới $0.343$). Điều này ép cả 4 mô hình lao lên bắt đỉnh mà không làm hỏng Feature Space.

## Key Decisions
- Biến mục tiêu: `utilization_rate`.
- Phương pháp luận bắt đỉnh: Custom Loss + Target Power Transformation (Double-Nuke Strategy).
- Quyết định loại bỏ SMOGN để bảo vệ Không gian Đặc trưng.
- Output: LaTeX Report + Defense Q&A Documentation.

## Next Steps
- Đánh giá 8 biểu đồ TPT của Task 4.3 để xem độ bám đỉnh.
- Bắt đầu **Task 5 (Viết Báo cáo Khoa học bằng LaTeX)**.

## Critical Context
- Lịch sử thử nghiệm SMOGN thất bại là một "Mỏ vàng" cho phiên phản biện để chứng minh tư duy phản biện (Critical Thinking).

## Folder Structure Summary
- `workspace/Idea.md`: Đặc tả dự án và Lịch sử Thử nghiệm.
- `agy-memory/SESSION_STATE.md`: Quản lý bộ nhớ hiện tại.
- `workspace/ACTION_PLAN.md`: Kế hoạch hành động.
- `workspace/figures/`: Thư mục chứa các biểu đồ xuất ra (Base, SMOGN, TPT).

## Asset Pointers
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\Idea.md`
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\agy-memory\SESSION_STATE.md`
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\ACTION_PLAN.md`
