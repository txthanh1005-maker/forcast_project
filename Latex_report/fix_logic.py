import os

file_path = "C:/Users/Admin/Desktop/HUST/data_science/forcast_project/Latex_report/sn-article.tex"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix Bug 1: Mathematical Contradiction (Option A - Golden Ratio)
text = text.replace("1-hour Residual Corrector model", "1-hour Micro-Tuner model")
text = text.replace("micro-level residual correction", "micro-level agile correction")
text = text.replace("Residual Boosting", "Proxy Feature Boosting")
text = text.replace("strictly learn the dynamic residuals", "predict the absolute target utilizing the proxy")
text = text.replace("Residual Corrector that explicitly learns the dynamic error residuals", "Micro-Tuner that explicitly integrates the macro proxy to predict the absolute target")
text = text.replace("1h Residual \\\\ Corrector ($\\epsilon_t$)", "1h Micro \\\\ Tuner (Absolute)")
text = text.replace("1-hour residual corrector", "1-hour micro-tuner")
text = text.replace("Residual Corrector", "Micro-Tuner")
text = text.replace("residual corrector", "micro-tuner")
text = text.replace("models the dynamic residual error $\\epsilon_t$, defined as:", "integrates the 24-hour prediction as a critical \\textit{Proxy Feature} $P_t$, defined as:")
text = text.replace("\\epsilon_t = y_{t} - \\hat{y}_{24h\\_proxy, t}", "P_t = \\hat{y}_{24h\\_proxy, t}")
text = text.replace("approximates $f(X_t) \\approx \\epsilon_t$. By exclusively learning the kinematics of the residuals", "approximates $\\hat{y}_{1h\\_micro} = f(X_t \\cup \\{P_t\\})$. By explicitly injecting the proxy into the feature space")
text = text.replace("\\hat{y}_{1h\\_residual}", "\\hat{y}_{1h\\_micro}")
text = text.replace("represents the corrective adjustment output by the 1-hour Micro-Tuner", "represents the absolute output from the 1-hour Micro-Tuner")
text = text.replace("Instead of compelling the 1-hour model to forecast the absolute utilization rate---which redundantly forces the algorithm to reconstruct the intricate diurnal seasonality already captured by the 24-hour macro-model---the mathematical objective was profoundly redefined. We systematically stripped the stable seasonal baseline from the target space, constraining the 1-hour micro-model to strictly predict the dynamic ``Residual'' error. By liberating the algorithm from the computational burden of cyclical trend prediction, its entire modeling capacity was reallocated toward mapping rapid, high-frequency stochastic shocks.", "Instead of compelling the 1-hour model to reconstruct the intricate diurnal seasonality from scratch, the mathematical objective was profoundly redefined. We systematically embedded the stable seasonal baseline as a primary structural anchor in the feature space. By injecting the proxy into the feature manifold, the algorithm's modeling capacity is freed from cyclical trend discovery and reallocated toward mapping rapid, high-frequency stochastic shocks.")
text = text.replace("1-hour residual model", "1-hour micro-model")
text = text.replace("Breaking Phase Lag with Residual and Proxy-Lag Integration", "Breaking Phase Lag with Proxy-Lag Integration")
text = text.replace("we introduce the structural breakthrough of Proxy Feature Boosting. Rather than asking the model to predict the absolute load value---which is heavily dominated by the underlying diurnal cycle---we strip away this cyclical baseline. By explicitly forcing the model to predict only the error (the residual) between the naive cyclical expectation and the actual target, the phase lag is effectively shattered. The model is freed from tracking the heavy macro-cycle and can dedicate its entire representational capacity to forecasting high-frequency deviations (Figure~\\ref{fig:1h_residual}).", "we introduce the structural breakthrough of Proxy Feature Boosting. Rather than discarding the diurnal context, we explicitly embed the 24-hour cyclical baseline as a primary feature. By forcing the model to predict the absolute target utilizing this proxy, the phase lag is effectively shattered. The model is anchored by the macro-cycle and can dedicate its representational capacity to forecasting high-frequency deviations (Figure~\\ref{fig:1h_residual}).")
text = text.replace("By isolating and predicting only the error component", "By integrating the proxy feature")

# Fix Bug 2: Fluff & Repetition in Section 3.2
fluff_old = "Rather than injecting severe computational bloat by deploying an independent, autonomous classification network to detect peaks, our architecture adheres to the principle of Occam's Razor. It ingeniously utilizes the stable Baseline Model's prediction as a deterministic physical trigger. Specifically, when the baseline trajectory crosses the rigorously defined physical threshold of $0.55$, the architecture seamlessly executes a hard switch, substituting the conservative baseline forecast with the aggressive TPT peak prediction. As unequivocally demonstrated in Figure \\ref{fig:two_stage_model}, this Two-Stage mechanism perfectly harmonizes the dual requirements of the system. It successfully protects the dense off-peak valleys from stochastic volatility while flawlessly capturing the acute camel peaks, achieving a globally optimal predictive envelope without the cascading errors and computational overhead characteristic of multi-model classifier pipelines."

fluff_new = "As unequivocally demonstrated in Figure \\ref{fig:two_stage_model}, the Two-Stage Rule-Based switch mechanism perfectly harmonizes the dual requirements of the system. Specifically, when the baseline trajectory crosses the rigorously defined threshold of $0.55$, the system executes a hard switch to the aggressive TPT prediction. This successfully protects the dense off-peak valleys from stochastic volatility while flawlessly capturing the acute bimodal peaks, achieving a globally optimal predictive envelope without unnecessary classifier complexity."

text = text.replace(fluff_old, fluff_new)
text = text.replace("``camel peak''", "bimodal peak")
text = text.replace("camel peaks", "bimodal peaks")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Replacement complete.")
