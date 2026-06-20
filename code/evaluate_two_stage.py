import pandas as pd
import numpy as np
import joblib
import os
import xgboost as xgb
import matplotlib.pyplot as plt
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error

sys.path.append('code')
from core_functions import prepare_tabular_data, print_info

def run_two_stage():
    print_info("Loading test data and models for Two-Stage Evaluation...")
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
    
    # Train Classifier
    y_train_class = (y_train_reg >= peak_threshold).astype(int)
    counts = y_train_class.value_counts()
    scale_weight = (counts[0] / counts[1]) * 1.5
    clf = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, scale_pos_weight=scale_weight, random_state=42, n_jobs=1)
    clf.fit(X_train, y_train_class)
    
    pred_proba_peak = clf.predict_proba(X_test)[:, 1]
    
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
    
    # Combine Predictions using Soft Blending (Gating Mechanism)
    xgb_pred_two_stage = (1 - pred_proba_peak) * xgb_pred_base + pred_proba_peak * xgb_pred_tpt
    lgbm_pred_two_stage = (1 - pred_proba_peak) * lgbm_pred_base + pred_proba_peak * lgbm_pred_tpt
    
    # Post-processing (Clipping) suggested by Domain Reviewer
    xgb_pred_two_stage = np.clip(xgb_pred_two_stage, 0.0, 1.0)
    lgbm_pred_two_stage = np.clip(lgbm_pred_two_stage, 0.0, 1.0)
    
    # Evaluation
    print("\n--- Two-Stage Evaluation Metrics ---")
    xgb_rmse = np.sqrt(mean_squared_error(y_test_reg, xgb_pred_two_stage))
    xgb_mae = mean_absolute_error(y_test_reg, xgb_pred_two_stage)
    lgbm_rmse = np.sqrt(mean_squared_error(y_test_reg, lgbm_pred_two_stage))
    lgbm_mae = mean_absolute_error(y_test_reg, lgbm_pred_two_stage)
    print(f"Two-Stage XGBoost  -> RMSE: {xgb_rmse:.4f}, MAE: {xgb_mae:.4f}")
    print(f"Two-Stage LightGBM -> RMSE: {lgbm_rmse:.4f}, MAE: {lgbm_mae:.4f}")
    
    # Plotting (Offset by 23 hours to match previous plots that included LSTM seq_length-1)
    os.makedirs('workspace/figures', exist_ok=True)
    offset = 23
    timestamps = test_df.index[horizon + offset:]
    actuals = y_test_reg[offset:]
    xgb_plot = xgb_pred_two_stage[offset:]
    lgbm_plot = lgbm_pred_two_stage[offset:]
    
    # 7 Days plot (168 hours)
    time_axis = np.arange(168)
    plt.figure(figsize=(15, 6))
    plt.plot(time_axis, actuals[:168], label='Actual', color='black', linewidth=2)
    plt.plot(time_axis, xgb_plot[:168], label='Soft Two-Stage XGBoost', color='blue', linestyle='--')
    plt.plot(time_axis, lgbm_plot[:168], label='Soft Two-Stage LightGBM', color='red', linestyle='-.')
    plt.axhline(y=0.7, color='gray', linestyle=':', label='Peak Threshold (0.7)')
    plt.axhline(y=0.6, color='orange', linestyle=':', label='Classifier Threshold (0.6)')
    plt.title('Soft Hybrid Two-Stage Model: 7 Days Continuous Forecast')
    plt.xlabel('Hours')
    plt.ylabel('Utilization Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('workspace/figures/two_stage_7days.png', dpi=300)
    plt.close()
    
    print("Two-Stage plots generated successfully at workspace/figures/two_stage_7days.png")

if __name__ == "__main__":
    run_two_stage()
