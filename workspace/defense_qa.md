# Tài liệu Bảo vệ Đồ án: Defense Q&A - Proxy-Lag Cascade Ensemble

**Mục tiêu:** Trang bị cho Tư lệnh các lập luận sắc bén, mang tính học thuật cao và thực tiễn để bảo vệ kiến trúc "Proxy-Lag Cascade Ensemble" trước Hội đồng bảo vệ.

## Câu hỏi 1: Tại sao lại chọn resample dữ liệu từ 30 phút lên 1 giờ? Liệu việc này có làm mất mát thông tin quan trọng của tín hiệu gốc hay không?
**Trả lời:**
Thưa Hội đồng, quyết định resample lên 1 giờ không phải là sự hạ cấp dữ liệu mà là một kỹ thuật **khử nhiễu (noise reduction)** có chủ đích. Dữ liệu 30 phút chứa nhiều biến động ngẫu nhiên (micro-fluctuations) do hành vi cắm sạc bất định của người dùng, tạo ra nhiễu tần số cao (high-frequency noise). Việc downsample xuống 1 giờ đóng vai trò như một bộ lọc thông thấp (low-pass filter), làm nổi bật xu hướng vĩ mô (macro-trend) của chu kỳ tải mà không làm mất đi các đặc trưng cốt lõi của đỉnh tải. Điều này giúp mô hình tập trung học các quy luật chu kỳ thay vì cố gắng khớp (overfit) vào nhiễu ngẫu nhiên.

## Câu hỏi 2: Với bài toán chuỗi thời gian (Time-Series), tại sao không sử dụng các mô hình Deep Learning tiên tiến như LSTM, GRU hay Transformer mà lại chọn Tabular Tree-based models (XGBoost)?
**Trả lời:**
Lựa chọn XGBoost dựa trên đặc thù của tập dữ liệu và nguyên lý **Occam's Razor**: "Các giải pháp đơn giản hơn thường tốt hơn nếu chúng giải thích được cùng một hiện tượng". Dữ liệu của chúng em có kích thước tương đối nhỏ và phân tán (small/sparse dataset). Các mô hình Deep Learning như LSTM yêu cầu lượng dữ liệu khổng lồ để hội tụ và rất dễ bị overfit trên dữ liệu nhỏ, đồng thời chúng gặp khó khăn với hiện tượng **Phase Lag** (trễ pha) khi dự báo các điểm đột biến. Ngược lại, XGBoost (Tree-based) cực kỳ mạnh mẽ trong việc nắm bắt các tương tác phi tuyến tính phức tạp trong dữ liệu bảng (tabular data), đặc biệt khi chúng em đã trích xuất các đặc trưng thời gian (time-lag features) thủ công một cách chuẩn xác.

## Câu hỏi 3: Xin giải thích về Custom Peak Loss Function. Tại sao lại đặt mức phạt 50x tại ngưỡng 0.7 Utilization (hoặc 0.343 TPT)?
**Trả lời:**
Trong thực tế vận hành lưới điện, chi phí của việc đánh giá thấp đỉnh tải (under-predicting peaks) cao hơn rất nhiều so với việc dự báo sai ở vùng tải nền (base load) do nguy cơ quá tải máy biến áp. Do đó, chúng em thiết kế **Custom Peak Loss Function (Weighted MSE)** để định tuyến lại sự chú ý của gradient descent. Ngưỡng 0.7 Utilization được xác định là điểm tới hạn (critical threshold) của lưới điện cục bộ. Tại đây (tương đương 0.343 trong không gian TPT), hàm loss áp dụng **trọng số phạt 50x**, buộc mô hình XGBoost phải hội tụ các cây quyết định ưu tiên giảm thiểu sai số ở các điểm đỉnh này, chấp nhận hy sinh một phần nhỏ độ chính xác ở vùng tải thấp để đảm bảo an ninh năng lượng (Grid Stability).

## Câu hỏi 4: Target Power Transformation (TPT - $y^3$) là gì và tại sao lại cần phép biến đổi này thay vì dự báo trực tiếp giá trị Utilization?
**Trả lời:**
TPT ($y^3$) là một kỹ thuật khuếch đại phi tuyến (Non-linear Peak Amplification). Dữ liệu EV Utilization thường phân bố lệch phải (right-skewed), tập trung ở dải giá trị thấp và rất hiếm ở các đỉnh cao. Khi dự báo trực tiếp, mô hình có xu hướng kéo giá trị dự báo về mức trung bình (mean-reversion), dẫn đến việc "bỏ sót đỉnh" (under-estimation). Bằng cách lũy thừa bậc 3 ($y^3$), khoảng cách giữa vùng tải thấp và tải đỉnh bị kéo giãn mạnh mẽ. Điều này buộc hàm mục tiêu (loss function) của mô hình nhận được tín hiệu gradient lớn hơn rất nhiều khi dự báo sai các đỉnh, từ đó nâng cao độ nhạy của mô hình với hiện tượng tải đỉnh cực đoan.

## Câu hỏi 5: Kiến trúc Two-Stage Rule-Based hoạt động như thế nào? Tại sao kích hoạt TPT khi Base model dự báo >= 0.55?
**Trả lời:**
Kiến trúc Two-Stage là cơ chế phân tuyến dự báo. Ở Stage 1, mô hình Base dự báo trên không gian dữ liệu gốc để nắm bắt xu hướng tổng thể. Tuy nhiên, nếu giá trị dự báo của Base model vượt ngưỡng $0.55$, hệ thống xác định đây là tín hiệu cảnh báo có thể hình thành đỉnh tải lớn. Ngay lập tức, luồng dữ liệu được chuyển hướng sang Stage 2: mô hình TPT (đã được huấn luyện chuyên biệt trên không gian $y^3$) sẽ tiếp quản để dự báo chính xác độ cao của đỉnh đó. Ngưỡng 0.55 được xác định qua thực nghiệm phân tích đường cong ROC, cân bằng giữa Recall (bắt đỉnh) và Precision (tránh báo động giả).

