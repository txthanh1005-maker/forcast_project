# CẤU TRÚC LOGIC BÁO CÁO KHOA HỌC (IEEE/ELSEVIER FORMAT)

Báo cáo khoa học đòi hỏi sự tách biệt nghiêm ngặt: **Methodology** chỉ nói về Toán học, Thiết kế kiến trúc và Lý do (Tại sao chọn kỹ thuật này); trong khi **Results & Discussion** mới là nơi tung ra các con số (RMSE) và biểu đồ để chứng minh thiết kế đó là đúng. 

Dưới đây là phương án "tách đôi" câu chuyện nhân quả của chúng ta để lắp vừa vặn vào khung 4 phần chuẩn mực:

---

## 1. INTRODUCTION (Mở đầu)
- **Bối cảnh & Vấn đề (The Problem):** Dự báo tỷ lệ sử dụng trạm sạc EV (EV utilization rate) đối mặt với hai thách thức cốt lõi: Tập dữ liệu nhỏ (Small Data) và đặc trưng "Bướu Lạc Đà" (Camel Peak) - nơi nhu cầu sạc biến động đột ngột, cực đoan và phi tuyến tính.
- **Hạn chế của nghiên cứu trước (The Gap):** Các mô hình hồi quy truyền thống (như MSE) luôn có xu hướng cào bằng sai số, dẫn đến hụt dự báo ở chóp đỉnh. Các nỗ lực can thiệp dữ liệu (như SMOGN) lại phá nát cấu trúc biến phân loại. Việc dùng mô hình Phân loại (Classifier) để gạt trạng thái lại làm phình to hệ thống (System Bloat). Cuối cùng, các mô hình với tầm nhìn vĩ mô (24h) luôn bỏ lỡ cực trị vi mô, trong khi mô hình vi mô (1h) lại mắc kẹt trong hiệu ứng Trễ pha (Phase Lag).
- **Literature Review & Related Works (Được định hướng bởi triết lý MPC):** *(Chiến dịch nghiên cứu tài liệu độc lập được lưu trữ tại `Idea_Lit.md` và `ACTION_PLAN_Lit.md`)*
  - Quét 5 trục học thuật cốt lõi để bảo vệ siêu kiến trúc: (1) Căn bệnh Small Data của Deep Learning; (2) Phương pháp can thiệp bắt đỉnh (Peak Catching); (3) Sự tinh gọn của Two-Stage Rule-Based; (4) Giải mã chu kỳ bằng Residual Learning; (5) **Triết lý Model Predictive Control (MPC)** kết hợp Cascade để triệt tiêu Phase Lag.
- **Đóng góp của nghiên cứu (Our Contributions):** Đề xuất kiến trúc **Proxy-Lag Cascade Ensemble** hoàn toàn mới. Hệ thống là sự kết hợp tinh xảo giữa (1) Kiến trúc "Công tắc" (Two-Stage Rule-Based) tích hợp Custom Loss và Target Power Transformation ($y^3$) để bắt chóp đỉnh mà không cần Classifier; và (2) Lớp hiệu chỉnh vi mô 1h (Residual Corrector) được dẫn đường bởi bản đồ vĩ mô 24h (Proxy Feature). Kiến trúc này giải quyết triệt để bài toán dự báo mà vẫn duy trì sự tinh gọn tuyệt đối.

## 2. MATERIAL & METHODOLOGY (Phương pháp nghiên cứu - Kể chuyện Bằng Tư duy Thiết kế)
*Phần này tuyệt đối KHÔNG đưa kết quả RMSE vào. Chỉ tập trung giải thích "Tại sao thiết kế như vậy" dựa trên đặc trưng dữ liệu.*

