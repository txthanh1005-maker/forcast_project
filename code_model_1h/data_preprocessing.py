import pandas as pd
import numpy as np
import sys
import os

# Import utils from code folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'code')))
from utils import print_info

def load_data(filepath: str) -> pd.DataFrame:
    print_info(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    return df

def handle_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    print_info("Handling missing data...")
    df_cleaned = df.ffill().bfill()
    return df_cleaned

def resample_data(df: pd.DataFrame) -> pd.DataFrame:
    print_info("Resampling data from 30T to 1H...")
    
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
            agg_dict[col] = 'first'
        elif col in time_features:
            agg_dict[col] = 'first'
        elif col in bool_features:
            agg_dict[col] = 'max'
        else:
            if pd.api.types.is_numeric_dtype(df[col]):
                agg_dict[col] = 'mean'
            else:
                agg_dict[col] = 'first'
                
    df_resampled = df.resample('1h').agg(agg_dict)
    
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
    
    df_feat['utilization_lag_1'] = df_feat['utilization_rate'].shift(1)
    df_feat['utilization_lag_2'] = df_feat['utilization_rate'].shift(2)
    df_feat['utilization_lag_24'] = df_feat['utilization_rate'].shift(24)
    
    df_feat['utilization_rolling_mean_3'] = df_feat['utilization_rate'].rolling(window=3).mean()
    df_feat['utilization_rolling_mean_6'] = df_feat['utilization_rate'].rolling(window=6).mean()
    
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

def prepare_tabular_data(df: pd.DataFrame, target_col: str = 'utilization_rate', horizon: int = 1):
    print_info(f"Preparing tabular data for horizon {horizon}...")
    df_model = df.copy()
    df_model['target'] = df_model[target_col].shift(-horizon)
    df_model.dropna(inplace=True)
    
    df_numeric = df_model.select_dtypes(include=[np.number, bool]).astype(np.float32)
    
    X = df_numeric.drop(columns=['target'])
    y = df_numeric['target']
    return X, y

def full_preprocessing_pipeline(input_filepath: str):
    df = load_data(input_filepath)
    df = handle_missing_data(df)
    df_resampled = resample_data(df)
    df_features = add_time_series_features(df_resampled)
    train_df, val_df, test_df = split_data(df_features)
    
    X_train, y_train = prepare_tabular_data(train_df, horizon=1)
    X_val, y_val = prepare_tabular_data(val_df, horizon=1)
    X_test, y_test = prepare_tabular_data(test_df, horizon=1)
    
    return X_train, y_train, X_val, y_val, X_test, y_test
