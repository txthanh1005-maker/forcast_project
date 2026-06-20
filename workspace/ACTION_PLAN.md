# Implementation Plan: EV Forecast Report & Defense Q&A

## Overview
Xây dựng một hệ thống phân tích, dự báo và so sánh các mô hình (RF, LSTM, LGBM, XGBoost) trên tập dữ liệu trạm sạc xe điện nhằm bắt chính xác các peak fluctuation bằng custom loss function. Cuối cùng, tổng hợp thành một báo cáo khoa học (LaTeX) và một tài liệu Q&A chuyên sâu phục vụ bảo vệ đồ án.

## Architecture Decisions
- **Data Pipeline:** Đọc từ `EV-pro1_forcast.csv`, resample 30 phút thành 1 giờ. Biến mục tiêu là `utilization_rate`. Dự báo 24 bước thời gian (t+24).
- **Custom Loss:** Do đặc thù yêu cầu bắt đỉnh, hàm mất mát sẽ phạt sai số lớn hơn đối với các giá trị `utilization_rate` cao (ví dụ: Weighted MSE).
- **Reporting:** Mọi kết quả, biểu đồ sẽ được đẩy vào thư mục `workspace/report/` để phân đội Văn thư (latex_writer) chèn vào file `.tex`.
- **Defense Q&A:** Phân đội Chuyên gia (general_expert/domain_reviewer) sẽ song hành giải thích các quyết định trong code và tổng hợp vào `workspace/defense_qa.md`.

## Task List

### Phase 1: Foundation (Data & Theory)
- [x] **Task 1: Xử lý dữ liệu & Resampling** (DONE)
  - **Description:** Xây dựng code cơ sở theo kiến trúc 3 file (main.py, core_functions.py, utils.py). Định nghĩa các hàm đọc dữ liệu, resample 1 hour, xử lý missing data trong `core_functions.py` và `utils.py`, sau đó gọi thực thi tại `main.py`. TUYỆT ĐỐI KHÔNG DÙNG OOP.
  - **Assigned:** `code_generator`
  - **Reviewer:** `test-engineer`
  - **Acceptance criteria:**
    - [x] Dữ liệu đầu ra là chu kỳ 1 giờ chuẩn xác.
    - [x] Tập dữ liệu được chia Train/Val/Test hợp lý, sẵn sàng đưa vào mô hình.
- [x] **Task 1.5: Feature Engineering (Lag & Rolling Window)** (DONE)
  - **Description:** Bổ sung Lag features (t-1, t-2, t-24) và Rolling Mean (3h, 6h) để bắt dao động zíc-zắc.
  - **Assigned:** `code_generator`
- [x] **Task 2: Thiết kế Custom Loss Function** (DONE)
  - **Description:** Triển khai hàm mất mát phạt nặng vùng Peak Fluctuation.
  - **Assigned:** `code_generator`
  - **Reviewer:** `domain_reviewer`
  - **Acceptance criteria:**
    - [x] Loss function tích hợp được với ít nhất 3/4 thuật toán.
    - [x] Có script kiểm thử chứng minh việc dùng loss function này nhạy hơn với các peak.

### Checkpoint: Foundation
- [x] Dữ liệu sẵn sàng.
- [x] Custom Loss đã qua kiểm duyệt chuyên ngành.

### Phase 2: Modeling & Evaluation
- [x] **Task 3: Huấn luyện và Hyper-tuning (RF, LSTM, LGBM, XGBoost)** (DONE)
  - **Description:** Chạy các mô hình dự báo t+24. Sử dụng Optuna để tuning siêu tham số.
  - **Assigned:** `code_generator`
  - **Reviewer:** `test-engineer`
  - **Acceptance criteria:**
    - [ ] Các mô hình chạy thành công và xuất ra predictions.
    - [ ] Ghi nhận log của Optuna.

- [x] **Task 4: Trích xuất Biểu đồ Base (Trước SMOGN)** (DONE)
  - **Description:** Xuất tổng cộng 8 hình (7 hình riêng rẽ cho 7 ngày, mỗi ngày 24h và 1 hình tổng nối 7 ngày) cho tình trạng Base (Lag/Window + Custom Loss).
  - **Assigned:** `code_generator`

- [x] **Task 4.1: Áp dụng kỹ thuật SMOGN (Synthetic Data)** (DONE)
  - **Description:** Implement SMOGN để oversample các vùng peak trên tập Train (>= 0.7). Train lại mô hình Tabular (XGBoost, LightGBM) với SMOGN + Custom Loss. Save models. Evaluated on original test set.
  - **Assigned:** `code_generator`

- [x] **Task 4.2: Trích xuất Biểu đồ Base & SMOGN và So sánh** (DONE)
  - **Description:** Cập nhật `evaluate.py` xuất 8 hình (7 ngày liên tục và 7 ngày riêng) cho cả model Base và model SMOGN.
  - **Assigned:** `code_generator`

- [ ] **Task 4.3: Triển khai cấm thuật Target Power Transformation (TPT)** (TODO)
  - **Description:** Lũy thừa bậc 3 target ($y^3$) trước khi train. Sửa Custom Loss threshold thành $0.7^3 = 0.343$. Căn bậc 3 ($y^{1/3}$) kết quả predict. Xuất 8 biểu đồ TPT.
  - **Assigned:** `code_generator`

### Checkpoint: Core Features
- [ ] Tất cả biểu đồ và số liệu đã sẵn sàng cho báo cáo.

### Phase 3: Documentation & Q&A
- [ ] **Task 5: Soạn thảo Báo cáo LaTeX**
  - **Description:** Viết file `.tex` chuẩn 4 phần theo Mind Map của Tư lệnh.
  - **Assigned:** `latex_writer`
  - **Reviewer:** `english_teacher` & `domain_reviewer`
  - **Acceptance criteria:**
    - [ ] File PDF biên dịch thành công.
    - [ ] Nội dung đầy đủ 4 phần (Intro, Material & Method, Results & Discussion, Conclusion).

- [ ] **Task 6: Viết tài liệu Defense Q&A**
  - **Description:** Tổng hợp các câu hỏi bảo vệ đồ án: Tại sao chọn Custom Loss? Tại sao resample 1 giờ? So sánh LSTM vs XGBoost ở điểm nào?
  - **Assigned:** `general_expert`
  - **Reviewer:** `domain_reviewer`
  - **Acceptance criteria:**
    - [ ] Hoàn thành file `workspace/defense_qa.md`.
    - [ ] Bao quát ít nhất 10 câu hỏi phòng thủ hóc búa nhất.

### Checkpoint: Complete
- [ ] Tất cả acceptance criteria met.
- [ ] Ready for review by Tư lệnh.
