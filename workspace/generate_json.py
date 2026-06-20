import json

with open(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\selected_papers.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

targets = [
    "Support vector regression with asymmetric loss for optimal electric load forecasting",
    "CLEAR-E: Concept-aware lightweight energy adaptation for smart grid load forecasting",
    "Deterministic and Probabilistic Forecasting of Wind Power Generation and Ramp Rate With Expectation-Implemented Deep Learning",
    "Cycle-Aware Adaptive Mixture-of-Experts with High-Demand-Sensitive Asymmetric Loss for Effective Electrical Load Forecasting",
    "A Methodology for Calculating Representative Solar Curves Based on Multi-year Weighted Library and Optimism Frequency Control"
]

output = []
for p in papers:
    if any(t.lower() in p["Title"].lower() for t in targets):
        align = ""
        if "asymmetric loss for optimal electric load forecasting" in p["Title"].lower():
            align = "Bài báo này chứng minh hiệu quả của hàm mất mát phi đối xứng (asymmetric loss) trong việc xử lý biến động phụ tải. Điều này củng cố trực tiếp cho thiết kế Custom Loss của chúng ta trong việc phạt nặng các sai số dự báo thiếu (under-forecasting) tại các đỉnh cực đoan."
        elif "CLEAR-E" in p["Title"]:
            align = "Nghiên cứu áp dụng asymmetric loss kết hợp với domain knowledge để tăng tốc độ thích ứng của mô hình. Cách tiếp cận này tương đồng với triết lý dùng Proxy-Lag để bắt đỉnh cực trị một cách linh hoạt mà không cần thay đổi dữ liệu đầu vào."
        elif "Deterministic and Probabilistic" in p["Title"]:
            align = "Bài báo sử dụng custom loss functions để học được các đặc trưng tín hiệu khác nhau trong năng lượng tái tạo. Nó hỗ trợ mạnh mẽ cho lập luận của chúng ta về việc can thiệp vào Output (Loss/Target) tốt hơn nhiều so với thao tác Input (như SMOGN)."
        elif "Cycle-Aware Adaptive" in p["Title"]:
            align = "Kiến trúc Mixture-of-Experts kết hợp Asymmetric Loss nhạy cảm với nhu cầu cao (High-Demand-Sensitive) để bám sát phụ tải. Điều này lót đường hoàn hảo cho cấu trúc Two-Stage Rule-Based (vợt chóp đỉnh) của đồ án."
        elif "Methodology for Calculating" in p["Title"]:
            align = "Việc sử dụng asymmetric loss function để phạt các sai lệch theo mục tiêu vận hành cụ thể cho thấy tính ứng dụng rộng rãi của phương pháp này. Nó bảo vệ cho sự lựa chọn Target Power Transformation và Custom Loss thay vì mô hình phân loại phức tạp."
        
        output.append({
            "Title": p["Title"],
            "Year": p["Year"],
            "Abstract": p["Abstract"],
            "URL": p["URL"],
            "Alignment with our project": align
        })

import os
os.makedirs(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\report", exist_ok=True)

with open(r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project\workspace\report\lit_subtheme_2.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)
