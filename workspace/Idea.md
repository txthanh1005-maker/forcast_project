# IDEA & STATIC SPEC: Chiến dịch Structure Alignment (Cấu trúc lại Báo cáo)

## 1. Objective & Success Criteria
- **Objective:** Tái cấu trúc lại 2 file báo cáo LaTeX (Anh/Việt) để khớp 100% với sơ đồ Tư duy (`requimentinreport.png`) do Giáo sư yêu cầu. 
- **Success Criteria:** 
  - Đẩy phần mô tả "Data Characteristic Analysis" (phân tích đặc tính dữ liệu, ACF/PACF, Feature Importance) xuống hoàn toàn mục **Results and Discussion**.
  - Đưa phần "Case Study" (Giới thiệu Dataset từ Kaggle và chọn trạm EV 00015) lên đầu mục **Material and Method**.
  - Bài viết mượt mà, cấu trúc chuẩn xác theo đúng trình tự Workflow được yêu cầu.

## 2. Assumptions
- File báo cáo hiện tại có cấu trúc tiêu chuẩn nhưng nội dung đang bị trộn lẫn (đưa phân tích biểu đồ lên phần Method).
- Dataset từ Kaggle (EV charging station availability tracking) cung cấp chuỗi thời gian theo dõi trạng thái trạm sạc. Trạm EV 00015 được chọn vì tính biến động đại diện.

## 3. Tech Stack & Structure
- **Target Files:**
  - `Latex_report/sn-article.tex` (Bản Anh)
  - `Latex_report_VN/sn-article.tex` (Bản Việt)

## 4. Boundaries
- **ALWAYS DO:** Đảm bảo giữ nguyên các file ảnh đã xuất (lag_optimization, acf_pacf...). Chỉ DỜI vị trí văn bản và hình ảnh trong file `.tex`. Thêm phần dẫn nhập Case Study.
- **ASK FIRST:** Ghi đè cấu trúc các phần Introduction hay Conclusion nếu thầy không yêu cầu sửa đổi.
- **FORBIDDEN:** Xóa nội dung cốt lõi của bài báo. Chỉ thực hiện "Move" (di chuyển) và "Wrap" (bọc lại/viết thêm từ nối).