- **2.1. Kỹ thuật Tiền xử lý & Thiết kế Đặc trưng (Data Preprocessing & Feature Engineering):**
  - *Làm sạch & Resample:* Xử lý dữ liệu thiếu và Resample về chu kỳ 1 giờ để đồng bộ hóa lưới thời gian.
  - *Lý do thiết kế Đặc trưng Nền tảng:* 
    - Chọn **Lag 1, 2** để thâu tóm quán tính ngắn hạn (momentum) của nhu cầu sạc. 
    - Chọn **Lag 24** để "chốt chặt" chu kỳ tuần hoàn ngày (Daily Seasonality) vì thói quen sạc thường lặp lại sau mỗi 24h. 
    - Chọn **Rolling Window 3h, 6h** nhằm làm mịn nhiễu cục bộ (noise smoothing) và nắm bắt làn sóng tích lũy nhu cầu sạc trong suốt một buổi.
  - *Chiến lược Chia tập dữ liệu & Chuẩn hóa:* 
    - Chia 3 tập **Train/Validation/Test**: Tập Train dùng để học; tập Test dùng làm bài thi cuối cùng; tập **Validation** đóng vai trò cực kỳ quan trọng làm "thao trường" để Optuna Tuning dò siêu tham số và là nơi chốt Tỷ lệ Vàng Ensemble (33% - 67%) nhằm đảm bảo tính khách quan tuyệt đối.
    - Áp dụng **Chuẩn hóa (Normalization)** để đồng nhất không gian tỷ lệ (scale). Việc này vừa ngăn các biến có giá trị lớn chèn ép biến nhỏ, vừa tạo sự ổn định tuyệt đối để Custom Loss Function có thể định vị và phạt đúng "tọa độ" đỉnh.
- **2.2. Phân tích Đặc trưng Dữ liệu & Lựa chọn Thuật toán:**
  - Chỉ ra bản chất dữ liệu: Kích thước nhỏ (Small Data) và có chứa các biến động cực đoan (Camel Peak).
  - Lập luận lý thuyết: Tại sao các thuật toán Tabular (XGBoost, LGBM) được chọn làm nòng cốt thay vì Deep Learning (1D-CNN/LSTM).
  - *Đoạn dẫn chuyển tiếp (Sự thiếu hụt của Base Model):* Lập luận chỉ ra rằng dù XGBoost rất mạnh, nhưng hàm mục tiêu mặc định (như MSE) luôn có bản chất "cào bằng" (mean-seeking). Hệ quả là mô hình luôn bất lực, dự báo thấp hơn thực tế ở các chóp đỉnh (under-forecasting peaks). Sự giới hạn này đặt ra yêu cầu bức thiết phải can thiệp sâu bằng Toán học để ép mô hình bắt đỉnh.
- **2.3. Toán học của việc Bắt Đỉnh (Từ Thất bại SMOGN đến Custom Loss & TPT):**
  - *Bác bỏ nỗ lực can thiệp Đầu vào (Thất bại của SMOGN):* Lập luận lý do SMOGN làm vỡ nát biến phân loại. Rút ra nguyên lý: **Không bóp méo Đầu vào (X), mà can thiệp Đầu ra (Y) và Loss Function**.
  - Trình bày công thức Custom Peak Loss (Trọng số x50) để định hướng Gradient.
  - Trình bày công thức Target Power Transformation ($y^3$). Phân tích trên lý thuyết việc hàm bậc 3 khuếch đại đỉnh.
  - *Đoạn dẫn chuyển tiếp (Ưu và Nhược điểm của TPT):* Mặc dù TPT giúp mô hình lao lên bắt đỉnh cực kỳ bạo liệt (ưu điểm), nhưng chính sự nén giá trị lại gây thảm họa sai số ở vùng thung lũng (nhược điểm). Sự đánh đổi cực đoan này báo hiệu rằng một mô hình đơn lẻ không thể gánh cả đỉnh lẫn đáy, đặt ra yêu cầu bắt buộc phải tách đôi kiến trúc để trị từng phần.
