import os
import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(base_dir, 'code'))
sys.path.append(os.path.join(base_dir, 'code_model_1h'))

from core_functions import prepare_tabular_data
from data_preprocessing import full_preprocessing_pipeline
from utils import print_info

def get_baseline(X, baseline_map):
    X_reset = X.reset_index(drop=True)
    X_merged = pd.merge(X_reset, baseline_map, on=['day_of_week', 'hour_of_day'], how='left')
    return X_merged['baseline'].values

print_info("Loading 24h models and data...")
# Load Train, Val, Test for 24h model to ensure continuous predictions without gaps
train_df_24h = pd.read_csv(os.path.join(base_dir, 'data_processed', 'train.csv'))
train_df_24h['timestamp'] = pd.to_datetime(train_df_24h['timestamp'])
train_df_24h.set_index('timestamp', inplace=True)
X_train_24, _ = prepare_tabular_data(train_df_24h, horizon=24)

val_df_24h = pd.read_csv(os.path.join(base_dir, 'data_processed', 'val.csv'))
val_df_24h['timestamp'] = pd.to_datetime(val_df_24h['timestamp'])
val_df_24h.set_index('timestamp', inplace=True)
X_val_24, _ = prepare_tabular_data(val_df_24h, horizon=24)

test_df_24h = pd.read_csv(os.path.join(base_dir, 'data_processed', 'test.csv'))
test_df_24h['timestamp'] = pd.to_datetime(test_df_24h['timestamp'])
test_df_24h.set_index('timestamp', inplace=True)
X_test_24, _ = prepare_tabular_data(test_df_24h, horizon=24)

xgb_base_24 = joblib.load(os.path.join(base_dir, 'code', 'models', 'xgb_model.pkl'))
xgb_tpt_24 = joblib.load(os.path.join(base_dir, 'code', 'models', 'tpt_xgb_model.pkl'))

trigger_threshold = 0.55

def get_24h_predictions(X_input):
    xgb_pred_base = xgb_base_24.predict(X_input)
    xgb_pred_tpt_raw = xgb_tpt_24.predict(X_input)
    xgb_pred_tpt = np.sign(xgb_pred_tpt_raw) * (np.abs(xgb_pred_tpt_raw) ** (1/3))
    xgb_pred_final = np.where(xgb_pred_base >= trigger_threshold, xgb_pred_tpt, xgb_pred_base)
    return np.clip(xgb_pred_final, 0.0, 1.0)

# Generate continuous predictions for Train, Val, Test
pred_24h_train = pd.Series(get_24h_predictions(X_train_24), index=X_train_24.index + pd.Timedelta(hours=24))
pred_24h_val = pd.Series(get_24h_predictions(X_val_24), index=X_val_24.index + pd.Timedelta(hours=24))
pred_24h_test = pd.Series(get_24h_predictions(X_test_24), index=X_test_24.index + pd.Timedelta(hours=24))

# Combine all 24h predictions into a single massive timeline to avoid NaNs
full_pred_24h = pd.concat([pred_24h_train, pred_24h_val, pred_24h_test])
# Sort index just in case
full_pred_24h = full_pred_24h.sort_index()
# Drop duplicates if any overlaps exist
full_pred_24h = full_pred_24h[~full_pred_24h.index.duplicated(keep='last')]

print_info("Loading 1h models and data...")
input_filepath = os.path.join(base_dir, 'EV-pro1_forcast.csv')
X_train_1h, y_train_1h, X_val_1h, y_val_1h, X_test_1h, y_test_1h = full_preprocessing_pipeline(input_filepath)

xgb_res_1h = joblib.load(os.path.join(base_dir, 'code_model_1h', 'models', 'tuned_residual_xgb.pkl'))
baseline_map = pd.read_csv(os.path.join(base_dir, 'code_model_1h', 'models', 'residual_baseline_map.csv'))


df_full = pd.concat([X_train_1h, X_val_1h, X_test_1h])
df_full = df_full.sort_index()
df_full = df_full[~df_full.index.duplicated(keep='last')]

