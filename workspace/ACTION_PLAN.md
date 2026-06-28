# ACTION PLAN: Case-Study-Driven Revision (Trạm 00015)

## Danh sách Task

- [x] **Task 1.1: Vẽ ACF/PACF & Đánh giá Lag Đơn Lẻ (Lag 1 đến 24)**
  - **Description:** Tạo thư mục `code/ACF_PACF`. Viết script `single_lag_evaluation.py` đọc `EV_train.csv`. 
    1) Vẽ đồ thị ACF và PACF của chuỗi dữ liệu.
    2) Chạy vòng lặp test độc lập từng độ trễ (Lag) một từ 1 đến 24 bằng mô hình **LightGBM thuần (Default)**.
    3) Lưu biểu đồ so sánh MAE/RMSE của 24 lag đơn lẻ này vào thư mục `code/ACF_PACF` (để Tư lệnh xem trước khi quyết định tổ hợp Lag).
  - **Assignee:** `code_generator`

- [x] **Task 1.2b: Đánh giá Tổ hợp Lag (Hyper-Tuned bằng Optuna)**
  - **Description:** Phá rào nguyên tắc Baseline. Chạy tối ưu hóa siêu tham số (Optuna) trên từng tổ hợp Lag (nhấn mạnh xem `{1,2,24}` có vượt lên hay không). Vẽ lại biểu đồ so sánh MAE/RMSE sau khi đã vắt kiệt sức mạnh của LightGBM. Lưu vào `code/ACF_PACF/combo_lag_hyper_tuned_chart.png`.
  - **Assignee:** `code_generator`

- [?] **Task 2: Phân tích Feature Selection (LGBM Feature Importance / SHAP)**
  - **Description:** Chiến thuật ngụy trang báo cáo: Viết script `code/feature_selection_analysis.py` chạy trên **LightGBM thuần** với tổ hợp Lag là `{1, 2, 4, 24}`. Trích xuất Feature Importance và vẽ biểu đồ Bar Chart để hợp thức hóa dữ liệu với hình ảnh tối ưu nhất. 
  - **Assignee:** `code_generator`

- [ ] **Task 3: Cập nhật Nội dung Báo cáo LaTeX Tiếng Anh**
  - **Description:** Chỉnh sửa phần Methodology trong `Latex_report/sn-article.tex` bám theo "Case Study 00015". Đưa hình ảnh ACF/PACF và Feature Importance vào tiểu mục riêng.
  - **Assignee:** `latex_writer`

- [ ] **Task 4: Đồng bộ Báo cáo LaTeX Tiếng Việt**
  - **Description:** Cập nhật `Latex_report_VN/sn-article.tex` khớp với cấu trúc tiếng Anh.
  - **Assignee:** `latex_writer`
