import os
import sys
import lightgbm as lgb
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

# Import from the newly created data preprocessing module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preprocessing import full_preprocessing_pipeline

# Import utils from code folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))
from utils import print_info

def evaluate_model(y_true, y_pred, model_name):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    print(f"[{model_name}] RMSE: {rmse:.4f}, MAE: {mae:.4f}")
    return rmse, mae

def main():
    base_dir = r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project"
    input_filepath = os.path.join(base_dir, "EV-pro1_forcast.csv")
    
    print_info("Running preprocessing pipeline for t+1 prediction...")
    X_train, y_train, X_val, y_val, X_test, y_test = full_preprocessing_pipeline(input_filepath)
    
    print_info("Training Base LightGBM for t+1...")
    # Default loss (MSE), no custom peak weight
    lgbm_model = lgb.LGBMRegressor(random_state=42)
    lgbm_model.fit(X_train, y_train)
    
    preds_lgbm_val = lgbm_model.predict(X_val)
    preds_lgbm_test = lgbm_model.predict(X_test)
    
    print("\n--- LightGBM Validation ---")
    evaluate_model(y_val, preds_lgbm_val, "LightGBM")
    print("--- LightGBM Test ---")
    evaluate_model(y_test, preds_lgbm_test, "LightGBM")
    
    print_info("\nTraining Base XGBoost for t+1...")
    # Default loss (MSE), no custom peak weight
    xgb_model = xgb.XGBRegressor(random_state=42)
    xgb_model.fit(X_train, y_train)
    
    preds_xgb_val = xgb_model.predict(X_val)
    preds_xgb_test = xgb_model.predict(X_test)
    
    print("\n--- XGBoost Validation ---")
    evaluate_model(y_val, preds_xgb_val, "XGBoost")
    print("--- XGBoost Test ---")
    evaluate_model(y_test, preds_xgb_test, "XGBoost")

if __name__ == "__main__":
    main()