def create_proxy_features(X_orig, full_pred_series, df_full):
    X_proxy = X_orig.copy()
    
    # 1. utilization_rate -> full_pred_series at exact index
    X_proxy['utilization_rate'] = full_pred_series.reindex(X_orig.index).ffill().bfill().values
    
    # 2. utilization_lag_1 -> full_pred_series.shift(1)
    X_proxy['utilization_lag_1'] = full_pred_series.shift(1).reindex(X_orig.index).ffill().bfill().values
    
    # 3. utilization_lag_2 -> full_pred_series.shift(2)
    X_proxy['utilization_lag_2'] = full_pred_series.shift(2).reindex(X_orig.index).ffill().bfill().values
    
    # 4. utilization_rolling_mean_3 and 6
    pred_roll_3 = full_pred_series.rolling(window=3, min_periods=1).mean()
    pred_roll_6 = full_pred_series.rolling(window=6, min_periods=1).mean()
    X_proxy['utilization_rolling_mean_3'] = pred_roll_3.reindex(X_orig.index).ffill().bfill().values
    X_proxy['utilization_rolling_mean_6'] = pred_roll_6.reindex(X_orig.index).ffill().bfill().values
    
    # 5. temperature_f, current_price, weather... (and others that are not deterministic or lag 24)
    target_idx = X_orig.index - pd.Timedelta(hours=24)
    
    naive_cols = [col for col in X_orig.columns if col not in [
        'utilization_rate', 'utilization_lag_1', 'utilization_lag_2', 
        'utilization_rolling_mean_3', 'utilization_rolling_mean_6',
        'utilization_lag_24', 'hour_of_day', 'day_of_week', 'month',
        'is_weekend', 'is_peak_hour'
    ]]
    
    for col in naive_cols:
        shifted_values = df_full[col].reindex(target_idx).values
        X_proxy[col] = shifted_values
        # Handle potential NaNs at the beginning
        X_proxy[col] = X_proxy[col].ffill().bfill()
        
    return X_proxy

# ---------------------------------------------------------
# Create proxy features for Val and Test
# ---------------------------------------------------------
X_val_1h_proxy = create_proxy_features(X_val_1h, full_pred_24h, df_full)
X_test_1h_proxy = create_proxy_features(X_test_1h, full_pred_24h, df_full)

# Run 1h model on Proxy Features (Val)
xgb_residual_preds_proxy_val = xgb_res_1h.predict(X_val_1h_proxy)
baseline_val = get_baseline(X_val_1h_proxy, baseline_map)
pred_proxy_val_series = pd.Series(xgb_residual_preds_proxy_val + baseline_val, index=X_val_1h_proxy.index + pd.Timedelta(hours=1))

# Run 1h model on Proxy Features (Test)
xgb_residual_preds_proxy_test = xgb_res_1h.predict(X_test_1h_proxy)
baseline_test = get_baseline(X_test_1h_proxy, baseline_map)
pred_proxy_test_series = pd.Series(xgb_residual_preds_proxy_test + baseline_test, index=X_test_1h_proxy.index + pd.Timedelta(hours=1))

# ---------------------------------------------------------
# Tune weight on Validation Set
# ---------------------------------------------------------
print_info("Tuning weight on Validation Set...")
common_idx_val = pred_24h_val.index.intersection(pred_proxy_val_series.index)
p24_val = pred_24h_val.loc[common_idx_val]
ppxy_val = pred_proxy_val_series.loc[common_idx_val]

actual_series_val = pd.Series(y_val_1h.values, index=X_val_1h.index + pd.Timedelta(hours=1))
actuals_val = actual_series_val.loc[common_idx_val]

best_val_rmse = float('inf')
best_w = 0.5
for w in np.linspace(0, 1, 101):
    temp_ens_val = w * p24_val + (1 - w) * ppxy_val
    temp_rmse = np.sqrt(mean_squared_error(actuals_val, temp_ens_val))
    if temp_rmse < best_val_rmse:
        best_val_rmse = temp_rmse
        best_w = w

print_info(f"Optimal Weight Tuned on Val Set -> 24h: {best_w:.2f}, Proxy: {1 - best_w:.2f} (Val RMSE: {best_val_rmse:.4f})")

