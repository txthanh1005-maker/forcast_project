import pandas as pd
import numpy as np
from utils import print_info
import os
import joblib
import optuna
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
import xgboost as xgb
def load_data(filepath: str) -> pd.DataFrame:
    print_info(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    return df

def handle_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    print_info("Handling missing data...")
    # Forward fill then backward fill for time series
    df_cleaned = df.ffill().bfill()
    return df_cleaned

def resample_data(df: pd.DataFrame) -> pd.DataFrame:
    print_info("Resampling data from 30T to 1H...")
    
    # Define aggregation dictionary based on columns
    agg_dict = {}
    
    continuous_cols = [
        'utilization_rate', 'temperature_f', 'current_price', 
        'gas_price_per_gallon', 'traffic_congestion_index'
    ]
    
    sum_cols = ['precipitation_mm']
    
    categorical_cols = [
        'weather_condition', 'local_event'
    ]
    
    time_features = ['hour_of_day', 'day_of_week', 'month']
    bool_features = ['is_weekend', 'is_peak_hour']
    
    for col in df.columns:
        if col in continuous_cols:
            agg_dict[col] = 'mean'
        elif col in sum_cols:
            agg_dict[col] = 'sum'
        elif col in categorical_cols:
            # Taking the first recorded categorical value in the hour
            agg_dict[col] = 'first'
        elif col in time_features:
            agg_dict[col] = 'first'
        elif col in bool_features:
            agg_dict[col] = 'max'  # True if any True in the hour
        else:
            # Default fallback
            if pd.api.types.is_numeric_dtype(df[col]):
                agg_dict[col] = 'mean'
            else:
                agg_dict[col] = 'first'
                
    # Use 'h' (lowercase) or 'H' for hours
    df_resampled = df.resample('1h').agg(agg_dict)
    
    # Ensure time features are correctly aligned after resampling
    if 'hour_of_day' in df_resampled.columns:
        df_resampled['hour_of_day'] = df_resampled.index.hour
    if 'day_of_week' in df_resampled.columns:
        df_resampled['day_of_week'] = df_resampled.index.dayofweek
    if 'month' in df_resampled.columns:
        df_resampled['month'] = df_resampled.index.month
        
    return df_resampled

def add_time_series_features(df: pd.DataFrame) -> pd.DataFrame:
    print_info("Adding time series features (lags and rolling means)...")
    df_feat = df.copy()
    
    # Lag features
    df_feat['utilization_lag_1'] = df_feat['utilization_rate'].shift(1)
    df_feat['utilization_lag_2'] = df_feat['utilization_rate'].shift(2)
    df_feat['utilization_lag_24'] = df_feat['utilization_rate'].shift(24)
    
    # Rolling features
    df_feat['utilization_rolling_mean_3'] = df_feat['utilization_rate'].rolling(window=3).mean()
    df_feat['utilization_rolling_mean_6'] = df_feat['utilization_rate'].rolling(window=6).mean()
    
    # Drop NaNs
    df_feat.dropna(inplace=True)
    return df_feat

def split_data(df: pd.DataFrame, train_ratio: float = 0.7, val_ratio: float = 0.15) -> tuple:
    print_info("Splitting data into train, val, test...")
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    
    train_df = df.iloc[:train_end]
    val_df = df.iloc[train_end:val_end]
    test_df = df.iloc[val_end:]
    
    print_info(f"Train size: {len(train_df)}, Val size: {len(val_df)}, Test size: {len(test_df)}")
    return train_df, val_df, test_df


def custom_peak_weighted_mse(y_true, y_pred, peak_threshold=0.7, penalty_weight=50.0):
    """
    Custom loss function (Weighted MSE) to heavily penalize errors during peak utilization.
    
    Logic & Defense for Final Exam:
    - Why this logic? In domains like power grids or traffic systems, underestimating 
      a peak is far more costly than normal fluctuations. Failing to predict a peak 
      leads to resource exhaustion.
    - `peak_threshold`: Set to 0.8 (80% utilization rate). We define "peak fluctuation" as 
      any point where the true utilization crosses 80%. This isolates high-stress periods.
    - `penalty_weight`: Set to 5.0. This means errors made when utilization is >= 80% 
      are penalized 5 times more than normal errors. This forces the model 
      to prioritize accuracy during critical peak hours.
      
    Compatibility:
    - Computes the loss value for standard evaluation loops.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Base squared errors
    sq_error = (y_true - y_pred) ** 2
    
    # Identify peak conditions
    is_peak = y_true >= peak_threshold
    
    # Assign weights: 1.0 for normal, penalty_weight for peak periods
    weights = np.ones_like(y_true, dtype=float)
    weights[is_peak] = penalty_weight
    
    # Calculate the weighted mean squared error
    loss = np.mean(weights * sq_error)
    return loss


def peak_weighted_objective(y_true, y_pred, *args):
    """
    Custom objective function compatible with gradient-boosted trees (LightGBM/XGBoost).
    Returns the Gradient and Hessian required by these frameworks.
    
    Logic & Defense for Final Exam:
    - Trees split nodes by optimizing the Gradient (first derivative) and Hessian (second derivative).
    - By multiplying the Gradient and Hessian by `penalty_weight` during peak instances,
      we artificially make the "pull" of peak errors 5x stronger, forcing the tree structure
      to focus on these instances to reduce the loss.
      
    Note for framework use: 
    - Wrap this for LightGBM like: `lambda preds, train_data: peak_weighted_objective(train_data.get_label(), preds)`
    - Wrap this for XGBoost like: `lambda preds, dtrain: peak_weighted_objective(dtrain.get_label(), preds)`
    """
    peak_threshold = 0.7
    penalty_weight = 50.0
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Calculate the gradient and hessian of 1/2 * (y_pred - y_true)^2
    # Gradient of MSE with respect to y_pred is (y_pred - y_true)
    # Hessian of MSE with respect to y_pred is 1.0
    grad = y_pred - y_true
    hess = np.ones_like(y_pred, dtype=float)
    
    # Apply penalty weights
    is_peak = y_true >= peak_threshold
    grad[is_peak] *= penalty_weight
    hess[is_peak] *= penalty_weight
    
    return grad, hess

def prepare_tabular_data(df: pd.DataFrame, target_col: str = 'utilization_rate', horizon: int = 24):
    print_info(f"Preparing tabular data for horizon {horizon}...")
    df_model = df.copy()
    # Target is utilization_rate 24 hours ahead
    df_model['target'] = df_model[target_col].shift(-horizon)
    df_model.dropna(inplace=True)
    
    # Keep only numeric and boolean columns for standard ML models
    df_numeric = df_model.select_dtypes(include=[np.number, bool]).astype(np.float32)
    
    X = df_numeric.drop(columns=['target'])
    y = df_numeric['target']
    return X, y

def prepare_sequence_data(df: pd.DataFrame, target_col: str = 'utilization_rate', horizon: int = 24, seq_length: int = 24):
    print_info(f"Preparing sequence data for horizon {horizon} and seq_length {seq_length}...")
    df_model = df.copy()
    df_model['target'] = df_model[target_col].shift(-horizon)
    df_model.dropna(inplace=True)
    
    df_numeric = df_model.select_dtypes(include=[np.number, bool]).astype(np.float32)
    X_vals = df_numeric.drop(columns=['target']).values
    y_vals = df_numeric['target'].values
    
    X_seq, y_seq = [], []
    for i in range(len(X_vals) - seq_length + 1):
        X_seq.append(X_vals[i:i+seq_length])
        y_seq.append(y_vals[i+seq_length-1])
        
    return np.array(X_seq), np.array(y_seq)

def train_rf(X_train, y_train, X_val, y_val, model_dir):
    print_info("Tuning and training Random Forest...")
    def objective(trial):
        n_estimators = trial.suggest_int('n_estimators', 20, 100)
        max_depth = trial.suggest_int('max_depth', 3, 10)
        
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return custom_peak_weighted_mse(y_val, preds)

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=5)
    
    best_model = RandomForestRegressor(**study.best_params, random_state=42, n_jobs=-1)
    best_model.fit(X_train, y_train)
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(best_model, os.path.join(model_dir, 'rf_model.pkl'))
    return best_model

def train_lgbm(X_train, y_train, X_val, y_val, model_dir):
    print_info("Tuning and training LightGBM...")
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 20, 100),
            'learning_rate': trial.suggest_float('learning_rate', 1e-3, 0.1, log=True),
            'max_depth': trial.suggest_int('max_depth', 3, 8),
            'random_state': 42,
            'verbose': -1
        }
        model = lgb.LGBMRegressor(**params)
        model.set_params(objective=peak_weighted_objective)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return custom_peak_weighted_mse(y_val, preds)

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=5)
    
    best_params = study.best_params
    best_params['verbose'] = -1
    best_model = lgb.LGBMRegressor(**best_params, random_state=42)
    best_model.set_params(objective=peak_weighted_objective)
    best_model.fit(X_train, y_train)
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(best_model, os.path.join(model_dir, 'lgbm_model.pkl'))
    return best_model

def train_xgboost(X_train, y_train, X_val, y_val, model_dir):
    print_info("Tuning and training XGBoost...")
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 20, 100),
            'learning_rate': trial.suggest_float('learning_rate', 1e-3, 0.1, log=True),
            'max_depth': trial.suggest_int('max_depth', 3, 8),
            'random_state': 42
        }
        model = xgb.XGBRegressor(**params)
        model.set_params(objective=peak_weighted_objective)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        return custom_peak_weighted_mse(y_val, preds)

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=5)
    
    best_model = xgb.XGBRegressor(**study.best_params, random_state=42)
    best_model.set_params(objective=peak_weighted_objective)
    best_model.fit(X_train, y_train)
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(best_model, os.path.join(model_dir, 'xgb_model.pkl'))
    return best_model

def train_lstm(X_train_seq, y_train_seq, X_val_seq, y_val_seq, model_dir):
    print_info("Tuning and training LSTM...")
    X_tr = torch.tensor(X_train_seq, dtype=torch.float32)
    y_tr = torch.tensor(y_train_seq, dtype=torch.float32).unsqueeze(-1)
    X_v = torch.tensor(X_val_seq, dtype=torch.float32)
    y_v = torch.tensor(y_val_seq, dtype=torch.float32).unsqueeze(-1)
    
    def objective(trial):
        hidden_size = trial.suggest_int('hidden_size', 16, 64)
        lr = trial.suggest_float('lr', 1e-3, 1e-2, log=True)
        
        rnn = nn.LSTM(input_size=X_tr.shape[2], hidden_size=hidden_size, batch_first=True)
        linear = nn.Linear(hidden_size, 1)
        params = list(rnn.parameters()) + list(linear.parameters())
        optimizer = optim.Adam(params, lr=lr)
        
        for epoch in range(5):
            rnn.train()
            linear.train()
            optimizer.zero_grad()
            out, _ = rnn(X_tr)
            pred = linear(out[:, -1, :])
            
            sq_error = (pred - y_tr) ** 2
            is_peak = (y_tr >= 0.8).float()
            weights = torch.ones_like(y_tr) + is_peak * (5.0 - 1.0)
            loss = torch.mean(weights * sq_error)
            
            loss.backward()
            optimizer.step()
            
        rnn.eval()
        linear.eval()
        with torch.no_grad():
            out, _ = rnn(X_v)
            val_pred = linear(out[:, -1, :])
            val_loss = custom_peak_weighted_mse(y_v.numpy().flatten(), val_pred.numpy().flatten())
            
        return val_loss

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=5)
    
    best_hidden = study.best_params['hidden_size']
    best_lr = study.best_params['lr']
    
    rnn = nn.LSTM(input_size=X_tr.shape[2], hidden_size=best_hidden, batch_first=True)
    linear = nn.Linear(best_hidden, 1)
    params = list(rnn.parameters()) + list(linear.parameters())
    optimizer = optim.Adam(params, lr=best_lr)
    
    for epoch in range(15):
        rnn.train()
        linear.train()
        optimizer.zero_grad()
        out, _ = rnn(X_tr)
        pred = linear(out[:, -1, :])
        
        sq_error = (pred - y_tr) ** 2
        is_peak = (y_tr >= 0.8).float()
        weights = torch.ones_like(y_tr) + is_peak * (5.0 - 1.0)
        loss = torch.mean(weights * sq_error)
        
        loss.backward()
        optimizer.step()
        
    os.makedirs(model_dir, exist_ok=True)
    torch.save({'rnn': rnn.state_dict(), 'linear': linear.state_dict()}, os.path.join(model_dir, 'lstm_model.pth'))
    return rnn, linear
