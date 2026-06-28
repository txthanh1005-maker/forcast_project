# IDEA & STATIC SPEC: Chiến dịch Case-Study-Driven Revision

## 1. Objective & Success Criteria
- **Objective:** Đổi trọng tâm báo cáo sang "Case-Study-Driven", chỉ tập trung huấn luyện và phân tích duy nhất trên dữ liệu Trạm EV 00015 (đã được cô lập). Chứng minh định lượng việc chọn Lag và Feature Selection bằng các biểu đồ minh bạch.
- **Success Criteria:** 
  - Đưa ra được biểu đồ ACF/PACF và biểu đồ/bảng so sánh hiệu suất khi thay đổi Lag (dùng Base Model, không dùng kỹ thuật tối ưu).
  - Đưa ra được biểu đồ SHAP / Feature Importance cho các đặc trưng để chứng minh độ quan trọng.
  - Sửa báo cáo LaTeX bám theo kết quả của trạm 00015.

## 2. Assumptions
- Dữ liệu `EV_train.csv`, `EV_test.csv`, `EV_val.csv` đang có sẵn trong thư mục chính là dữ liệu ĐÃ LỌC riêng cho trạm EV 00015. Không cần tiền xử lý thêm phần lọc trạm.
- Mô hình chạy kiểm thử Lag và Feature Importance là mô hình LGBM thuần (Base Model), hoàn toàn KHÔNG áp dụng các kỹ thuật nâng cao (như custom loss, SMOGN, hay ensemble) nhằm giữ tính khách quan tuyệt đối cho baseline.

## 3. Tech Stack & Structure
- **Tools:** Python (Pandas, Statsmodels, LightGBM, SHAP, Matplotlib).
- **Target Files:**
  - `code/lag_evaluation.py`
  - `code/feature_selection_analysis.py`
  - `Latex_report/sn-article.tex`

## 4. Boundaries
- **ALWAYS DO:** Dùng LightGBM mặc định. Trả về kết quả đầu ra bằng file biểu đồ (.png/.pdf).
- **ASK FIRST:** Thay đổi bất kỳ thông số siêu tham số (hyperparameter) nào, vì Tư lệnh đã yêu cầu chỉ dùng model thuần.
- **FORBIDDEN:** KHÔNG code kỹ thuật lọc dữ liệu các trạm khác nữa vì data đã sẵn sàng. KHÔNG thêm kỹ thuật tối ưu hóa vào bước đánh giá Feature/Lag.
