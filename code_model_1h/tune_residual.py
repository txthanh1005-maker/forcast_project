import os
import sys
import optuna
import lightgbm as lgb
import xgboost as xgb
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

# Add the directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preprocessing import full_preprocessing_pipeline

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))
from utils import print_info

def objective_lgbm(trial, X_train, y_train_res, X_val, y_val_res):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'num_leaves': trial.suggest_int('num_leaves', 20, 150),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'random_state': 42
    }
    model = lgb.LGBMRegressor(**params, verbose=-1)
    model.fit(X_train, y_train_res)
    preds = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val_res, preds))
    return rmse

def objective_xgb(trial, X_train, y_train_res, X_val, y_val_res):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'random_state': 42
    }
    model = xgb.XGBRegressor(**params, verbosity=0)
    model.fit(X_train, y_train_res)
    preds = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val_res, preds))
    return rmse

def get_baseline(X, baseline_map):
    X_reset = X.reset_index(drop=True)
    X_merged = pd.merge(X_reset, baseline_map, on=['day_of_week', 'hour_of_day'], how='left')
    return X_merged['baseline'].values

def main():
    base_dir = r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project"
    input_filepath = os.path.join(base_dir, "EV-pro1_forcast.csv")
    models_dir = os.path.join(base_dir, "code_model_1h", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    print_info("Running preprocessing pipeline for t+1 prediction...")
    X_train, y_train, X_val, y_val, X_test, y_test = full_preprocessing_pipeline(input_filepath)
    
    print_info("Calculating Seasonal Baseline...")
    train_df = X_train.copy()
    train_df['target'] = y_train.values
    baseline_map = train_df.groupby(['day_of_week', 'hour_of_day'])['target'].median().reset_index()
    baseline_map.rename(columns={'target': 'baseline'}, inplace=True)
    
    baseline_map.to_csv(os.path.join(models_dir, "residual_baseline_map.csv"), index=False)
    
    y_train_baseline = get_baseline(X_train, baseline_map)
    y_val_baseline = get_baseline(X_val, baseline_map)
    
    y_train_res = y_train.values - y_train_baseline
    y_val_res = y_val.values - y_val_baseline
    
    print_info("Tuning LightGBM for Residual...")
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study_lgbm = optuna.create_study(direction='minimize')
    study_lgbm.optimize(lambda trial: objective_lgbm(trial, X_train, y_train_res, X_val, y_val_res), n_trials=30)
    
    print_info(f"Best LightGBM params: {study_lgbm.best_params}")
    best_lgbm = lgb.LGBMRegressor(**study_lgbm.best_params, random_state=42, verbose=-1)
    best_lgbm.fit(X_train, y_train_res)
    joblib.dump(best_lgbm, os.path.join(models_dir, "tuned_residual_lgbm.pkl"))
    
    print_info("Tuning XGBoost for Residual...")
    study_xgb = optuna.create_study(direction='minimize')
    study_xgb.optimize(lambda trial: objective_xgb(trial, X_train, y_train_res, X_val, y_val_res), n_trials=30)
    
    print_info(f"Best XGBoost params: {study_xgb.best_params}")
    best_xgb = xgb.XGBRegressor(**study_xgb.best_params, random_state=42, verbosity=0)
    best_xgb.fit(X_train, y_train_res)
    joblib.dump(best_xgb, os.path.join(models_dir, "tuned_residual_xgb.pkl"))
    
    print_info("Tuning completed and models saved.")

if __name__ == "__main__":
    main()
