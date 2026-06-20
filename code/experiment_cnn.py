import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import joblib
import os
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import sys

sys.path.append('code')
from core_functions import prepare_sequence_data, prepare_tabular_data

# 1. Define 1D-CNN Architecture
class PeakHunterCNN(nn.Module):
    def __init__(self, num_features):
        super(PeakHunterCNN, self).__init__()
        # Conv1d expects (batch, channels, length)
        self.conv1 = nn.Conv1d(in_channels=num_features, out_channels=16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool1d(kernel_size=2)
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.flatten = nn.Flatten()
        # seq_len=24 -> pool -> 12 -> pool -> 6
        self.fc1 = nn.Linear(32 * 6, 16)
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        x = x.permute(0, 2, 1) # (batch, features, seq_len)
        x = self.conv1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        return self.fc2(x).squeeze()

def run_hybrid_cnn():
    print("Loading data...")
    train_df = pd.read_csv('data_processed/train.csv')
    test_df = pd.read_csv('data_processed/test.csv')
    train_df['timestamp'] = pd.to_datetime(train_df['timestamp'])
    test_df['timestamp'] = pd.to_datetime(test_df['timestamp'])
    train_df.set_index('timestamp', inplace=True)
    test_df.set_index('timestamp', inplace=True)
    
    # Sequence Data for CNN
    horizon = 24
    seq_length = 24
    X_train_seq, y_train_seq = prepare_sequence_data(train_df, horizon=horizon, seq_length=seq_length)
    X_test_seq, y_test_seq = prepare_sequence_data(test_df, horizon=horizon, seq_length=seq_length)
    
    # Tabular Data for Base XGBoost
    X_train_tab, y_train_tab = prepare_tabular_data(train_df, horizon=horizon)
    X_test_tab, y_test_tab = prepare_tabular_data(test_df, horizon=horizon)
    
    # Align shapes (Sequence cuts off first 23 rows)
    X_test_tab = X_test_tab[seq_length-1:]
    y_test_tab = y_test_tab[seq_length-1:]
    
    # Transform Target for CNN (TPT: y^3) to hunt peaks
    y_train_tpt = y_train_seq ** 3
    
    # PyTorch Tensors
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    X_train_t = torch.FloatTensor(X_train_seq).to(device)
    y_train_t = torch.FloatTensor(y_train_tpt).to(device)
    X_test_t = torch.FloatTensor(X_test_seq).to(device)
    
    num_features = X_train_seq.shape[2]
    model = PeakHunterCNN(num_features).to(device)
    
    # Use L2 penalty (weight_decay) to prevent overfitting
    optimizer = optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-4)
    criterion = nn.MSELoss()
    
    print("Training 1D-CNN on TPT data (Hunting Peaks)...")
    model.train()
    epochs = 150
    batch_size = 64
    for epoch in range(epochs):
        permutation = torch.randperm(X_train_t.size()[0])
        for i in range(0, X_train_t.size()[0], batch_size):
            indices = permutation[i:i+batch_size]
            batch_x, batch_y = X_train_t[indices], y_train_t[indices]
            
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
    
    print("Generating CNN predictions...")
    model.eval()
    with torch.no_grad():
        cnn_pred_tpt = model(X_test_t).cpu().numpy()
        
    # Inverse Transform TPT
    cnn_pred_tpt = np.sign(cnn_pred_tpt) * (np.abs(cnn_pred_tpt) ** (1/3))
    
    # Load Base XGBoost model
    xgb_base = joblib.load('code/models/xgb_model.pkl')
    xgb_pred_base = xgb_base.predict(X_test_tab)
    
    # HYBRID ROUTING (Base-Triggered)
    trigger_threshold = 0.55
    hybrid_pred = np.where(xgb_pred_base >= trigger_threshold, cnn_pred_tpt, xgb_pred_base)
    hybrid_pred = np.clip(hybrid_pred, 0.0, 1.0)
    
    rmse = np.sqrt(mean_squared_error(y_test_tab, hybrid_pred))
    mae = mean_absolute_error(y_test_tab, hybrid_pred)
    print(f"\n--- HYBRID CNN + XGBoost METRICS ---")
    print(f"RMSE: {rmse:.4f}, MAE: {mae:.4f}")
    
    # Plotting 7 Days
    os.makedirs('workspace/figures', exist_ok=True)
    actuals = y_test_tab[:168]
    hybrid_plot = hybrid_pred[:168]
    time_axis = np.arange(168)
    
    plt.figure(figsize=(15, 6))
    plt.plot(time_axis, actuals, label='Actual', color='black', linewidth=2)
    plt.plot(time_axis, hybrid_plot, label='Hybrid XGBoost + CNN', color='magenta', linestyle='--')
    plt.axhline(y=trigger_threshold, color='orange', linestyle=':', label='Base Trigger')
    plt.title('Hybrid Model: XGBoost (Base) + 1D-CNN (Peak Hunter)')
    plt.xlabel('Hours')
    plt.ylabel('Utilization Rate')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('workspace/figures/hybrid_cnn_xgboost.png', dpi=300)
    plt.close()
    
    print("Plot saved to workspace/figures/hybrid_cnn_xgboost.png")

if __name__ == "__main__":
    run_hybrid_cnn()
