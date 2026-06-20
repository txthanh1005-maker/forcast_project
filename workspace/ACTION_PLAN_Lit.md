# ACTION PLAN (LITERATURE REVIEW CAMPAIGN)

## GIAI ĐOẠN 1: SCOPING & QUERY DESIGN
- [x] Định hình 5 Sub-themes cốt lõi bao trùm siêu kiến trúc MPC, Two-stage và Residual (Đã hoàn thành trong `Idea_Lit.md`).
- [x] Thiết lập Boolean Query chuẩn xác cho từng Sub-theme để cung cấp cho Sĩ quan Trinh sát. (DONE)
  - **Q1:** `("Electric Vehicle" OR "EV charging") AND ("demand forecasting" OR "load forecasting") AND ("small data" OR "tree-based" OR "XGBoost")`
  - **Q2:** `("load forecasting" OR "power system") AND ("extreme value" OR "peak load" OR "custom loss" OR "target transformation" OR "asymmetric loss")`
  - **Q3:** `("load forecasting" OR "demand forecasting") AND ("two-stage" OR "rule-based" OR "peak and valley")`
  - **Q4:** `("time series" OR "load forecasting") AND ("residual learning" OR "error correction" OR "residual boosting")`
  - **Q5:** `("load forecasting" OR "time series") AND ("model predictive control" OR "multi-horizon" OR "cascade ensemble" OR "phase lag")`

## GIAI ĐOẠN 2 & 3: TÌM KIẾM, LỌC VÀ TRÍCH XUẤT JSON (Thực thi Song song 5 Trục)
- [ ] TODO: **Sub-theme 1 (Small Data):** Gọi `researcher` tìm kiếm bằng **Q1** (4-6 bài), thiết lập Reading Notes theo JSON.
- [ ] TODO: **Sub-theme 2 (Peak Catching):** Gọi `researcher` tìm kiếm bằng **Q2** (4-6 bài), thiết lập Reading Notes theo JSON.
- [ ] TODO: **Sub-theme 3 (Two-stage Rule-Based):** Gọi `researcher` tìm kiếm bằng **Q3** (4-6 bài), thiết lập Reading Notes theo JSON.
- [ ] TODO: **Sub-theme 4 (Residual Learning):** Gọi `researcher` tìm kiếm bằng **Q4** (4-6 bài), thiết lập Reading Notes theo JSON.
- [ ] TODO: **Sub-theme 5 (MPC & Cascade):** Gọi `researcher` tìm kiếm bằng **Q5** (4-6 bài), thiết lập Reading Notes theo JSON.

## GIAI ĐOẠN 4A: LOCAL SYNTHESIS (Viết LaTeX Cục Bộ)
- [ ] TODO: Gọi `latex_writer` tổng hợp Sub-theme 1 thành đoạn LaTeX.
- [ ] TODO: Gọi `latex_writer` tổng hợp Sub-theme 2 thành đoạn LaTeX.
- [ ] TODO: Gọi `latex_writer` tổng hợp Sub-theme 3 thành đoạn LaTeX.
- [ ] TODO: Gọi `latex_writer` tổng hợp Sub-theme 4 thành đoạn LaTeX.
- [ ] TODO: Gọi `latex_writer` tổng hợp Sub-theme 5 thành đoạn LaTeX.

## KIỂM DUYỆT CỤC BỘ (LOCAL DUAL-REVIEW)
- [ ] TODO: Gọi song song `domain_reviewer` (Duyệt tính ăn khớp Logic học thuật) và `test-engineer` (Đối soát Fact-check, kiểm tra độ chính xác của trích dẫn BibTeX). Đảm bảo tuân thủ triết lý viết cắt nhỏ.

## GIAI ĐOẠN 4B & 5: GLOBAL INTEGRATION & GAP IDENTIFICATION
- [ ] TODO: Meta-Agent gộp 5 đoạn Local Synthesis, viết câu chuyển ý (Transitions) để xâu chuỗi mạch truyện, và xuất file tổng `references.bib`.
- [ ] TODO: Meta-Agent quét toàn bài để định vị Research Gap cấp độ L2 (Trọng tâm) làm bàn đạp cho triết lý MPC.

## GIAI ĐOẠN 6: GLOBAL DUAL-REVIEW CHỐT HẠ
- [ ] TODO: Gọi lại hệ thống Dual-Reviewer (`domain_reviewer` + `test-engineer`) duyệt bản thảo toàn cục. 
  - *Nếu FAIL:* Trả hồ sơ để làm lại (Chạy Loop).
  - *Nếu PASS:* Nghiệm thu, chốt file `report.tex` và `references.bib`.
