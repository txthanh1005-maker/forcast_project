import json

titles_to_select = [
    "Highly accurate peak and valley prediction short-term net load forecasting approach based on decomposition for power systems with high PV penetration",
    "Short-Term Load Forecasting With Deep Residual Networks",
    "A novel approach to short-term load forecasting using fuzzy neural networks",
    "Two-Stage Artificial Neural Network Model for Short-Term Load Forecasting",
    "Daily peak electricity demand forecasting based on an adaptive hybrid two-stage methodology"
]

alignments = {
    "Highly accurate peak and valley prediction short-term net load forecasting approach based on decomposition for power systems with high PV penetration": "This recent study validates our Two-Stage architecture by proving that separating the high-frequency peaks and valleys from the main curve fundamentally increases prediction accuracy. It justifies our decision to use a dedicated Stage 1 for extreme value bounding before applying the 1h corrector.",
    "Short-Term Load Forecasting With Deep Residual Networks": "This paper supports our architectural choice of using a two-stage ensemble strategy where the second stage acts as a residual corrector. It demonstrates that learning on residuals after a primary proxy prediction significantly reduces phase lag and generalization errors.",
    "A novel approach to short-term load forecasting using fuzzy neural networks": "Serving as a foundational piece, this paper established the paradigm of predicting peak and valley extremals separately and mapping the rest of the curve based on them. It perfectly aligns with our Proxy-Lag Cascade design where the 24h Proxy provides the boundaries for the 1h interpolations.",
    "Two-Stage Artificial Neural Network Model for Short-Term Load Forecasting": "This paper provides empirical evidence that splitting the forecasting problem into a two-stage hierarchical model systematically outperforms single-stage end-to-end ML models. It strongly backs our rejection of a monolithic ML approach in favor of a divide-and-conquer rule-based pipeline.",
    "Daily peak electricity demand forecasting based on an adaptive hybrid two-stage methodology": "This research emphasizes the necessity of adaptive two-stage methodologies to capture peak demand accurately in power systems. It validates our use of physical rule-based triggers (e.g., threshold 0.55) over heavy classifiers for switching between peak and valley models."
}

with open("filtered_papers.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

selected_papers = []
for p in papers:
    if p["Title"] in titles_to_select:
        # Avoid duplicates
        if any(sp["Title"] == p["Title"] for sp in selected_papers):
            continue
        selected_papers.append({
            "Title": p["Title"],
            "Year": p["Year"],
            "Abstract": p["Abstract"],
            "URL": p["URL"],
            "Alignment with our project": alignments[p["Title"]]
        })

import os
os.makedirs("workspace/report", exist_ok=True)
with open("workspace/report/lit_subtheme_3.json", "w", encoding="utf-8") as f:
    json.dump(selected_papers, f, indent=4)

print(f"Generated lit_subtheme_3.json with {len(selected_papers)} papers.")
