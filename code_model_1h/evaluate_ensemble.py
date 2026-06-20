import os
import sys
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Append paths
sys.path.append(os.path.join(base_dir, 'code'))
sys.path.append(os.path.join(base_dir, 'code_model_1h'))

from core_functions import prepare_tabular_data
from data_preprocessing import full_preprocessing_pipeline
from utils import print_info

def get_baseline(X, baseline_map):
    X_reset = X.reset_index(drop=True)
    X_merged = pd.merge(X_reset, baseline_map, on=['day_of_week', 'hour_of_day'], how='left')
    return X_merged['baseline'].values

def run_ensemble():
    print_info("Loading test and val data for 24h model...")
    test_df_24h = pd.read_csv(os.path.join(base_dir, 'data_processed', 'test.csv'))
    test_df_24h['timestamp'] = pd.to_datetime(test_df_24h['timestamp'])
    test_df_24h.set_index('timestamp', inplace=True)
    X_test_24, y_test_24 = prepare_tabular_data(test_df_24h, horizon=24)

    val_df_24h = pd.read_csv(os.path.join(base_dir, 'data_processed', 'val.csv'))
    val_df_24h['timestamp'] = pd.to_datetime(val_df_24h['timestamp'])
    val_df_24h.set_index('timestamp', inplace=True)
    X_val_24, _ = prepare_tabular_data(val_df_24h, horizon=24)

    print_info("Loading 24h Models...")
    xgb_base_24 = joblib.load(os.path.join(base_dir, 'code', 'models', 'xgb_model.pkl'))
    xgb_tpt_24 = joblib.load(os.path.join(base_dir, 'code', 'models', 'tpt_xgb_model.pkl'))

    trigger_threshold = 0.55

    # 24h Test Predictions
    xgb_pred_base = xgb_base_24.predict(X_test_24)
    xgb_pred_tpt_raw = xgb_tpt_24.predict(X_test_24)
    xgb_pred_tpt = np.sign(xgb_pred_tpt_raw) * (np.abs(xgb_pred_tpt_raw) ** (1/3))
    xgb_pred_final_24 = np.where(xgb_pred_base >= trigger_threshold, xgb_pred_tpt, xgb_pred_base)
    xgb_pred_final_24 = np.clip(xgb_pred_final_24, 0.0, 1.0)
    pred_24h_series = pd.Series(xgb_pred_final_24, index=X_test_24.index + pd.Timedelta(hours=24), name='pred_24h')

    # 24h Val Predictions
    xgb_pred_base_val = xgb_base_24.predict(X_val_24)
    xgb_pred_tpt_raw_val = xgb_tpt_24.predict(X_val_24)
    xgb_pred_tpt_val = np.sign(xgb_pred_tpt_raw_val) * (np.abs(xgb_pred_tpt_raw_val) ** (1/3))
    xgb_pred_final_24_val = np.where(xgb_pred_base_val >= trigger_threshold, xgb_pred_tpt_val, xgb_pred_base_val)
    xgb_pred_final_24_val = np.clip(xgb_pred_final_24_val, 0.0, 1.0)
    pred_24h_val_series = pd.Series(xgb_pred_final_24_val, index=X_val_24.index + pd.Timedelta(hours=24), name='pred_24h_val')

    # ==========================
    # 1h Residual Boosting Model
    # ==========================
    print_info("Loading data for 1h model...")
    input_filepath = os.path.join(base_dir, 'EV-pro1_forcast.csv')
    X_train_1h, y_train_1h, X_val_1h, y_val_1h, X_test_1h, y_test_1h = full_preprocessing_pipeline(input_filepath)

    print_info("Loading 1h Models...")
    xgb_res_1h = joblib.load(os.path.join(base_dir, 'code_model_1h', 'models', 'tuned_residual_xgb.pkl'))
    baseline_map = pd.read_csv(os.path.join(base_dir, 'code_model_1h', 'models', 'residual_baseline_map.csv'))

    # 1h Test Predictions
    xgb_residual_preds = xgb_res_1h.predict(X_test_1h)
    baseline_test = get_baseline(X_test_1h, baseline_map)
    xgb_final_preds_1h = xgb_residual_preds + baseline_test
    pred_1h_series = pd.Series(xgb_final_preds_1h, index=X_test_1h.index + pd.Timedelta(hours=1), name='pred_1h')

    # 1h Val Predictions
    xgb_residual_preds_val = xgb_res_1h.predict(X_val_1h)
    baseline_val = get_baseline(X_val_1h, baseline_map)
    xgb_final_preds_1h_val = xgb_residual_preds_val + baseline_val
    pred_1h_val_series = pd.Series(xgb_final_preds_1h_val, index=X_val_1h.index + pd.Timedelta(hours=1), name='pred_1h_val')

    # ==========================
    # Ensemble Optimization (Val Set)
    # ==========================
    print_info("Tuning weights on Validation Set...")
    common_idx_val = pred_24h_val_series.index.intersection(pred_1h_val_series.index)
    pred_24h_val = pred_24h_val_series.loc[common_idx_val]
    pred_1h_val = pred_1h_val_series.loc[common_idx_val]
    
    actual_series_val = pd.Series(y_val_1h.values, index=X_val_1h.index + pd.Timedelta(hours=1))
    actuals_val = actual_series_val.loc[common_idx_val]

    best_val_rmse = float('inf')
    best_w = 0.5
    for w in np.linspace(0, 1, 101):
        temp_ens_val = w * pred_24h_val + (1 - w) * pred_1h_val
        temp_rmse = np.sqrt(mean_squared_error(actuals_val, temp_ens_val))
        if temp_rmse < best_val_rmse:
            best_val_rmse = temp_rmse
            best_w = w
            
    print_info(f"Optimal Weight Tuned on Val Set -> 24h: {best_w:.2f}, 1h: {1 - best_w:.2f} (Val RMSE: {best_val_rmse:.4f})")

    # ==========================
    # Evaluate Ensemble (Test Set)
    # ==========================
    common_idx = pred_24h_series.index.intersection(pred_1h_series.index)
    pred_24h = pred_24h_series.loc[common_idx]
    pred_1h = pred_1h_series.loc[common_idx]
    
    actual_series = pd.Series(y_test_1h.values, index=X_test_1h.index + pd.Timedelta(hours=1))
    actuals = actual_series.loc[common_idx]

    pred_ensemble = best_w * pred_24h + (1 - best_w) * pred_1h

    # Metrics
    rmse_24h = np.sqrt(mean_squared_error(actuals, pred_24h))
    mae_24h = mean_absolute_error(actuals, pred_24h)
    
    rmse_1h = np.sqrt(mean_squared_error(actuals, pred_1h))
    mae_1h = mean_absolute_error(actuals, pred_1h)

    rmse_ens = np.sqrt(mean_squared_error(actuals, pred_ensemble))
    mae_ens = mean_absolute_error(actuals, pred_ensemble)

    print("\n--- Evaluation Metrics ---")
    print(f"24h Two-Stage Rule-Based (XGB) -> RMSE: {rmse_24h:.4f}, MAE: {mae_24h:.4f}")
    print(f"1h Residual Boosting (XGB)     -> RMSE: {rmse_1h:.4f}, MAE: {mae_1h:.4f}")
    print(f"Ensemble ({best_w:.2f}/{1-best_w:.2f})             -> RMSE: {rmse_ens:.4f}, MAE: {mae_ens:.4f}")
    
    with open(os.path.join(base_dir, "code_model_1h", "metrics_ensemble.txt"), "w") as f:
        f.write(f"Ensemble RMSE: {rmse_ens:.4f}, MAE: {mae_ens:.4f}\n")

    # Plotting
    figures_dir = os.path.join(base_dir, 'workspace', 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    plt.figure(figsize=(15, 6))
    time_axis = np.arange(168)
    
    plt.plot(time_axis, actuals.values[:168], label='Actual', color='black', linewidth=2)
    plt.plot(time_axis, pred_24h.values[:168], label='24h Two-Stage Rule-Based (XGB)', color='blue', linestyle='--', alpha=0.7)
    plt.plot(time_axis, pred_1h.values[:168], label='1h Residual Boosting (XGB)', color='red', linestyle='-.', alpha=0.7)
    plt.plot(time_axis, pred_ensemble.values[:168], label=f'Ensemble ({best_w:.2f}/{1-best_w:.2f})', color='green', linewidth=2)
    
    plt.title('Ensemble 24h & 1h Model: 7 Days Continuous Forecast')
    plt.xlabel('Hours')
    plt.ylabel('Utilization Rate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, 'ensemble_24h_1h_7days.png'), dpi=300)
    plt.close()
    
    print(f"\nEnsemble plot generated at workspace/figures/ensemble_24h_1h_7days.png")
    print(f"REPORT RMSE: {rmse_ens:.4f}")

if __name__ == "__main__":
    run_ensemble()
