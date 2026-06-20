# LÝ LỊCH TRẬN ĐÁNH (PROJECT SPECIFICATION) - EV FORECAST REPORT

## 1. Objective & Success Criteria
- **Mục tiêu kép:** 
  1. Xây dựng báo cáo khoa học trình bày mô hình dự báo tỷ lệ sử dụng trạm sạc xe điện (EV utilization rate) từ tập dữ liệu `EV-pro1_forcast.csv`.
  2. **Bảo vệ đồ án (Final Exam Defense):** Cung cấp tài liệu giải thích chuyên sâu (Deep-dive Q&A) để Tư lệnh nắm vững lý thuyết, quyết định thiết kế mô hình, custom loss, và kết quả phân tích nhằm bảo vệ thành công trước hội đồng.
- **Tiêu chí thành công:**
  - Tiền xử lý dữ liệu: Resample dữ liệu về chu kỳ 1 giờ (1-hour time step).
  - Khung dự báo: Dự báo đa bước cho 24 giờ tiếp theo (t+24 hours).
  - Thuật toán cốt lõi: Triển khai và so sánh toàn diện 4 mô hình: Random Forest, LSTM, LightGBM (LGBM), XGBoost.
  - Tối ưu hóa: Triển khai **Custom Loss Function** để phạt nặng các sai số tại vùng đỉnh (peak fluctuation) trong quá trình huấn luyện và hyper-tuning.
  - Đầu ra báo cáo: Báo cáo LaTeX chuẩn 4 phần (Introduction, Material and Method, Results and Discussion, Conclusion).

## 2. Assumptions (Giả định)
- Dữ liệu `EV-pro1_forcast.csv` có chất lượng đủ tốt, các trường dữ liệu thời tiết, sự kiện có thể được sử dụng làm features bổ sung.
- Biến mục tiêu dự báo chính xác là `utilization_rate`.
- Dữ liệu sẽ được resample 1 giờ trực tiếp trên `EV-pro1_forcast.csv` và chia lại Train/Val/Test (hoặc sử dụng các file cắt sẵn nếu tương thích cấu trúc thời gian).
- Mẫu báo cáo LaTeX mặc định sử dụng định dạng bài báo khoa học chuẩn (e.g. IEEEtran).

## 3. Tech Stack & Structure
- **Ngôn ngữ & Phân tích:** Python 3, Pandas, NumPy.
- **Machine Learning/Deep Learning:** Scikit-learn (Random Forest), TensorFlow/PyTorch (LSTM), LightGBM, XGBoost.
- **Tối ưu hóa (Hyper-tuning):** Optuna.
- **Soạn thảo văn bản:** LaTeX.
- **Cấu trúc Không gian mạng (Workspace):**
  - `code/main.py`: Luồng thực thi chính (Main workflow).
  - `code/core_functions.py`: Chứa các hàm xử lý chính (Load data, resample, train models, custom loss).
  - `code/utils.py`: Chứa các hàm phụ trợ, vẽ biểu đồ, tính metrics.
  - `workspace/report/`: Chứa mã nguồn LaTeX và figures cho báo cáo.
  - `workspace/defense_qa.md`: Bộ câu hỏi/đáp án và giải thích chuyên sâu phục vụ bảo vệ đồ án.

## 4. Boundaries (Giới hạn & Quy tắc tác chiến)
- **ALWAYS DO:** Viết code theo hướng Procedure/Functional (hàm đơn giản, dễ hiểu), TUYỆT ĐỐI KHÔNG DÙNG CẤU TRÚC OOP (Class/Object). Đảm bảo custom loss thực sự cải thiện khả năng bắt đỉnh so với Baseline. Các biểu đồ kết quả phải trực quan hóa được khả năng dự báo tại các điểm Peak. Chuẩn bị giải thích cặn kẽ tại sao lại chọn các tham số này.
- **ASK FIRST:** Phải báo cáo Tư lệnh nếu thuật toán Deep Learning (LSTM) tiêu tốn quá mức tài nguyên phần cứng hoặc thời gian huấn luyện. Xin ý kiến nếu cần thay đổi template LaTeX.
- **FORBIDDEN:** Tuyệt đối không thay đổi cấu trúc 4 phần của báo cáo đã được Tư lệnh thiết kế trong sơ đồ `requimentinreport.png`. Không tự ý thay đổi số bước dự báo t+24.

## 5. Advanced Feature Engineering Extension (Comparison Cases for Defense Q&A)
Trong quá trình thiết kế đặc trưng (Feature Engineering), hội đồng có thể chất vấn về việc mở rộng biến Lag/Rolling Window cho các dữ liệu ngoại lai (Exogenous variables). Dưới đây là phương án phòng thủ & mở rộng:
- **Nguyên lý gốc:** Chỉ áp dụng Lag (1, 2, 24) và Rolling Window (3h, 6h) cho biến mục tiêu `utilization_rate` để tối ưu hóa sức mạnh nội tại (Target is King), giảm thiểu bùng nổ chiều dữ liệu (Curse of Dimensionality) và chống Overfitting.
- **Tình huống mở rộng (Extension Cases):** Nếu cần đưa thêm dữ liệu ngoại lai vào để so sánh, mô hình sẽ CHỈ ưu tiên chọn 2 biến sau:
  1. **`traffic_congestion_index` (Chỉ số kẹt xe):** Áp dụng `Rolling 3h` để đo lường "Độ tích lũy kẹt xe/Cạn pin" của EV trên đường, dự báo làn sóng sạc đột biến sau khi thông xe.