- **2.4. Khắc phục Thung lũng: Kiến trúc "Công tắc" Two-Stage Rule-Based:**
  - *Sự tinh gọn (Occam's Razor) so với Lớp Phân loại (Classifier):* Nhắc đến việc từng triển khai thành công một mô hình Classifier độc lập để dự báo "Khi nào có đỉnh?". Dù Classifier cho kết quả nhận diện đỉnh rất tốt, nhưng việc phải huấn luyện và duy trì thêm một model thứ ba chỉ để làm nhiệm vụ "gạt công tắc" khiến hệ thống trở nên cồng kềnh, phức tạp và tốn kém tài nguyên vận hành không cần thiết.
  - *Cơ sở của Rule-Based Trigger & Giải mã Ngưỡng 0.55:* Từ bài toán tối ưu kiến trúc, chốt hạ triết lý tinh gọn: Dùng trực tiếp dự báo của Base Model làm "Công tắc" (Rule-Based). **Lập luận tại sao lại là 0.55:** Dựa trên phân tích phân phối dữ liệu thực tế, 0.55 (55% công suất) là "điểm uốn" (inflection point) vật lý của hệ thống. Dưới 0.55 là trạng thái vận hành ổn định, tuyến tính. Từ 0.55 trở lên, trạm sạc chính thức bước vào trạng thái quá tải cực đoan.
  - *Cấu hình Toán học của Hệ thống (Operational Formulation):* Trình bày công thức chốt hạ ghép nối 2 mô hình (Đầu ra cuối cùng $\hat{y}_{final}$): Nếu $\hat{y}_{base} < 0.55$, hệ thống xuất ra $\hat{y}_{base}$ để bảo vệ thung lũng một cách êm ái. Nếu $\hat{y}_{base} \ge 0.55$, hệ thống tự động gạt sang $\hat{y}_{TPT}$ để vợt chóp đỉnh. Sự kết hợp toán học (Piecewise Function) này tạo ra một mô hình lai hoàn hảo, vừa có độ nhạy của TPT vừa có tính ổn định của Base.
  - *Đoạn dẫn chuyển tiếp (Thành quả & Giới hạn 24h):* Dù Two-Stage đã xuất sắc giải quyết vẹn toàn Đỉnh và Đáy, nhưng hệ thống vẫn "hụt hơi" ở các đỉnh thứ 2 (cực trị phụ). Nguyên nhân do điểm mù vật lý của Tầm nhìn: Dự báo một lúc 24 giờ (Horizon = 24h) khiến mô hình mất đi độ phân giải vi mô. Điều này ép buộc hệ thống phải tiến hóa thêm một tầng kiến trúc.
- **2.5. Tư duy Bù đắp: Kiến trúc Lớp 24h & Giới hạn Cực trị:**
  - Phân tích chi tiết toán học của điểm mù Tầm nhìn 24h.
  - Đề xuất bổ sung Lớp Corrector (t+1) để bù đắp điểm mù này.
- **2.6. Khảo sát Xây dựng Lớp Corrector 1h (Từ bác bỏ sai lầm đến giải pháp Tối ưu):**
  - *Cuộc vật lộn thiết kế & Bác bỏ các phương pháp Thất bại:* Liệt kê chuỗi thử nghiệm đẫm máu khi cố gắng giải quyết lỗi Trễ Pha (Phase Lag) đặc trưng của dự báo 1h:
    - (1) *Bê nguyên TPT và Custom Loss sang 1h:* Thất bại do các dao động vi mô 1h quá nhiễu, làm sai lệch hàm phạt.
    - (2) *Sử dụng Đặc trưng Động học (Kinematic Features):* Thử dùng các công thức Vận tốc, Gia tốc để đoán gia số nhưng không bẻ gãy được quán tính trễ pha.
    - (3) *Áp dụng DTW Loss (Dynamic Time Warping):* Thất bại về mặt nền tảng Toán học do DTW đánh giá theo chuỗi (sequence-level), hoàn toàn không tương thích với bộ tối ưu Gradient điểm (pointwise) của thuật toán Tree-based (XGBoost).
  - *Sự đột phá của Kiến trúc Residual Boosting (The Gold Standard):* Trình bày phương pháp cực mạnh: Bóc tách chu kỳ bằng Seasonal Baseline, ép mô hình 1h chỉ tập trung dự báo "Phần dư" (Residual).
  - *Giải pháp chốt hạ (Proxy-Lag Cascade):* Đề xuất việc dùng dự báo 24h làm Đặc trưng Dẫn đường (Proxy Feature) bơm trực tiếp vào mô hình 1h. Điều này cung cấp cho Lớp 1h một "tấm bản đồ vĩ mô", giúp mô hình vi mô không bị mất phương hướng, biến toàn bộ hệ thống thành một thác đổ (Cascade) đồng bộ.

## 3. RESULTS & DISCUSSION (Kết quả & Bàn luận - Bằng chứng Thực nghiệm)
*Phần này tuyệt đối tuân thủ triết lý: Mỗi lập luận lý thuyết trong Methodology đều phải được chứng minh bằng biểu đồ/chỉ số (RMSE) tương ứng tại đây.*

- **3.1. Xác thực sự ưu việt của Tabular Models (Chứng minh cho Mục 2.2):** 
  - Trình bày Bảng so sánh RMSE giữa XGBoost/LGBM và Deep Learning (1D-CNN). Khẳng định bằng số liệu rằng Tree-based models vô địch trên địa hạt Small Data.
- **3.2. Hiệu năng của Toán học Bắt Đỉnh & Kiến trúc Two-Stage (Chứng minh cho Mục 2.3 & 2.4):** 
  - *Tác động của TPT:* Trình bày biểu đồ so sánh dự báo Base (hụt đỉnh) và dự báo sau khi áp dụng TPT $y^3$ (bắt chạm đỉnh nhưng phá hỏng đáy).
  - *Sự hoàn hảo của Two-Stage Rule-Based:* Biểu diễn đồ thị khi hàm Piecewise (Ngưỡng 0.55) được kích hoạt. Chứng minh trực quan khả năng "bảo vệ thung lũng, vợt chóp đỉnh" của kiến trúc này mà không cần tốn chi phí vận hành Classifier.
- **3.3. Bẻ gãy Trễ pha bằng Residual & Proxy-Lag (Chứng minh cho Mục 2.5 & 2.6):** 
  - *Nỗi ám ảnh Phase Lag:* Show đồ thị dự báo 1h tiêu chuẩn để lột tả hiện tượng "Trễ Pha" (Dự báo luôn đi sau thực tế 1 bước) bất chấp các thuật toán thông thường.
  - *Đột phá Residual Boosting:* Show biểu đồ khi thuật toán học trên Phần dư (Residual), phá vỡ giới hạn đơn điệu đầu tiên.
  - *Chốt hạ Proxy-Lag Cascade:* Đưa ra đồ thị so sánh trước và sau khi Lớp 1h được bơm "Đặc trưng Dẫn đường" (Proxy 24h). Chứng minh lỗi trễ pha bị tiêu diệt hoàn toàn nhờ sự hợp nhất giữa Tầm nhìn Vĩ mô (24h) và Độ phân giải Vi mô (1h).
- **3.4. Đỉnh cao SOTA & Bàn luận Triển khai (Production-ready):** 
  - Trình bày bảng tổng kết hiệu năng chốt hạ: Kiến trúc Proxy-Lag Cascade Ensemble đạt RMSE kỷ lục (0.0664). 
  - **Bàn luận (Discussion):** Phân tích Tỷ lệ Vàng (33% Base - 67% Corrector) thu được từ tập Validation. Kết luận về tính thực tiễn, sự tinh gọn (Occam's Razor) và tính khả thi khi deploy hệ thống.

## 4. CONCLUSION (Kết luận)
- Tóm tắt lại thành quả: Tạo ra một hệ thống dự báo EV Utilization đa tầng tinh xảo, bắt được đỉnh lạc đà và đạt sai số cực thấp.
- Đề xuất hướng phát triển tương lai (Future Works).
