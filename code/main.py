import os
import sys

# Ensure the current directory is in sys.path so we can import modules properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_functions import (
    load_data, handle_missing_data, resample_data, split_data,
    add_time_series_features, apply_smote_for_regression,
    prepare_tabular_data, prepare_sequence_data,
    train_rf, train_lgbm, train_xgboost, train_lstm
)
from utils import print_info, print_dataframe_info

def main():
    # Base paths
    base_dir = r"C:\Users\Admin\Desktop\HUST\data_science\forcast_project"
    input_filepath = os.path.join(base_dir, "EV-pro1_forcast.csv")
    output_dir = os.path.join(base_dir, "data_processed")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print_info(f"Created output directory at {output_dir}")
        
    print_info("Starting Data Processing Pipeline...")
    
    # 1. Load Data
    df = load_data(input_filepath)
    print_dataframe_info(df, "Original 30-min Data")
    
    # 2. Handle Missing Data
    df = handle_missing_data(df)
    
    # 3. Resample Data (from 30-min to 1-hour)
    df_resampled = resample_data(df)
    print_dataframe_info(df_resampled, "Resampled 1-hour Data")
    
    # 3.5 Add Time Series Features
    df_features = add_time_series_features(df_resampled)
    print_dataframe_info(df_features, "Features Added Data")
    
    # 4. Split Data (Train, Validation, Test)
    train_df, val_df, test_df = split_data(df_features)
    
    # 5. Save Data
    print_info("Saving processed datasets to disk...")
    train_df.to_csv(os.path.join(output_dir, "train.csv"))
    val_df.to_csv(os.path.join(output_dir, "val.csv"))
    test_df.to_csv(os.path.join(output_dir, "test.csv"))
    
    print_info("Data Processing Pipeline completed successfully!")
    
    # ==========================================
    # Task 3: Modeling & Hyper-tuning
    # ==========================================
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    print_info(f"Starting Modeling phase. Models will be saved to {models_dir}")
    
    # Tabular Data Preparation
    X_train_tab, y_train_tab = prepare_tabular_data(train_df, horizon=24)
    X_val_tab, y_val_tab = prepare_tabular_data(val_df, horizon=24)
    
    # Target Power Transformation (TPT)
    print_info("Applying Target Power Transformation (TPT) y^3...")
    y_train_tab_tpt = y_train_tab ** 3
    y_val_tab_tpt = y_val_tab ** 3
    
    # Train Tabular Models (TPT)
    train_rf(X_train_tab, y_train_tab_tpt, X_val_tab, y_val_tab_tpt, models_dir, model_name='tpt_rf_model.pkl')
    train_lgbm(X_train_tab, y_train_tab_tpt, X_val_tab, y_val_tab_tpt, models_dir, model_name='tpt_lgbm_model.pkl')
    train_xgboost(X_train_tab, y_train_tab_tpt, X_val_tab, y_val_tab_tpt, models_dir, model_name='tpt_xgb_model.pkl')
    
    # Sequence Data Preparation
    X_train_seq, y_train_seq = prepare_sequence_data(train_df, horizon=24, seq_length=24)
    X_val_seq, y_val_seq = prepare_sequence_data(val_df, horizon=24, seq_length=24)
    
    y_train_seq_tpt = y_train_seq ** 3
    y_val_seq_tpt = y_val_seq ** 3
    
    # Train Sequence Model (LSTM) on TPT
    train_lstm(X_train_seq, y_train_seq_tpt, X_val_seq, y_val_seq_tpt, models_dir, model_name='tpt_lstm_model.pth')
    
    print_info("All models trained and saved successfully!")

if __name__ == "__main__":
    main()
