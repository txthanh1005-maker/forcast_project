# Trường ca Khám phá: Quá trình Tối ưu hóa Mô hình Dự báo Trạm sạc Xe điện (EV)

Tài liệu này ghi nhận toàn bộ quy trình thiết kế, các đợt thử nghiệm thất bại và những điểm nghẽn học thuật (bottleneck) đã được giải quyết trong dự án. Đây là chất liệu cốt lõi để đưa vào phần **Methodology (Phương pháp nghiên cứu)** và **Results & Discussion (Kết quả & Bàn luận)** trong báo cáo LaTeX, đồng thời cung cấp luận điểm sắc bén cho buổi Bảo vệ Đồ án (Defense Q&A).

---

## 1. Giai đoạn 1: Khởi tạo và Thiết lập Nền móng (Baseline)
- **Mục tiêu & Tiền xử lý:** Bài toán đặt ra là dự báo tỷ lệ sử dụng trạm sạc (`utilization_rate`) cho 24 giờ tiếp theo (Horizon = 24h). Dữ liệu được làm sạch và chuẩn hóa (resample) về chu kỳ 1 giờ/bước.
- **Feature Engineering cơ sở:** Thiết kế các đặc trưng chuỗi thời gian tập trung vào biến mục tiêu như độ trễ (Lag 1, 2, 24) và Trung bình trượt (Rolling Window 3h, 6h). Mã nguồn được xây dựng theo chuẩn Procedure/Functional, tuyệt đối tránh OOP để đảm bảo tính tinh gọn.
- **Custom Loss Function:** Quan sát thấy dữ liệu có các đỉnh đột biến (Peak Fluctuation), một hàm Mất mát Tùy chỉnh (Custom Loss) được thiết kế để phạt nặng (gấp 50 lần) các sai số tại vùng giá trị thực tế >= 0.7.
- **Huấn luyện Baseline:** Tiến hành huấn luyện đồng loạt 4 thuật toán: Random Forest, LightGBM, XGBoost, và LSTM kết hợp Custom Loss để tạo mốc cơ sở (Base).

## 2. Giai đoạn 2: Trận đánh "Bắt Đỉnh" (The Camel Peak)
Các mô hình Base thường có xu hướng cào bằng, bỏ qua các chóp đỉnh (Peak) của biến mục tiêu. Việc ép mô hình bắt đỉnh là một thách thức lớn.
- **Thất bại của SMOGN (Oversampling):** Thử nghiệm dùng thuật toán k-NN (SMOGN) để nội suy và nhân bản các điểm ở vùng đỉnh. **Kết cục:** Thất bại thảm hại. Quá trình nội suy làm phá vỡ cấu trúc của các biến phân loại (Categorical/Ordinal) – ví dụ: *giờ trong ngày 8.0 biến thành 8.5*, gây nhiễu loạn mô hình. SMOGN bị loại bỏ để bảo vệ sự tinh khiết của Không gian Đặc trưng.
- **Sáng tạo Target Power Transformation (TPT - $y^3$):** Thay vì can thiệp biến đầu vào (X), chiến thuật chuyển sang biến đổi biến đầu ra (Y) bằng phép lũy thừa bậc 3. Cơ chế này nén các giá trị ở vùng đáy và phóng to khoảng cách ở vùng đỉnh. **Kết cục:** Mô hình lao lên bắt đỉnh cực kỳ xuất sắc nhưng sai số ở vùng đáy (thung lũng) lại tăng vọt.
- **Kiến trúc Hybrid Two-Stage (Rule-Based):** Để trung hòa, cơ chế "Công tắc" ra đời. Nếu mô hình Base dự báo giá trị < 0.55 thì tin dùng Base (để bám đáy). Nếu >= 0.55, kích hoạt mô hình TPT (để bắt đỉnh). Hệ thống bắt đầu có độ chính xác cao.

