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

- [x] **Task 3: Nâng cấp Đồ họa Học thuật (TikZ / pgfplots Diagrams)**
  - **Description:** 
    Thiết kế và lập trình 4 biểu đồ vector phân tích kiến trúc ngay trong mã LaTeX:
    1. **Time-Series Split:** Cấu trúc chia 70-15-15 chặn rò rỉ dữ liệu (No Look-ahead bias).
    2. **TPT Graph:** Đồ thị toán học hàm lũy thừa bậc 3 ($y^3$) và vùng kích hoạt Penalty.
    3. **Optuna Flowchart:** Sơ đồ thuật toán Bayesian Optimization TPE.
    4. **XAI Decision Tree:** Cây giải thích thuật toán phân tách Peak/Valley.
    - Vượt qua kiểm định an toàn và logic (Domain Reviewer Audit: Pass 100%). Đã tinh chỉnh hoàn thiện đồ họa.
  - **Assignee:** `meta-agent`
