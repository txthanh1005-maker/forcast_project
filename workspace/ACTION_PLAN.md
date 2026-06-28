# ACTION PLAN: Structure Alignment (Tái cấu trúc báo cáo)

## Danh sách Task

- [x] **Task 1: Cập nhật Cấu trúc LaTeX Tiếng Anh (`sn-article.tex`)**
  - **Description:** 
    1. **Tạo tiểu mục "Case Study" ở đầu Material and Method:** Viết đoạn văn giới thiệu dataset Kaggle (EV charging station availability tracking) cung cấp hồ sơ sạc thực tế. Viết lý luận tại sao lọc ra trạm "EV 00015" làm đối tượng nghiên cứu (đại diện cho mẫu phân bố có độ nhiễu cao, tính chu kỳ phức tạp).
    2. **Cắt/Dán (Move):** Cắt bỏ phần "Data Characteristic Analysis" (cùng với ACF, PACF, Feature Selection) hiện đang lạc lõng ở Methodology.
    3. **Dán vào Results and Discussion:** Đưa toàn bộ nội dung phân tích đặc trưng dữ liệu, ACF/PACF, đồ thị Lag Optuna và Feature Importance xuống mục Results. Viết lại vài câu nối (transition sentences) để đảm bảo mạch văn logic "Trình bày kết quả theo trình tự workflow nghiên cứu" (như sơ đồ thầy yêu cầu).
  - **Assignee:** `latex_writer`

- [x] **Task 2: Đồng bộ Cấu trúc LaTeX Tiếng Việt (`Latex_report_VN`)**
  - **Description:** 
    Thực hiện tương tự Task 1 nhưng đối với bản Tiếng Việt. Dịch đoạn dẫn nhập Case Study Kaggle sang tiếng Việt học thuật. Đảm bảo cấu trúc Heading 2, Heading 3 khớp 100% với bản Tiếng Anh.
  - **Assignee:** `latex_writer`