## 3. Giai đoạn 3: Khảo sát Giới hạn & Tìm ra Điểm mù
- **Thất bại của Deep Learning (1D-CNN):** Cố gắng ứng dụng Mạng nơ-ron Tích chập 1 chiều (1D-CNN) nhằm tự động trích xuất đặc trưng. **Kết cục:** Mô hình thất bại do dính "Lời nguyền Đói dữ liệu" (Small Data Curse), qua đó khẳng định chắc chắn các thuật toán Tabular dạng cây (như XGBoost) là bá chủ của bộ dữ liệu này.
- **Thử nghiệm DirRec (24 Models) & Lỗi Cộng dồn:** Thử xây chuỗi 24 mô hình nối tiếp để dự báo từng giờ. **Kết cục:** Sụp đổ hoàn toàn do lỗi cộng dồn (Error Propagation). 
- **Phát hiện Điểm mù 24h:** Quan sát thấy hệ thống luôn bị hụt 1 cực trị (thường là đỉnh thứ 2 trong ngày). Phân tích chỉ ra đây là giới hạn vật lý của Tầm nhìn dự báo quá dài (Horizon = 24h). Bắt buộc phải có Lớp 24h làm "Neo định hướng" và một lớp dự báo ngắn hạn để uốn nắn vi mô.

## 4. Giai đoạn 4: Cuộc vật lộn thiết kế Lớp Corrector 1h và Đỉnh cao SOTA
Nhận thấy 24h không thể tối ưu hơn, dự án lùi lại để xây dựng mô hình dự báo cực ngắn (Horizon = 1h, t+1) làm lớp hiệu chỉnh (Corrector). Đây là chương tốn nhiều công sức, thử và sai nhiều nhất:
- **Khởi đầu (Base 1h):** Mô hình t+1 bằng XGBoost/LightGBM đạt RMSE ~0.0668. Tốt, nhưng chưa đạt ngưỡng đột phá.
- **Áp dụng "vũ khí hạng nặng" thất bại:** Mang toàn bộ các kỹ thuật đã thành công ở 24h (Custom Peak Loss, TPT $y^3$, Dự báo biến thiên Delta $\Delta y$) đắp sang 1h. **Kết cục:** Các kỹ thuật này kháng cự lại mô hình 1h, hoàn toàn vô tác dụng, không tạo ra bước nhảy vọt nào.
- **Trận chiến với Căn bệnh "Trễ Pha" (Lag Effect):** Mô hình 1h bám sát thực tế nhưng luôn báo trễ 1 nhịp (chỉ đơn thuần sao chép lag 1 giờ trước). Các thủ thuật triệt tiêu trễ pha được tung ra:
  - Thêm **Kinematic Features** (Vận tốc, Gia tốc biến thiên).
  - Áp dụng **DTW Loss** (Dynamic Time Warping). **Kết cục:** Thất bại vì DTW không tương thích với đạo hàm của Tree Gradients.
  - Sục sạo qua hàng loạt bài báo nghiên cứu (Literature Review) để tìm lối thoát.
- **Kiến trúc Residual Boosting:** Chuyển hướng bóc tách chu kỳ. Dùng Seasonal Baseline để lọc sạch chu kỳ gốc, ép mô hình 1h chỉ tập trung dự báo "Phần dư" (Residual).
- **Cửa tử Data Leakage & Vượt Ải Kiểm duyệt:** Tiến hành Ensemble giữa mô hình 24h và 1h Residual. Bóng ma lớn nhất xuất hiện: **Rò rỉ dữ liệu (Data Leakage)**. Trong thực tế, không thể dùng biến ngoại lai (nhiệt độ, giá điện, traffic) của tương lai để nạp vào mô hình t+1. Nếu giữ nguyên, mô hình sẽ không thể dùng trong môi trường Production.
- **Giải pháp Chốt hạ Tuyệt đỉnh - Proxy-Lag Cascade:** 
  - Khắc phục Data Leakage: Áp dụng **Naive Forecast** (bê nguyên nhiệt độ/giá điện của giờ hiện tại làm mốc cho giờ tương lai).
  - Dùng "Mồi giả": Lấy chính dự báo của Lớp 24h nhét vào làm đặc trưng (Proxy Feature) cho mô hình 1h.
  - Trộn Tỷ lệ Vàng: Ensemble theo tỷ lệ 33% Base (24h Two-Stage) + 67% Proxy (1h).
- **Kết quả SOTA:** Kiến trúc vượt qua bài Test khắc nghiệt (100% No Data Leakage) và thiết lập kỷ lục sai số tinh khiết **RMSE 0.0664**.

---
*Ghi chú cho Phân đội Văn thư (LaTeX Writer): File này cung cấp mạch truyện chính. Sử dụng văn phong học thuật, khách quan khi đưa vào các mục Methodology và Results. Nhấn mạnh vào quá trình "thử sai" để làm nổi bật độ khó của bài toán.*
