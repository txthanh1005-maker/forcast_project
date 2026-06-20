import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
import sys
import os

sys.path.append('code')
from core_functions import prepare_tabular_data, print_info

def run_classification_check():
    print_info("Loading data for Classification Check...")
    train_df = pd.read_csv('data_processed/train.csv')
    test_df = pd.read_csv('data_processed/test.csv')
    
    train_df['timestamp'] = pd.to_datetime(train_df['timestamp'])
    test_df['timestamp'] = pd.to_datetime(test_df['timestamp'])
    train_df.set_index('timestamp', inplace=True)
    test_df.set_index('timestamp', inplace=True)
    
    horizon = 24
    peak_threshold = 0.6
    
    X_train, y_train_reg = prepare_tabular_data(train_df, horizon=horizon)
    X_test, y_test_reg = prepare_tabular_data(test_df, horizon=horizon)
    
    # Convert regression target to binary classification target
    y_train = (y_train_reg >= peak_threshold).astype(int)
    y_test = (y_test_reg >= peak_threshold).astype(int)
    
    counts = y_train.value_counts()
    print_info(f"Train Class Distribution: \n{counts}")
    
    if 1 not in counts:
        print_info("No peaks found in training data for this threshold!")
        return
        
    scale_weight = (counts[0] / counts[1]) * 1.5 # Boost recall
    
    print_info(f"Training XGBClassifier with scale_pos_weight = {scale_weight:.2f}...")
    clf = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        scale_pos_weight=scale_weight,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    
    print_info("Predicting on Test Set...")
    preds = clf.predict(X_test)
    
    print("\n" + "="*50)
    print(f"CLASSIFICATION REPORT (Threshold >= {peak_threshold})")
    print("="*50)
    print(classification_report(y_test, preds))
    
    print("CONFUSION MATRIX:")
    cm = confusion_matrix(y_test, preds)
    print(f"                Predicted Đáy (0) | Predicted Đỉnh (1)")
    print(f"Thực tế Đáy (0) | {cm[0][0]:<15} | {cm[0][1]}")
    print(f"Thực tế Đỉnh (1)| {cm[1][0]:<15} | {cm[1][1]}")
    print("="*50)
    
    recall = cm[1][1] / (cm[1][0] + cm[1][1])
    print(f"-> Khả năng BẮT TRÚNG ĐỈNH (Recall Class 1): {recall*100:.2f}%")

if __name__ == "__main__":
    run_classification_check()
