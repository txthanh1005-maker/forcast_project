# Literature Review Synthesis Material

## Sub-theme 1
### Study on orderly charging strategy of EV with load forecasting
- **BibTeX Key:** `\cite{ref1_0_Studyon2023}`
- **Alignment/Argument:** This paper demonstrates the power of combining tree-based XGBoost with other models for EV load forecasting to achieve high accuracy. It reinforces our project's approach of using XGBoost as a foundational component in a hybrid architecture.

### Prediction of EV Charging Behavior Using Machine Learning
- **BibTeX Key:** `\cite{ref1_1_Predictionof2021}`
- **Alignment/Argument:** This paper highlights that ensemble learning models like Random Forest and XGBoost outperform individual deep neural networks for predicting EV behavior. This strongly supports our choice of tree-based models when dealing with diverse input features.

### A comprehensive review on deep learning approaches for short-term load forecasting
- **BibTeX Key:** `\cite{ref1_2_Acomprehensive2023}`
- **Alignment/Argument:** This comprehensive review highlights the data-hungry nature and computational overhead of deep learning models in short-term load forecasting. It serves as a strong counter-argument to justify our project's pivot towards more efficient tree-based algorithms.

### Machine Learning Approaches for EV Charging Behavior: A Review
- **BibTeX Key:** `\cite{ref1_3_Machinelearning2020}`
- **Alignment/Argument:** This review contrasts traditional machine learning techniques with deep neural networks for analyzing EV charging behavior. It provides the necessary background to argue why simpler tabular models often suffice over complex neural networks in limited data scenarios.

### Electric Vehicle Charging Load Forecasting: A Comparative Study of Deep Learning Approaches
- **BibTeX Key:** `\cite{ref1_4_Electricvehicle2019}`
- **Alignment/Argument:** While this paper advocates for deep learning under extensive data conditions, it underscores the models' heavy reliance on massive datasets. This limitation perfectly validates our strategy to employ Tabular/Tree-based models like XGBoost to avoid the small data curse.

## Sub-theme 2
### Support vector regression with asymmetric loss for optimal electric load forecasting
- **BibTeX Key:** `\cite{ref2_0_Supportvector2021}`
- **Alignment/Argument:** Bài báo này chứng minh hiệu quả của hàm mất mát phi đối xứng (asymmetric loss) trong việc xử lý biến động phụ tải. Điều này củng cố trực tiếp cho thiết kế Custom Loss của chúng ta trong việc phạt nặng các sai số dự báo thiếu (under-forecasting) tại các đỉnh cực đoan.

### CLEAR-E: Concept-aware lightweight energy adaptation for smart grid load forecasting
- **BibTeX Key:** `\cite{ref2_1_Cleareconceptaware2025}`
- **Alignment/Argument:** Nghiên cứu áp dụng asymmetric loss kết hợp với domain knowledge để tăng tốc độ thích ứng của mô hình. Cách tiếp cận này tương đồng với triết lý dùng Proxy-Lag để bắt đỉnh cực trị một cách linh hoạt mà không cần thay đổi dữ liệu đầu vào.

### Deterministic and Probabilistic Forecasting of Wind Power Generation and Ramp Rate With Expectation-Implemented Deep Learning
- **BibTeX Key:** `\cite{ref2_2_Deterministicand2025}`
- **Alignment/Argument:** Bài báo sử dụng custom loss functions để học được các đặc trưng tín hiệu khác nhau trong năng lượng tái tạo. Nó hỗ trợ mạnh mẽ cho lập luận của chúng ta về việc can thiệp vào Output (Loss/Target) tốt hơn nhiều so với thao tác Input (như SMOGN).

### Cycle-Aware Adaptive Mixture-of-Experts with High-Demand-Sensitive Asymmetric Loss for Effective Electrical Load Forecasting
- **BibTeX Key:** `\cite{ref2_3_Cycleawareadaptive2026}`
- **Alignment/Argument:** Kiến trúc Mixture-of-Experts kết hợp Asymmetric Loss nhạy cảm với nhu cầu cao (High-Demand-Sensitive) để bám sát phụ tải. Điều này lót đường hoàn hảo cho cấu trúc Two-Stage Rule-Based (vợt chóp đỉnh) của đồ án.

### A Methodology for Calculating Representative Solar Curves Based on Multi-year Weighted Library and Optimism Frequency Control
- **BibTeX Key:** `\cite{ref2_4_Amethodology2026}`
- **Alignment/Argument:** Việc sử dụng asymmetric loss function để phạt các sai lệch theo mục tiêu vận hành cụ thể cho thấy tính ứng dụng rộng rãi của phương pháp này. Nó bảo vệ cho sự lựa chọn Target Power Transformation và Custom Loss thay vì mô hình phân loại phức tạp.

