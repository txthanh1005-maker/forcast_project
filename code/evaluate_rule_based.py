import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error

sys.path.append('code')
from core_functions import prepare_tabular_data, print_info

def run_rule_based_two_stage():
    print_info("Loading test data and models for Rule-Based Two-Stage Evaluation...")
    test_df = pd.read_csv('data_processed/test.csv')
    test_df['timestamp'] = pd.to_datetime(test_df['timestamp'])
    test_df.set_index('timestamp', inplace=True)
    
    horizon = 24
    X_test, y_test_reg = prepare_tabular_data(test_df, horizon=horizon)
    
    # Load Models (We NO LONGER NEED THE CLASSIFIER)
    xgb_base = joblib.load('code/models/xgb_model.pkl')
    xgb_tpt = joblib.load('code/models/tpt_xgb_model.pkl')
    lgbm_base = joblib.load('code/models/lgbm_model.pkl')
    lgbm_tpt = joblib.load('code/models/tpt_lgbm_model.pkl')
    
    # Base Predictions (The Tracker)
    xgb_pred_base = xgb_base.predict(X_test)
    lgbm_pred_base = lgbm_base.predict(X_test)
    
    # TPT Predictions (The Peak Hunter - Must inverse transform)
    xgb_pred_tpt_raw = xgb_tpt.predict(X_test)
    lgbm_pred_tpt_raw = lgbm_tpt.predict(X_test)
    xgb_pred_tpt = np.sign(xgb_pred_tpt_raw) * (np.abs(xgb_pred_tpt_raw) ** (1/3))
    lgbm_pred_tpt = np.sign(lgbm_pred_tpt_raw) * (np.abs(lgbm_pred_tpt_raw) ** (1/3))
    
    # THE ULTIMATE SOLUTION: BASE-TRIGGERED HARD SWITCH
    # If the Base model predicts >= 0.55 (meaning it senses a peak is coming), unleash TPT!
    # If the Base model predicts < 0.55 (meaning we are in a valley), strictly use Base!
    trigger_threshold = 0.55
    
    xgb_pred_final = np.where(xgb_pred_base >= trigger_threshold, xgb_pred_tpt, xgb_pred_base)
    lgbm_pred_final = np.where(lgbm_pred_base >= trigger_threshold, lgbm_pred_tpt, lgbm_pred_base)
    
    # Post-processing (Clipping)
    xgb_pred_final = np.clip(xgb_pred_final, 0.0, 1.0)
    lgbm_pred_final = np.clip(lgbm_pred_final, 0.0, 1.0)
    
    # Evaluation
    print("\n--- Rule-Based Two-Stage Evaluation Metrics ---")
    xgb_rmse = np.sqrt(mean_squared_error(y_test_reg, xgb_pred_final))
    xgb_mae = mean_absolute_error(y_test_reg, xgb_pred_final)
    print(f"Rule-Based XGBoost  -> RMSE: {xgb_rmse:.4f}, MAE: {xgb_mae:.4f}")
    
    # Plotting
    os.makedirs('workspace/figures', exist_ok=True)
    offset = 23
    actuals = y_test_reg[offset:]
    xgb_plot = xgb_pred_final[offset:]
    
    time_axis = np.arange(168)
    
    plt.figure(figsize=(15, 6))
    plt.plot(time_axis, actuals[:168], label='Actual', color='black', linewidth=2)
    plt.plot(time_axis, xgb_plot[:168], label='Rule-Based XGBoost', color='blue', linestyle='--')
    plt.axhline(y=trigger_threshold, color='orange', linestyle=':', label=f'Base Trigger ({trigger_threshold})')
    plt.title('Rule-Based Hard Switch: Flawless Camel Peak Tracking')
    plt.xlabel('Hours')
    plt.ylabel('Utilization Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('workspace/figures/two_stage_rule_based.png', dpi=300)
    plt.close()
    
    print("Rule-Based plots generated successfully at workspace/figures/two_stage_rule_based.png")

if __name__ == "__main__":
    run_rule_based_two_stage()
