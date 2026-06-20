import os
import sys
import numpy as np
import pandas as pd
import joblib
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Add code directory to path to import core_functions
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))
from core_functions import prepare_tabular_data, prepare_sequence_data, peak_weighted_objective, custom_peak_weighted_mse

def main():
    base_dir = r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project"
    test_path = os.path.join(base_dir, "data_processed", "test.csv")
    models_dir = os.path.join(base_dir, "code", "models")
    figures_dir = os.path.join(base_dir, "workspace", "figures")
    
    os.makedirs(figures_dir, exist_ok=True)
    
    print("Loading test data...")
    df_test = pd.read_csv(test_path)
    if 'timestamp' in df_test.columns:
        df_test['timestamp'] = pd.to_datetime(df_test['timestamp'])
        df_test.set_index('timestamp', inplace=True)
        
    X_test_tab, y_test_tab = prepare_tabular_data(df_test, horizon=24)
    
    print("Loading TPT tabular models...")
    rf_model = joblib.load(os.path.join(models_dir, "tpt_rf_model.pkl"))
    lgbm_model = joblib.load(os.path.join(models_dir, "tpt_lgbm_model.pkl"))
    xgb_model = joblib.load(os.path.join(models_dir, "tpt_xgb_model.pkl"))
    
    print("Predicting with tabular models...")
    rf_preds_raw = rf_model.predict(X_test_tab)
    lgbm_preds_raw = lgbm_model.predict(X_test_tab)
    xgb_preds_raw = xgb_model.predict(X_test_tab)
    
    # Inverse transform (cube root)
    rf_preds = np.sign(rf_preds_raw) * (np.abs(rf_preds_raw) ** (1/3))
    lgbm_preds = np.sign(lgbm_preds_raw) * (np.abs(lgbm_preds_raw) ** (1/3))
    xgb_preds = np.sign(xgb_preds_raw) * (np.abs(xgb_preds_raw) ** (1/3))
    
    X_test_seq, y_test_seq = prepare_sequence_data(df_test, horizon=24, seq_length=24)
    X_test_seq_tensor = torch.tensor(X_test_seq, dtype=torch.float32)
    
    print("Loading LSTM model...")
    lstm_checkpoint = torch.load(os.path.join(models_dir, "tpt_lstm_model.pth"))
    input_size = X_test_seq_tensor.shape[2]
    linear_weight = lstm_checkpoint['linear']['weight']
    hidden_size = linear_weight.shape[1]
    
    rnn = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
    linear = nn.Linear(hidden_size, 1)
    
    rnn.load_state_dict(lstm_checkpoint['rnn'])
    linear.load_state_dict(lstm_checkpoint['linear'])
    
    rnn.eval()
    linear.eval()
    
    print("Predicting with LSTM model...")
    with torch.no_grad():
        out, _ = rnn(X_test_seq_tensor)
        lstm_preds_raw = linear(out[:, -1, :]).numpy().flatten()
        lstm_preds = np.sign(lstm_preds_raw) * (np.abs(lstm_preds_raw) ** (1/3))
        
    print("\n--- Evaluation Metrics ---")
    rf_rmse = np.sqrt(mean_squared_error(y_test_tab, rf_preds))
    rf_mae = mean_absolute_error(y_test_tab, rf_preds)
    print(f"Random Forest -> RMSE: {rf_rmse:.4f}, MAE: {rf_mae:.4f}")
    
    lgbm_rmse = np.sqrt(mean_squared_error(y_test_tab, lgbm_preds))
    lgbm_mae = mean_absolute_error(y_test_tab, lgbm_preds)
    print(f"LightGBM      -> RMSE: {lgbm_rmse:.4f}, MAE: {lgbm_mae:.4f}")
    
    xgb_rmse = np.sqrt(mean_squared_error(y_test_tab, xgb_preds))
    xgb_mae = mean_absolute_error(y_test_tab, xgb_preds)
    print(f"XGBoost       -> RMSE: {xgb_rmse:.4f}, MAE: {xgb_mae:.4f}")
    
    lstm_rmse = np.sqrt(mean_squared_error(y_test_seq, lstm_preds))
    lstm_mae = mean_absolute_error(y_test_seq, lstm_preds)
    print(f"LSTM          -> RMSE: {lstm_rmse:.4f}, MAE: {lstm_mae:.4f}")
    
    print("\nGenerating plots...")
    seq_len = 24
    true_vals = y_test_tab.values[seq_len-1:]
    
    rf_plot = rf_preds[seq_len-1:]
    lstm_plot = lstm_preds
    
    # TPT plots
    lgbm_plot = lgbm_preds[seq_len-1:]
    xgb_plot = xgb_preds[seq_len-1:]
    
    def plot_window(start_idx, end_idx, title, filename, lgbm_data, xgb_data):
        time_axis = np.arange(end_idx - start_idx)
        plt.figure(figsize=(15, 6))
        plt.plot(time_axis, true_vals[start_idx:end_idx], label='Actual', color='black', linewidth=2)
        plt.plot(time_axis, rf_plot[start_idx:end_idx], label='Random Forest', linestyle='--', alpha=0.8)
        plt.plot(time_axis, lgbm_data[start_idx:end_idx], label='LightGBM', linestyle='--', alpha=0.8)
        plt.plot(time_axis, xgb_data[start_idx:end_idx], label='XGBoost', linestyle='--', alpha=0.8)
        plt.plot(time_axis, lstm_plot[start_idx:end_idx], label='LSTM', linestyle='-', alpha=0.8)
        
        plt.title(title)
        plt.xlabel('Hours')
        plt.ylabel('Utilization Rate')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, filename), dpi=300)
        plt.close()

    # Generate 8 TPT Plots
    print("Generating TPT Plots...")
    plot_window(0, min(168, len(true_vals)), 'Model Predictions vs Actual (7-Day Window) - TPT', 'tpt_7days.png', lgbm_plot, xgb_plot)
    for day in range(7):
        s_idx = day * 24
        e_idx = min((day + 1) * 24, len(true_vals))
        plot_window(s_idx, e_idx, f'Model Predictions vs Actual (Day {day+1}) - TPT', f'tpt_day_{day+1}.png', lgbm_plot, xgb_plot)
    
    print("PASS")

if __name__ == "__main__":
    main()
