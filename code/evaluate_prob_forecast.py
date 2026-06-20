import pandas as pd
import numpy as np
import joblib
import os
import xgboost as xgb
import matplotlib.pyplot as plt
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, brier_score_loss

sys.path.append('code')
from core_functions import prepare_tabular_data, print_info

def run_prob_forecast():
    print_info("Loading test data and models for Probability Forecast (Smoothed Two-Stage)...")
    train_df = pd.read_csv('data_processed/train.csv')
    test_df = pd.read_csv('data_processed/test.csv')
    train_df['timestamp'] = pd.to_datetime(train_df['timestamp'])
    test_df['timestamp'] = pd.to_datetime(test_df['timestamp'])
    train_df.set_index('timestamp', inplace=True)
    test_df.set_index('timestamp', inplace=True)
    
    horizon = 24
    peak_threshold = 0.6
    
    X_train, y_train_reg = prepare_tabular_data(train_df, horizon=horizon)
    X_test, y_test_reg = prepare_tabular_data(test_df, horizon=horizon)
    
    # 1. TRAIN CLASSIFIER TO OUTPUT RAW PROBABILITIES
    y_train_class = (y_train_reg >= peak_threshold).astype(int)
    y_test_class = (y_test_reg >= peak_threshold).astype(int)
    
    counts = y_train_class.value_counts()
    scale_weight = (counts[0] / counts[1]) * 1.5
    clf = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, scale_pos_weight=scale_weight, random_state=42, n_jobs=1)
    clf.fit(X_train, y_train_class)
    
    # Raw probabilities
    raw_probs = clf.predict_proba(X_test)[:, 1]
    
    # 2. TRANSFORM INTO A TIME-SERIES PERCENTAGE FORECAST (SMOOTHING)
    # Using a rolling mean over 3 hours to create a continuous transition state
    smoothed_probs = pd.Series(raw_probs).rolling(window=3, min_periods=1, center=True).mean().values
    
    # 3. EVALUATE THE PERCENTAGE FORECAST ACCURACY
    # Brier Score measures the accuracy of probabilistic predictions (0 is perfect, 1 is worst)
    raw_brier = brier_score_loss(y_test_class, raw_probs)
    smooth_brier = brier_score_loss(y_test_class, smoothed_probs)
    print("\n--- PERCENTAGE FORECAST ACCURACY (BRIER SCORE) ---")
    print(f"Raw Probabilities Brier Score:      {raw_brier:.4f}")
    print(f"Smoothed Probabilities Brier Score: {smooth_brier:.4f}")
    if smooth_brier < raw_brier:
        print("-> Smoothing improved the probabilistic accuracy!")
    
    # Load Models
    xgb_base = joblib.load('code/models/xgb_model.pkl')
    xgb_tpt = joblib.load('code/models/tpt_xgb_model.pkl')
    lgbm_base = joblib.load('code/models/lgbm_model.pkl')
    lgbm_tpt = joblib.load('code/models/tpt_lgbm_model.pkl')
    
    # Base Predictions
    xgb_pred_base = xgb_base.predict(X_test)
    lgbm_pred_base = lgbm_base.predict(X_test)
    
    # TPT Predictions (Must inverse transform)
    xgb_pred_tpt = xgb_tpt.predict(X_test)
    lgbm_pred_tpt = lgbm_tpt.predict(X_test)
    xgb_pred_tpt = np.sign(xgb_pred_tpt) * (np.abs(xgb_pred_tpt) ** (1/3))
    lgbm_pred_tpt = np.sign(lgbm_pred_tpt) * (np.abs(lgbm_pred_tpt) ** (1/3))
    
    # 4. APPLY SMOOTHED PERCENTAGE TO TWO-STAGE BLENDING
    xgb_pred_two_stage = (1 - smoothed_probs) * xgb_pred_base + smoothed_probs * xgb_pred_tpt
    lgbm_pred_two_stage = (1 - smoothed_probs) * lgbm_pred_base + smoothed_probs * lgbm_pred_tpt
    
    # Post-processing (Clipping)
    xgb_pred_two_stage = np.clip(xgb_pred_two_stage, 0.0, 1.0)
    lgbm_pred_two_stage = np.clip(lgbm_pred_two_stage, 0.0, 1.0)
    
    # 5. EVALUATE FINAL REGRESSION METRICS
    print("\n--- FINAL HYBRID MODEL METRICS ---")
    xgb_rmse = np.sqrt(mean_squared_error(y_test_reg, xgb_pred_two_stage))
    xgb_mae = mean_absolute_error(y_test_reg, xgb_pred_two_stage)
    lgbm_rmse = np.sqrt(mean_squared_error(y_test_reg, lgbm_pred_two_stage))
    lgbm_mae = mean_absolute_error(y_test_reg, lgbm_pred_two_stage)
    print(f"Smoothed Hybrid XGBoost  -> RMSE: {xgb_rmse:.4f}, MAE: {xgb_mae:.4f}")
    print(f"Smoothed Hybrid LightGBM -> RMSE: {lgbm_rmse:.4f}, MAE: {lgbm_mae:.4f}")
    
    # 6. PLOTTING
    os.makedirs('workspace/figures', exist_ok=True)
    offset = 23
    actuals = y_test_reg[offset:]
    xgb_plot = xgb_pred_two_stage[offset:]
    lgbm_plot = lgbm_pred_two_stage[offset:]
    probs_plot = smoothed_probs[offset:]
    
    time_axis = np.arange(168)
    
    # Create a subplot with 2 rows: Top for Forecasting, Bottom for the Percentage Transition
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # Top Plot: Forecast
    ax1.plot(time_axis, actuals[:168], label='Actual', color='black', linewidth=2)
    ax1.plot(time_axis, xgb_plot[:168], label='Smoothed Hybrid XGBoost', color='blue', linestyle='--')
    ax1.plot(time_axis, lgbm_plot[:168], label='Smoothed Hybrid LightGBM', color='red', linestyle='-.')
    ax1.axhline(y=0.7, color='gray', linestyle=':', label='Peak Threshold (0.7)')
    ax1.set_title('Smoothed Hybrid Two-Stage Model: 7 Days Continuous Forecast')
    ax1.set_ylabel('Utilization Rate')
    ax1.legend()
    ax1.grid(True)
    
    # Bottom Plot: The Forecasted Percentage (State Transition)
    ax2.plot(time_axis, probs_plot[:168], label='Forecasted Peak Probability (%)', color='purple', linewidth=2)
    ax2.fill_between(time_axis, 0, probs_plot[:168], color='purple', alpha=0.3)
    ax2.set_title('Forecasted Percentage of State Transition (Base <--> Peak)')
    ax2.set_xlabel('Hours')
    ax2.set_ylabel('Probability')
    ax2.set_ylim(0, 1.1)
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('workspace/figures/two_stage_smoothed.png', dpi=300)
    plt.close()
    
    print("Smoothed Hybrid plots generated at workspace/figures/two_stage_smoothed.png")

if __name__ == "__main__":
    run_prob_forecast()