# ---------------------------------------------------------
# Evaluate on Test Set
# ---------------------------------------------------------
print_info("Evaluating Proxy Cascade Model on Test Set...")
common_idx = pred_24h_test.index.intersection(pred_proxy_test_series.index)
p24_test = pred_24h_test.loc[common_idx]
ppxy_test = pred_proxy_test_series.loc[common_idx]

actual_series = pd.Series(y_test_1h.values, index=X_test_1h.index + pd.Timedelta(hours=1))
actuals = actual_series.loc[common_idx]

rmse_24h = np.sqrt(mean_squared_error(actuals, p24_test))
mae_24h = mean_absolute_error(actuals, p24_test)

rmse_proxy = np.sqrt(mean_squared_error(actuals, ppxy_test))
mae_proxy = mean_absolute_error(actuals, ppxy_test)

pred_ensemble = best_w * p24_test + (1 - best_w) * ppxy_test
rmse_ens = np.sqrt(mean_squared_error(actuals, pred_ensemble))
mae_ens = mean_absolute_error(actuals, pred_ensemble)

print(f"\n--- Evaluation Metrics ---")
print(f"24h Model             -> RMSE: {rmse_24h:.4f}, MAE: {mae_24h:.4f}")
print(f"Proxy Cascade Model   -> RMSE: {rmse_proxy:.4f}, MAE: {mae_proxy:.4f}")
print(f"Cascade Ensemble({best_w:.2f}/{1-best_w:.2f})-> RMSE: {rmse_ens:.4f}, MAE: {mae_ens:.4f}")

with open(os.path.join(base_dir, "code_model_1h", "metrics_proxy_cascade.txt"), "w") as f:
    f.write(f"Proxy Cascade RMSE: {rmse_proxy:.4f}, MAE: {mae_proxy:.4f}\n")
    f.write(f"Cascade Ensemble RMSE: {rmse_ens:.4f}, MAE: {mae_ens:.4f}\n")

figures_dir = os.path.join(base_dir, 'workspace', 'figures')
os.makedirs(figures_dir, exist_ok=True)
plt.figure(figsize=(15, 6))
time_axis = np.arange(168)
plt.plot(time_axis, actuals.values[:168], label='Actual', color='black', linewidth=2)
plt.plot(time_axis, p24_test.values[:168], label='24h Model', color='blue', linestyle='--', alpha=0.7)
plt.plot(time_axis, ppxy_test.values[:168], label='Proxy Cascade', color='red', linestyle='-.', alpha=0.7)
plt.plot(time_axis, pred_ensemble.values[:168], label=f'Cascade Ensemble ({best_w:.2f}/{1-best_w:.2f})', color='green', linewidth=2)
plt.title('Strict Proxy Cascade Model (No Leakage): 7 Days Continuous Forecast')
plt.xlabel('Hours')
plt.ylabel('Utilization Rate')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'proxy_cascade_7days_strict.png'), dpi=300)
plt.close()
print("Saved plot to proxy_cascade_7days_strict.png")

daily_dir = os.path.join(figures_dir, 'daily_proxy_strict')
os.makedirs(daily_dir, exist_ok=True)
for day in range(7):
    start_idx = day * 24
    end_idx = (day + 1) * 24
    plt.figure(figsize=(10, 5))
    time_axis = np.arange(24)
    plt.plot(time_axis, actuals.values[start_idx:end_idx], label='Actual', color='black', linewidth=2)
    plt.plot(time_axis, p24_test.values[start_idx:end_idx], label='24h Model', color='blue', linestyle='--', alpha=0.7)
    plt.plot(time_axis, ppxy_test.values[start_idx:end_idx], label='Proxy 1h', color='red', linestyle='-.', alpha=0.7)
    plt.plot(time_axis, pred_ensemble.values[start_idx:end_idx], label=f'Cascade ({best_w:.2f}/{1-best_w:.2f})', color='green', linewidth=2)
    plt.title(f'Strict Proxy Cascade Model - Day {day + 1}')
    plt.xlabel('Hour of Day')
    plt.ylabel('Utilization Rate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(daily_dir, f'proxy_cascade_day_{day + 1}.png'), dpi=300)
    plt.close()
print("Saved 7 daily plots to workspace/figures/daily_proxy_strict/")