## Câu hỏi 6: Tại sao lại dùng Rule-based (ngưỡng 0.55) để chuyển nhánh trong Two-Stage thay vì huấn luyện một mô hình Machine Learning Classifier (như Random Forest hay Logistic Regression) độc lập để phân loại?
**Trả lời:**
Câu trả lời nằm ở nguyên lý **Occam's Razor** và triết lý tối giản hóa pipeline (Pipeline Minimalism). Việc thêm một mô hình Classifier độc lập sẽ làm tăng độ phức tạp của hệ thống (complexity overhead) và đưa vào rủi ro "lỗi dây chuyền" (Cascading Errors): nếu Classifier nhận diện sai, toàn bộ Stage 2 sẽ sụp đổ. Một ngưỡng Rule-Based (0.55) tĩnh trích xuất trực tiếp từ đầu ra của Base Model mang lại tính ổn định (robustness) vượt trội, dễ dàng diễn dịch (interpretability) và có chi phí tính toán (inference time) gần như bằng 0.

## Câu hỏi 7: Vai trò của 1h Residual Corrector (Micro-Tuner) trong kiến trúc tổng thể là gì? Tại sao phải dự báo phần dư (Residual) thay vì dự báo thẳng giá trị cuối cùng?
**Trả lời:**
Đây là một kỹ thuật tinh chỉnh vi mô (Micro-Tuning). Trong dự báo chuỗi thời gian, phần đường cơ sở (cyclical baseline) mang tính chu kỳ cao và dễ học, nhưng độ trễ pha (**Phase Lag**) và các sai số đột biến thường nằm ở phần dư (residuals). Bằng cách sử dụng mô hình Macro (24h) để tạo ra đường cơ sở, chúng em bóc tách chu kỳ tĩnh ra khỏi tín hiệu. Mô hình Micro-Tuner lúc này chỉ tập trung giải quyết bài toán cốt lõi: **"Học phần lỗi chưa giải thích được"**. Việc chia nhỏ bài toán này làm giảm không gian tìm kiếm giả thuyết của mô hình, giúp bộ Corrector nhận diện chính xác độ lệch dư mà không bị nhiễu bởi chu kỳ ngày/đêm.

## Câu hỏi 8: Final ensemble kết hợp theo tỷ lệ 33% Macro (24h) + 67% Micro (1h). Tỷ lệ "Golden Ensemble Ratio" này được xác định dựa trên cơ sở nào?
**Trả lời:**
Tỷ lệ 33% - 67% (hay **Golden Ensemble Ratio**) không phải là ngẫu nhiên mà được tối ưu hóa dựa trên triết lý **Model Predictive Control (MPC)**. Trong MPC, hệ thống cân bằng giữa kế hoạch dài hạn (horizon planning - đại diện bởi Macro 24h) và phản hồi động học ngắn hạn (dynamic feedback - đại diện bởi Micro 1h). Tỷ lệ 67% nghiêng về Micro-Tuner cho thấy hệ thống đặt trọng số lớn vào các cập nhật trạng thái gần nhất để triệt tiêu độ trễ pha (**Phase Lag**). Trong khi đó, 33% Macro đóng vai trò như một mỏ neo (anchor), đảm bảo rằng sự điều chỉnh của Micro-Tuner không bị trượt khỏi quỹ đạo vận hành chung của hệ thống điện.

## Câu hỏi 9: Hệ thống này có thể triển khai thực tế trên các trạm sạc EV hoặc hệ thống quản lý lưới điện (EMS) hiện tại không? Chi phí triển khai như thế nào?
**Trả lời:**
Hoàn toàn khả thi và cực kỳ tối ưu về chi phí. Do chúng em kiên quyết loại bỏ Deep Learning (như LSTM) và Classifier thừa thãi, kiến trúc "Proxy-Lag Cascade Ensemble" dựa trên XGBoost có tốc độ nội suy (inference speed) tính bằng mili-giây. Nó không yêu cầu phần cứng chuyên biệt như GPU đắt tiền mà có thể chạy trơn tru trên các thiết bị Edge Computing thông thường hoặc CPU của các hệ thống SCADA/EMS hiện hữu. Kích thước mô hình nhỏ nhắn nhưng mang lại độ chính xác cao đối với dự báo đỉnh tải là một lợi thế cạnh tranh cốt lõi của kiến trúc này.

## Câu hỏi 10: Điểm yếu hoặc hạn chế lớn nhất của kiến trúc "Proxy-Lag Cascade Ensemble" hiện tại là gì và hướng phát triển trong tương lai?
**Trả lời:**
Hạn chế hiện tại nằm ở tính phụ thuộc vào dữ liệu trễ tĩnh (static lagged data) trong một số điều kiện bất khả kháng (ví dụ: mất điện lưới, sự kiện lễ hội lớn bất thường chưa từng có trong lịch sử). Hướng phát triển tương lai sẽ là tích hợp thêm dữ liệu ngoại sinh (Exogenous variables) như thời tiết thời gian thực, sự kiện xã hội, hoặc giá điện linh hoạt (Time-of-Use pricing) vào hệ thống. Đồng thời, có thể kết hợp phương pháp học trực tuyến (Online Learning) cho bộ Micro-Tuner để nó có thể cập nhật liên tục với từng dòng dữ liệu mới mà không cần phải huấn luyện lại toàn bộ khối Macro.
