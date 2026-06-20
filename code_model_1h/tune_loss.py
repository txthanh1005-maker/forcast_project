import os
import sys
import optuna
import lightgbm as lgb
import xgboost as xgb
import joblib
import numpy as np

# Add the directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preprocessing import full_preprocessing_pipeline

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))
from utils import print_info
from core_functions import custom_peak_weighted_mse, peak_weighted_objective

def objective_lgbm(trial, X_train, y_train, X_val, y_val):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'num_leaves': trial.suggest_int('num_leaves', 20, 150),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'random_state': 42
    }
    
    model = lgb.LGBMRegressor(**params, verbose=-1)
    model.set_params(objective=peak_weighted_objective)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_val)
    # Use custom loss for evaluation
    loss = custom_peak_weighted_mse(y_val, preds)
    return loss

def objective_xgb(trial, X_train, y_train, X_val, y_val):
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
    model.set_params(objective=peak_weighted_objective)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_val)
    # Use custom loss for evaluation
    loss = custom_peak_weighted_mse(y_val, preds)
    return loss

def main():
    base_dir = r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project"
    input_filepath = os.path.join(base_dir, "EV-pro1_forcast.csv")
    models_dir = os.path.join(base_dir, "code_model_1h", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    print_info("Running preprocessing pipeline for t+1 prediction...")
    X_train, y_train, X_val, y_val, X_test, y_test = full_preprocessing_pipeline(input_filepath)
    
    print_info("Tuning LightGBM with custom loss for t+1...")
    # Use optuna to tune
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study_lgbm = optuna.create_study(direction='minimize')
    study_lgbm.optimize(lambda trial: objective_lgbm(trial, X_train, y_train, X_val, y_val), n_trials=30)
    
    print_info(f"Best LightGBM params: {study_lgbm.best_params}")
    print_info(f"Best LightGBM validation Custom Loss: {study_lgbm.best_value:.4f}")
    best_lgbm = lgb.LGBMRegressor(**study_lgbm.best_params, random_state=42, verbose=-1)
    best_lgbm.set_params(objective=peak_weighted_objective)
    best_lgbm.fit(X_train, y_train)
    joblib.dump(best_lgbm, os.path.join(models_dir, "tuned_loss_lgbm_model.pkl"))
    
    print_info("Tuning XGBoost with custom loss for t+1...")
    study_xgb = optuna.create_study(direction='minimize')
    study_xgb.optimize(lambda trial: objective_xgb(trial, X_train, y_train, X_val, y_val), n_trials=30)
    
    print_info(f"Best XGBoost params: {study_xgb.best_params}")
    print_info(f"Best XGBoost validation Custom Loss: {study_xgb.best_value:.4f}")
    best_xgb = xgb.XGBRegressor(**study_xgb.best_params, random_state=42, verbosity=0)
    best_xgb.set_params(objective=peak_weighted_objective)
    best_xgb.fit(X_train, y_train)
    joblib.dump(best_xgb, os.path.join(models_dir, "tuned_loss_xgb_model.pkl"))
    
    print_info("Tuning completed and models saved.")

if __name__ == "__main__":
    main()
