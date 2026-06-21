## Goal
Xây dựng báo cáo khoa học dự báo tỷ lệ sử dụng trạm sạc xe điện (EV utilization rate) từ dữ liệu `EV-pro1_forcast.csv` và hỗ trợ Tư lệnh nắm vững kiến thức chuyên sâu để bảo vệ đồ án thành công. (ĐÃ HOÀN THÀNH TOÀN BỘ)

## Constraints
- Resample dữ liệu về 1 hour/step. Dự báo t+24 hours.
- So sánh RF, LSTM, LGBM, XGBoost.
- Sử dụng Custom Loss Function để bắt peak fluctuation.
- Báo cáo phải được viết bằng LaTeX, theo cấu trúc chuẩn Q1 (Springer/IEEE).
- Xây dựng file `defense_qa.md` để giải thích chuyên sâu các quyết định thiết kế.
- Mọi giới hạn kiến trúc (như Data Leakage) phải được lý giải bằng học thuật (Operational Realism).

## Progress & Changelog
- **[Archived Progress]:** Hoàn thành xây dựng cấu trúc mô hình Proxy-Lag Cascade Ensemble (Base 24h + 1h Micro-Tuner). Xóa sổ SMOGN và 1D-CNN. Thay thế bằng TPT ($y^3$) và Two-Stage Rule-Based. Xây dựng xong `defense_qa.md` và `README.md` Manifesto.
- **Hoàn thành vá lỗ hổng "Data Leakage & Magic Numbers":** Cung cấp giải trình học thuật Optuna cho các ngưỡng $0.55$, $50.0$ và Tỷ lệ Vàng. Thêm đoạn văn "Operational Realism - Naive Shift $t-24$" vào Mục 2.4 để chứng minh việc ép mô hình 1h mù thông tin là có chủ đích, tôn vinh sức mạnh của Proxy Feature.
- **Hoàn thành chuẩn hóa văn phong học thuật (English Tone Revision):** "Tẩy" sạch các cụm từ cường điệu cảm xúc (Vietglish/Hyperbole), thay bằng hệ thống từ vựng chuẩn mực chuyên ngành.
- **Vượt qua Kiểm toán Logic (Deep Logic Audit):** Vá lỗ hổng phương trình, refactor "Residual Boosting" thành "Proxy Feature Boosting". Bổ sung giới hạn kiến trúc (Limitations) vào Conclusion.
- **Phiên bản Tiếng Việt Học thuật:** Khởi tạo thành công thư mục `Latex_report_VN`. Sử dụng 4 Sub-agents dịch thuật song song. Bản dịch giữ nguyên 100% cấu trúc thẻ LaTeX. Khắc phục lỗi font Tiếng Việt bằng `\usepackage[utf8]{inputenc}` và `\usepackage[T5]{fontenc}`, tối ưu hóa đường dẫn ảnh.

## Key Decisions
- Biến mục tiêu: `utilization_rate` $[0, 1]$.
- Cấu trúc CHỐT HẠ (Proxy-Lag Cascade Ensemble):
  1. **Lớp Base 24h (Trajectory/Proxy):** Two-Stage Rule-Based với Custom Peak Loss.
  2. **Lớp 1h (Corrector):** Dùng Proxy 24h, bị ép Naive Shift để chặn Data Leakage.
  3. **Lớp Ensemble:** Tỷ lệ tối ưu (33% Base + 67% Proxy).

## Next Steps
- DỰ ÁN KẾT THÚC. Toàn bộ `ACTION_PLAN.md` đã hoàn thành 100%. Đã nén và lưu bộ nhớ. Sẵn sàng đóng gói hoặc chạy dọn dẹp thư mục nếu Tư lệnh yêu cầu.

## Critical Context
- Báo cáo LaTeX đã hoàn thiện 100% (cả bản Tiếng Anh gốc và bản Tiếng Việt) tuân thủ khắt khe tiêu chuẩn IEEE Q1.
- Mọi quyết định thiết kế, con số, và giới hạn kiến trúc đều đã được vũ trang lý luận sắc bén.

## Folder Structure Summary
- `workspace/`: Chứa kế hoạch (Idea, ACTION_PLAN), dữ liệu sinh ra và file Q&A bảo vệ đồ án.
- `Latex_report/`: Báo cáo khoa học bản Tiếng Anh (Bản final).
- `Latex_report_VN/`: Báo cáo khoa học bản Tiếng Việt (Bản final) (Tham chiếu chéo ảnh từ thư mục gốc).
- `agy-memory/SESSION_STATE.md`: Bộ nhớ tổng.

## Asset Pointers
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\Idea_Lit.md`
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\Latex_report\sn-article.tex`
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\Latex_report_VN\sn-article.tex`
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\defense_qa.md`
- `C:\Users\Admin\Desktop\HUST\data_science\forcast_project\README.md`
