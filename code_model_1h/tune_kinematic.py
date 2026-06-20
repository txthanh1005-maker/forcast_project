import os
import sys
import optuna
import lightgbm as lgb
import xgboost as xgb
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_preprocessing import load_data, handle_missing_data, resample_data, add_time_series_features, split_data, prepare_tabular_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))
from utils import print_info

def add_kinematic_features(df: pd.DataFrame) -> pd.DataFrame:
    print_info("Adding kinematic features...")
    df_feat = df.copy()
    
    # add lag 3 as it's not added in basic features
    if 'utilization_lag_3' not in df_feat.columns:
        df_feat['utilization_lag_3'] = df_feat['utilization_rate'].shift(3)
        
    df_feat['Velocity'] = df_feat['utilization_lag_1'] - df_feat['utilization_lag_2']
    df_feat['Acceleration'] = (df_feat['utilization_lag_1'] - df_feat['utilization_lag_2']) - (df_feat['utilization_lag_2'] - df_feat['utilization_lag_3'])
    df_feat['Rolling_Mean_3_Kinematic'] = (df_feat['utilization_lag_1'] + df_feat['utilization_lag_2'] + df_feat['utilization_lag_3']) / 3
    df_feat['Rolling_Std_3_Kinematic'] = df_feat[['utilization_lag_1', 'utilization_lag_2', 'utilization_lag_3']].std(axis=1)
    
    df_feat.dropna(inplace=True)
    return df_feat

def full_preprocessing_pipeline_kinematic(input_filepath: str):
    df = load_data(input_filepath)
    df = handle_missing_data(df)
    df_resampled = resample_data(df)
    df_features = add_time_series_features(df_resampled)
    df_kinematic = add_kinematic_features(df_features)
    
    train_df, val_df, test_df = split_data(df_kinematic)
    
    X_train, y_train = prepare_tabular_data(train_df, horizon=1)
    X_val, y_val = prepare_tabular_data(val_df, horizon=1)
    X_test, y_test = prepare_tabular_data(test_df, horizon=1)
    
    return X_train, y_train, X_val, y_val, X_test, y_test

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
    model.fit(X_train, y_train)
    
    preds = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    return rmse

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
    model.fit(X_train, y_train)
    
    preds = model.predict(X_val)
    rmse = np.sqrt(mean_squared_error(y_val, preds))
    return rmse

def main():
    base_dir = r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project"
    input_filepath = os.path.join(base_dir, "EV-pro1_forcast.csv")
    models_dir = os.path.join(base_dir, "code_model_1h", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    print_info("Running kinematic preprocessing pipeline for t+1 prediction...")
    X_train, y_train, X_val, y_val, X_test, y_test = full_preprocessing_pipeline_kinematic(input_filepath)
    
    print_info("Tuning LightGBM with kinematic features...")
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study_lgbm = optuna.create_study(direction='minimize')
    study_lgbm.optimize(lambda trial: objective_lgbm(trial, X_train, y_train, X_val, y_val), n_trials=30)
    
    print_info(f"Best LightGBM params: {study_lgbm.best_params}")
    print_info(f"Best LightGBM validation RMSE: {study_lgbm.best_value:.4f}")
    best_lgbm = lgb.LGBMRegressor(**study_lgbm.best_params, random_state=42, verbose=-1)
    best_lgbm.fit(X_train, y_train)
    joblib.dump(best_lgbm, os.path.join(models_dir, "tuned_kinematic_lgbm.pkl"))
    
    print_info("Tuning XGBoost with kinematic features...")
    study_xgb = optuna.create_study(direction='minimize')
    study_xgb.optimize(lambda trial: objective_xgb(trial, X_train, y_train, X_val, y_val), n_trials=30)
    
    print_info(f"Best XGBoost params: {study_xgb.best_params}")
    print_info(f"Best XGBoost validation RMSE: {study_xgb.best_value:.4f}")
    best_xgb = xgb.XGBRegressor(**study_xgb.best_params, random_state=42, verbosity=0)
    best_xgb.fit(X_train, y_train)
    joblib.dump(best_xgb, os.path.join(models_dir, "tuned_kinematic_xgb.pkl"))
    
    print_info("Kinematic tuning completed and models saved.")

if __name__ == "__main__":
    main()
