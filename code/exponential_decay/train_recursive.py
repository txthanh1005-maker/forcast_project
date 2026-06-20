import pandas as pd
import os
import sys
import joblib

sys.path.append('code')
from core_functions import prepare_tabular_data, train_xgboost, print_info

def run():
    print_info("Loading train data for Recursive Model...")
    train_df = pd.read_csv('data_processed/train.csv')
    train_df['timestamp'] = pd.to_datetime(train_df['timestamp'])
    train_df.set_index('timestamp', inplace=True)
    
    val_df = pd.read_csv('data_processed/val.csv')
    val_df['timestamp'] = pd.to_datetime(val_df['timestamp'])
    val_df.set_index('timestamp', inplace=True)

    horizon = 1
    
    X_train, y_train = prepare_tabular_data(train_df, horizon=horizon)
    X_val, y_val = prepare_tabular_data(val_df, horizon=horizon)
    
    train_xgboost(X_train, y_train, X_val, y_val, 'code/models', 'xgb_recursive.pkl')
    print_info("Recursive model saved to code/models/xgb_recursive.pkl")

if __name__ == "__main__":
    run()
