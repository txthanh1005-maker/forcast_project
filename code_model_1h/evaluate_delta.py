import os
import sys
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preprocessing import full_preprocessing_pipeline

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))
from utils import print_info

def evaluate_model(y_true, y_pred, model_name):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    print(f"[{model_name}] RMSE: {rmse:.4f}, MAE: {mae:.4f}")
    return rmse, mae

def plot_window(start_idx, end_idx, title, filename, figures_dir, true_vals, lgbm_data, xgb_data):
    time_axis = np.arange(end_idx - start_idx)
    plt.figure(figsize=(15, 6))
    plt.plot(time_axis, true_vals[start_idx:end_idx], label='Actual', color='black', linewidth=2)
    plt.plot(time_axis, lgbm_data[start_idx:end_idx], label='Tuned LightGBM (Delta)', linestyle='--', alpha=0.8)
    plt.plot(time_axis, xgb_data[start_idx:end_idx], label='Tuned XGBoost (Delta)', linestyle='--', alpha=0.8)
    
    plt.title(title)
    plt.xlabel('Hours')
    plt.ylabel('Utilization Rate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, filename), dpi=300)
    plt.close()

def main():
    base_dir = r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project"
    input_filepath = os.path.join(base_dir, "EV-pro1_forcast.csv")
    models_dir = os.path.join(base_dir, "code_model_1h", "models")
    figures_dir = os.path.join(base_dir, "workspace", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    print_info("Loading test data...")
    X_train, y_train, X_val, y_val, X_test, y_test = full_preprocessing_pipeline(input_filepath)
    
    print_info("Loading tuned delta models...")
    lgbm_model = joblib.load(os.path.join(models_dir, "tuned_delta_lgbm.pkl"))
    xgb_model = joblib.load(os.path.join(models_dir, "tuned_delta_xgb.pkl"))
    
    print_info("Predicting delta with tuned models...")
    delta_preds_lgbm = lgbm_model.predict(X_test)
    delta_preds_xgb = xgb_model.predict(X_test)
    
    # Recover original prediction: y_pred = Lag_1 + delta_pred
    lgbm_preds = X_test['utilization_rate'].values + delta_preds_lgbm
    xgb_preds = X_test['utilization_rate'].values + delta_preds_xgb
    
    print("\n--- Evaluation Metrics on Test Set (Delta Recovery) ---")
    rmse_lgbm, mae_lgbm = evaluate_model(y_test, lgbm_preds, "LightGBM Delta")
    rmse_xgb, mae_xgb = evaluate_model(y_test, xgb_preds, "XGBoost Delta")
    
    true_vals = y_test.values
    
    print_info("Generating Plots...")
    # 7-day continuous plot
    plot_window(0, min(168, len(true_vals)), 'Model Predictions vs Actual (7-Day Window) - 1h Tuned Delta', '1h_tune_delta_7days.png', figures_dir, true_vals, lgbm_preds, xgb_preds)
        
    print_info("Evaluation and plotting completed.")

if __name__ == "__main__":
    main()
