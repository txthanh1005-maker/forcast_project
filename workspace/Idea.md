# IDEA & STATIC SPEC: Chiến dịch "Càn quét & Tái thiết" Bibliography

## 1. Objective & Success Criteria
- **Objective:** Tái thiết lập toàn bộ file `sn-bibliography.bib` với dữ liệu (metadata) chuẩn xác 100% (từ nguồn OpenAlex/Web), không còn tác giả "Unknown". Cập nhật file LaTeX `sn-article.tex` để sử dụng các trích dẫn mới, nâng cao độ tin cậy của bài báo khoa học.
- **Success Criteria:** 
  - Hoàn tất tra cứu 14 bài báo (từ `ref1_2` đến `ref4_3`) và lấy chính xác BibTeX (Author, Journal, Year, Volume, DOI, etc.).
  - Tìm mới 1-2 bài báo thực tế (Real papers) thay thế `ref1_0` và `ref1_1` nhằm chứng minh sự hiệu quả của Tree-based models (XGBoost, RF) với dữ liệu nhỏ trong lĩnh vực dự báo EV/tải trọng.
  - File `sn-bibliography.bib` mới không còn bất kỳ entry nào chứa `author={Unknown}`.
  - File `sn-article.tex` được cập nhật thay thế trích dẫn `ref1_0` và `ref1_1` thành công.

## 2. Assumptions
- Các DOI hoặc tiêu đề từ `ref1_2` đến `ref4_3` hiện tại có thể tìm thấy metadata chuẩn xác trên các hệ thống cơ sở dữ liệu học thuật (OpenAlex, Crossref, etc.).
- File LaTeX sử dụng định dạng BibTeX chuẩn để quản lý tài liệu tham khảo.

## 3. Tech Stack & Structure
- **Tools:** `literature-search-openalex`, `search_web`.
- **Target Files:**
  - `Latex_report/sn-bibliography.bib` (Tạo mới hoàn toàn).
  - `Latex_report/sn-article.tex` (Thay thế nội dung).

## 4. Boundaries
- **ALWAYS DO:** Đảm bảo chính tả, định dạng chuẩn BibTeX.
- **ASK FIRST:** Bất cứ khi nào việc thay thế nội dung file `.tex` có nguy cơ hỏng định dạng tài liệu, hoặc không tìm thấy bài báo nào trong số 14 bài, phải báo cáo.
- **FORBIDDEN:** TUYỆT ĐỐI không sử dụng `author={Unknown}`. Không bịa đặt bài báo (hallucination).
