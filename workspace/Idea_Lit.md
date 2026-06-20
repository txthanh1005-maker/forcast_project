# IDEA SPECIFICATION (LITERATURE REVIEW)

## 1. TỔNG QUAN CHIẾN DỊCH (Objective & Success Criteria)
- **Mục tiêu:** Thực hiện chiến dịch Systematic Literature Review chuyên sâu nhằm xây dựng phần "Introduction & Related Work" mạnh mẽ, lót đường hoàn hảo cho toàn bộ siêu kiến trúc của chúng ta. Mô hình của chúng ta là sự hội tụ tinh hoa: Tích hợp triết lý **Model Predictive Control (MPC)** khi kết nối tầm nhìn vĩ mô 24h với khả năng hiệu chỉnh vi mô 1h (Residual). Trong đó, lõi 24h vận hành dưới dạng **Two-stage Rule-Based** (để bắt song song cả đỉnh và đáy), còn lõi 1h làm nhiệm vụ **Residual Corrector** được neo bởi Proxy.
- **Tiêu chí Thành công:** Tìm đúng các bài báo trên IEEE/Elsevier phản ánh được từng mảng học thuật tạo nên kiến trúc này. Thiết lập được "Research Gap" chuẩn xác cấp độ L2 để làm bệ phóng vững chắc chứng minh tính tất yếu của mô hình.

## 2. PHÂN RÃ CHỦ ĐỀ VÀ TỪ KHÓA ĐA CHIỀU (Sub-themes & Keywords)
**Giới hạn số lượng:** Mỗi chủ đề 4-6 bài báo xuất sắc nhất (Tổng ~20-30 bài, Q1/Q2 IEEE & ScienceDirect).

- **Sub-theme 1: EV Load Forecasting & The Small Data Curse**
  - Khảo sát sự thất bại của Deep Learning cồng kềnh trước lượng dữ liệu nhỏ, tôn vinh hiệu năng của Tabular/Tree-based models.
  - *Keywords:* EV charging demand forecast, small data time-series, tree-based models vs deep learning.
  
- **Sub-theme 2: Extreme Peak Catching (Bắt Đỉnh Cực Đoan)**
  - Phê phán việc bóp méo dữ liệu Đầu vào (như SMOGN phá vỡ biến phân loại). Tập trung vào các thuật toán can thiệp Đầu ra: Custom Loss, Target Power Transformation.
  - *Keywords:* extreme value forecasting, custom loss function power system, target transformation peak load.
  
- **Sub-theme 3: Two-Stage & Rule-Based Architectures (Bắt Đỉnh - Bảo vệ Đáy)**
  - Khảo sát các kiến trúc chia để trị (Two-stage) trong hệ thống điện. Lập luận bảo vệ sự tinh gọn của Rule-Based Switching (Công tắc ngưỡng vật lý) so với việc phải kẹp thêm một mô hình Classifier nặng nề.
  - *Keywords:* two-stage load forecasting, rule-based ensemble, peak and valley forecasting.

- **Sub-theme 4: Residual Learning in Time-Series (Học trên Phần dư)**
  - Tách nhiễu chu kỳ (Seasonality Baseline) và bẻ gãy tính đơn điệu của dự báo 1h bằng thuật toán học Residual.
  - *Keywords:* residual boosting time series, error correction model power demand, residual learning.

- **Sub-theme 5: Multi-Horizon Fusion & MPC Philosophy (Triết lý MPC & Proxy-Lag Cascade)**
  - Đây là cú chốt hạ học thuật lớn nhất: Đưa triết lý **Model Predictive Control (MPC)** vào dự báo. Khảo sát các cấu trúc dùng tầm nhìn dài (24h) làm khung dẫn đường (Proxy/Trajectory), và dùng bước ngắn (1h) để bám sát thực tế theo cơ chế Cascade nhằm triệt tiêu hoàn toàn hiệu ứng Trễ pha (Phase Lag).
  - *Keywords:* model predictive control forecasting, multi-horizon load forecasting, cascade ensemble phase lag.

## 3. TIÊU CHUẨN KỸ THUẬT & RÀNG BUỘC (Boundaries)
- **Nguồn (MUST):** Độc quyền IEEE Xplore và ScienceDirect (Elsevier).
- **BibTeX (MUST):** Khóa trích dẫn chuẩn: `[HọTácGiảChính][NămXuấtBản][TừKhóaChủĐề]`.
- **Trích xuất JSON (MUST):** Không trích xuất định tính chung chung; bắt buộc ghi nhận mô hình toán học và lưới điện/dataset thử nghiệm.
- **Chống Kể chuyện (FORBIDDEN):** Không tóm tắt A làm này, B làm kia. Bắt buộc gom nhóm theo "Conflict/Consensus" và "Argumentative synthesis".