- Tất cả các biến khác (thời gian, sự kiện, thời tiết) đều bị loại khỏi danh sách làm Lag/Window do tính quy luật tĩnh hoặc thay đổi quá chậm, nếu đưa vào chỉ gây nhiễu loạn (Noise).

## 6. Lịch sử Thử nghiệm (Experiment Logs & Failures)
Trong khoa học dữ liệu, việc chứng minh một phương pháp thất bại cũng có giá trị ngang với một phương pháp thành công. 
- **Thất bại của SMOGN (Synthetic Minority Over-sampling Technique for Regression):**
  - **Kỳ vọng:** Dùng thuật toán k-NN để nội suy và nhân bản các điểm Peak.
  - **Thực tế:** Thất bại do nội suy làm vỡ cấu trúc biến Categorical/Ordinal (VD: `hour_of_day = 8.5`). Gây tẩu hỏa nhập ma cho mô hình trên tập Test (Garbage In, Garbage Out).
  - **Quyết định:** Loại bỏ SMOGN để bảo vệ độ tinh khiết của Không gian Đặc trưng (Feature Space).

- **Giải pháp Tối thượng: Target Power Transformation (TPT) kết hợp Custom Loss**
  - **Nguyên lý Toán học:** Thay vì bóp méo Đầu vào (X), ta bóp méo Đầu ra (Y) bằng phép Lũy thừa bậc 3 ($y^3$). Vùng đáy (0.2) sẽ bị nén lại ($0.2^3 = 0.008$), trong khi vùng Đỉnh (0.9) vẫn giữ khoảng cách rất lớn ($0.9^3 = 0.729$).
  - **Hiệu ứng Kép (Double-Nuke):** Khoảng cách vật lý ở vùng đỉnh bị kéo giãn ra gấp nhiều lần. Kết hợp với hàm `custom_peak_weighted_mse` (Ngưỡng kích hoạt dời từ 0.7 thành $0.7^3 = 0.343$, phạt 50x). Bản năng sinh tồn của thuật toán sẽ dồn 100% lực lượng vào việc khớp các chóp đỉnh bị phóng to này.
  - **Tính tương thích:** Áp dụng hoàn hảo cho CẢ 4 MÔ HÌNH (RF, LGBM, XGBoost, LSTM) mà không cần can thiệp cấu trúc lõi. Chỉ cần Căn bậc 3 ($y^{1/3}$) kết quả dự báo để trả về tỷ lệ %.

## 7. Kiến trúc Data Assimilation (Predictor-Corrector) - Tối thượng
Hệ thống chốt hạ giải quyết triệt để "Bướu Lạc Đà" (Camel Peak) dựa trên sự kết hợp giữa 2 lớp mô hình độc lập:
1. **Lớp Base 24h (Predictor - Khung định hướng):**
   - Sử dụng kiến trúc **Rule-Based Two-Stage Model**.
   - Dùng Base Model làm Trigger: Nếu Base < 0.55 thì dùng kết quả của Base để theo dõi sát vùng thung lũng (Valleys).
   - Nếu Base >= 0.55 thì chuyển sang dùng TPT Model ($y^3$ + Custom Loss) để bắt trọn các chóp đỉnh (Peaks).
   - *Vai trò:* Cung cấp một bộ khung 24h cực kỳ an toàn, miễn nhiễm hoàn toàn với lỗi cộng dồn (Error Propagation).
2. **Lớp Corrector 1h (Hiệu chỉnh vi mô):**
   - Xây dựng một mô hình dự báo cực ngắn (Horizon = 1h) mang tính cuốn chiếu (Recursive). 
   - *Trạng thái hiện tại:* Đã áp dụng Optuna tuning thành công. **XGBoost Tuned (RMSE ~ 0.0668)** trở thành SOTA cho lớp Corrector, đánh bại mọi cấu hình cơ bản trước đó.
   - *Vai trò:* Sở hữu sai số cực thấp, mô hình này được dùng làm công cụ "nắn" lại các nếp gấp vi mô bị hụt của mô hình 24h (Đặc biệt là các đỉnh đôi của bướu lạc đà) nhằm đẩy hệ thống đạt SOTA (State-of-the-Art).
3. **Vũ khí Phản biện (Dành cho Q&A):**
   - Sự thất bại của **1D-CNN** khẳng định: Tabular Models (XGBoost) là bá chủ tuyệt đối trên dữ liệu nhỏ (Small Data).
   - Sự sụp đổ của **DirRec (24 Models)** chứng minh: Việc thiết lập Khung định hướng 24h là yêu cầu sống còn. Việc mù quáng nối tiếp sai số mà không có "Neo 24h" sẽ hủy diệt mô hình.