## Sub-theme 3
### Short-Term Load Forecasting With Deep Residual Networks
- **BibTeX Key:** `\cite{ref3_0_Shorttermload2018}`
- **Alignment/Argument:** This paper supports our architectural choice of using a two-stage ensemble strategy where the second stage acts as a residual corrector. It demonstrates that learning on residuals after a primary proxy prediction significantly reduces phase lag and generalization errors.

### Daily peak electricity demand forecasting based on an adaptive hybrid two-stage methodology
- **BibTeX Key:** `\cite{ref3_1_Dailypeak2015}`
- **Alignment/Argument:** This research emphasizes the necessity of adaptive two-stage methodologies to capture peak demand accurately in power systems. It validates our use of physical rule-based triggers (e.g., threshold 0.55) over heavy classifiers for switching between peak and valley models.

### Highly accurate peak and valley prediction short-term net load forecasting approach based on decomposition for power systems with high PV penetration
- **BibTeX Key:** `\cite{ref3_2_Highlyaccurate2023}`
- **Alignment/Argument:** This recent study validates our Two-Stage architecture by proving that separating the high-frequency peaks and valleys from the main curve fundamentally increases prediction accuracy. It justifies our decision to use a dedicated Stage 1 for extreme value bounding before applying the 1h corrector.

### Two-Stage Artificial Neural Network Model for Short-Term Load Forecasting
- **BibTeX Key:** `\cite{ref3_3_Twostageartificial2018}`
- **Alignment/Argument:** This paper provides empirical evidence that splitting the forecasting problem into a two-stage hierarchical model systematically outperforms single-stage end-to-end ML models. It strongly backs our rejection of a monolithic ML approach in favor of a divide-and-conquer rule-based pipeline.

### A novel approach to short-term load forecasting using fuzzy neural networks
- **BibTeX Key:** `\cite{ref3_4_Anovel1998}`
- **Alignment/Argument:** Serving as a foundational piece, this paper established the paradigm of predicting peak and valley extremals separately and mapping the rest of the curve based on them. It perfectly aligns with our Proxy-Lag Cascade design where the 24h Proxy provides the boundaries for the 1h interpolations.

## Sub-theme 4
### CBL-Imputer: A self-attention-based residual-boosting architecture for high-fidelity customer baseline load estimation
- **BibTeX Key:** `\cite{ref4_0_Cblimputera2026}`
- **Alignment/Argument:** This paper perfectly aligns with our Proxy-Lag Cascade architecture by using a two-stage method where a base model captures the main trajectory and a boosted tree model (LightGBM) corrects the residuals. It validates our approach of using residual boosting to catch localized high-frequency errors without disturbing the primary baseline.

### Short-term electrical load forecasting based on error correction using dynamic mode decomposition
- **BibTeX Key:** `\cite{ref4_1_Shorttermelectrical2019}`
- **Alignment/Argument:** This research confirms the effectiveness of separating cyclical load baselines from residuals to enhance forecast accuracy. It provides academic backing for our 1h Corrector layer that predicts errors to break phase lag after the 24h Proxy baseline is established.

### A novel ensemble deep learning model with dynamic error correction and multi-objective ensemble pruning for time series forecasting
- **BibTeX Key:** `\cite{ref4_2_Anovel2020}`
- **Alignment/Argument:** The paper's use of dynamic error correction within an ensemble framework heavily supports our Cascade Ensemble logic. It justifies our mechanism of learning the residual dynamically to compensate for the base model's limitations in catching extreme fluctuations.

### A novel time series forecasting model with deep learning
- **BibTeX Key:** `\cite{ref4_3_Anovel2019}`
- **Alignment/Argument:** The discussion on mitigating errors in deep learning architectures provides a baseline to compare against. This serves as theoretical justification for our Residual Corrector layer, proving that modeling residuals breaks the inertia of time-series models.

## Sub-theme 5
### Unknown Title
- **BibTeX Key:** `\cite{ref5_0_Unknowntitle2025}`
- **Alignment/Argument:** 

### Unknown Title
- **BibTeX Key:** `\cite{ref5_1_Unknowntitle2025}`
- **Alignment/Argument:** 

### Unknown Title
- **BibTeX Key:** `\cite{ref5_2_Unknowntitle2025}`
- **Alignment/Argument:** 

### Unknown Title
- **BibTeX Key:** `\cite{ref5_3_Unknowntitle2025}`
- **Alignment/Argument:** 

