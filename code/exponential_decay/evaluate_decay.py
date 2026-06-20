import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error

sys.path.append('code')
from core_functions import prepare_tabular_data, print_info

def run_evaluate_decay():
    print_info("Loading test data and models for Exponential Decay Blending...")
    test_df = pd.read_csv('data_processed/test.csv')
    test_df['timestamp'] = pd.to_datetime(test_df['timestamp'])
    test_df.set_index('timestamp', inplace=True)
    
    # 1. Prepare data
    X_test_24, y_test_24 = prepare_tabular_data(test_df, horizon=24)
    X_test_1, y_test_1 = prepare_tabular_data(test_df, horizon=1)
    
    # 2. Load Models
    xgb_base = joblib.load('code/models/xgb_model.pkl')
    xgb_tpt = joblib.load('code/models/tpt_xgb_model.pkl')
    xgb_recursive = joblib.load('code/models/xgb_recursive.pkl')
    
    # 3. Direct Predictions (Rule-Based Two-Stage)
    print_info("Calculating Direct Predictions...")
    xgb_pred_base = xgb_base.predict(X_test_24)
    xgb_pred_tpt_raw = xgb_tpt.predict(X_test_24)
    xgb_pred_tpt = np.sign(xgb_pred_tpt_raw) * (np.abs(xgb_pred_tpt_raw) ** (1/3))
    
    trigger_threshold = 0.55
    xgb_pred_direct = np.where(xgb_pred_base >= trigger_threshold, xgb_pred_tpt, xgb_pred_base)
    xgb_pred_direct = np.clip(xgb_pred_direct, 0.0, 1.0)
    
    # 4. Iterate over 24-hour blocks
    print_info("Evaluating Recursive Model and Blending...")
    block_size = 24
    offset = 23
    
    all_actuals = []
    all_blended_preds = []
    
    for k in range(offset, len(y_test_24) - block_size + 1, block_size):
        y_true_block = y_test_24.iloc[k : k+block_size].values
        direct_pred_block = xgb_pred_direct[k : k+block_size]
        
        recursive_pred_block = np.zeros(block_size)
        idx_start_1 = k + 23
        
        prev_pred = None
        for i in range(block_size):
            curr_feat = X_test_1.iloc[idx_start_1 + i].copy()
            if prev_pred is not None:
                curr_feat['utilization_lag_1'] = prev_pred
                
            curr_feat_df = curr_feat.to_frame().T
            pred = xgb_recursive.predict(curr_feat_df)[0]
            recursive_pred_block[i] = pred
            prev_pred = pred
            
        # 5. Blend them
        blended_pred_block = np.zeros(block_size)
        for i in range(block_size):
            alpha = 0.85 ** i
            blended_pred_block[i] = alpha * recursive_pred_block[i] + (1 - alpha) * direct_pred_block[i]
            
        blended_pred_block = np.clip(blended_pred_block, 0.0, 1.0)
            
        all_actuals.extend(y_true_block)
        all_blended_preds.extend(blended_pred_block)
        
    all_actuals = np.array(all_actuals)
    all_blended_preds = np.array(all_blended_preds)
    
    rmse = np.sqrt(mean_squared_error(all_actuals, all_blended_preds))
    mae = mean_absolute_error(all_actuals, all_blended_preds)
    
    print("\n--- Exponential Decay Blending (Predictor-Corrector) ---")
    print(f"Blended Model -> RMSE: {rmse:.4f}, MAE: {mae:.4f}")
    
    # 6. Generate plot
    os.makedirs('workspace/figures', exist_ok=True)
    time_axis = np.arange(168)
    
    plt.figure(figsize=(15, 6))
    plt.plot(time_axis, all_actuals[:168], label='Actual', color='black', linewidth=2)
    plt.plot(time_axis, all_blended_preds[:168], label='Blended Predictor-Corrector', color='green', linestyle='--')
    plt.title('Exponential Decay Blending: 7 Days Continuous Forecast')
    plt.xlabel('Hours')
    plt.ylabel('Utilization Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('workspace/figures/exponential_decay_7days.png', dpi=300)
    plt.close()
    
    print("Plot generated successfully at workspace/figures/exponential_decay_7days.png")

if __name__ == "__main__":
    run_evaluate_decay()
