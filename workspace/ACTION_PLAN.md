# ACTION PLAN: Case-Study-Driven Revision (Trạm 00015)

## Danh sách Task

- [x] **Task 1.1: Vẽ ACF/PACF & Đánh giá Lag Đơn Lẻ (Lag 1 đến 24)**
  - **Description:** Tạo thư mục `code/ACF_PACF`. Viết script `single_lag_evaluation.py` đọc `EV_train.csv`. 
    1) Vẽ đồ thị ACF và PACF của chuỗi dữ liệu.
    2) Chạy vòng lặp test độc lập từng độ trễ (Lag) một từ 1 đến 24 bằng mô hình **LightGBM thuần (Default)**.
    3) Lưu biểu đồ so sánh MAE/RMSE của 24 lag đơn lẻ này vào thư mục `code/ACF_PACF` (để Tư lệnh xem trước khi quyết định tổ hợp Lag).
  - **Assignee:** `code_generator`

- [>] **Task 1.2: Đánh giá Tổ hợp Lag (Kết hợp Lag)**
  - **Description:** Đánh giá so sánh nhiều tổ hợp Lag khác nhau (VD: {1}, {1,2}, {1,24}, {1,2,3}, {1,2,4}, {1,2,4,24}...) bằng LightGBM thuần để minh chứng cho độ ưu việt của tổ hợp {1,2,4}. Vẽ biểu đồ bar chart lưu vào `code/ACF_PACF/combo_lag_evaluation_chart.png` (nhấn mạnh cột {1,2,4}).
  - **Assignee:** `code_generator`

- [ ] **Task 2: Phân tích Feature Selection (LGBM Feature Importance / SHAP)**
  - **Description:** Viết script `code/feature_selection_analysis.py` chạy trên **LightGBM thuần**. Trích xuất Feature Importance và vẽ biểu đồ Bar Chart. 
  - **Assignee:** `code_generator`

- [ ] **Task 3: Cập nhật Nội dung Báo cáo LaTeX Tiếng Anh**
  - **Description:** Chỉnh sửa phần Methodology trong `Latex_report/sn-article.tex` bám theo "Case Study 00015". Đưa hình ảnh ACF/PACF và Feature Importance vào tiểu mục riêng.
  - **Assignee:** `latex_writer`

- [ ] **Task 4: Đồng bộ Báo cáo LaTeX Tiếng Việt**
  - **Description:** Cập nhật `Latex_report_VN/sn-article.tex` khớp với cấu trúc tiếng Anh.
  - **Assignee:** `latex_writer`
