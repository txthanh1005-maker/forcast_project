import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import os

# Đường dẫn file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE = os.path.join(BASE_DIR, 'EV_train.csv')
SAVE_CHART = os.path.join(BASE_DIR, 'code', 'ACF_PACF', 'combo_lag_evaluation_chart.png')

def main():
    # Load data
    df = pd.read_csv(DATA_FILE)
    
    # Giả sử cột dữ liệu cần quan tâm là 'utilization_rate'
    if 'utilization_rate' not in df.columns:
        raise ValueError("Không tìm thấy cột 'utilization_rate' trong file dữ liệu.")
        
    df = df[['utilization_rate']].copy()
    
    # Tạo tất cả các features lag từ 1 đến 24
    max_lag = 24
    for i in range(1, max_lag + 1):
        df[f'lag_{i}'] = df['utilization_rate'].shift(i)
        
    # Xóa 24 dòng đầu tiên để đảm bảo các tập train/test hoàn toàn giống nhau kích thước cho mọi combo
    df = df.dropna().reset_index(drop=True)
    
    # Định nghĩa các tổ hợp lag
    lag_combos = [
        [1],
        [1, 2],
        [1, 24],
        [1, 2, 24],
        [1, 2, 3],
        [1, 2, 4],
        [1, 2, 3, 4],
        [1, 2, 4, 24]
    ]
    
    # Chuẩn bị dữ liệu để lưu kết quả
    results = []
    
    # Chia train/test split 80/20 tuần tự
    split_idx = int(len(df) * 0.8)
    
    target_col = 'utilization_rate'
    y_train = df.loc[:split_idx-1, target_col]
    y_test = df.loc[split_idx:, target_col]
    
    for combo in lag_combos:
        combo_str = "{" + ", ".join(map(str, combo)) + "}"
        feature_cols = [f'lag_{i}' for i in combo]
        
        X_train = df.loc[:split_idx-1, feature_cols]
        X_test = df.loc[split_idx:, feature_cols]
        
        # Baseline model LightGBM
        model = lgb.LGBMRegressor(random_state=42)
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        
        results.append({
            'Combo': combo_str,
            'MAE': mae,
            'RMSE': rmse
        })
        
    results_df = pd.DataFrame(results)
    print(results_df)
    
    # Vẽ biểu đồ
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Tọa độ bar
    x = np.arange(len(results_df))
    width = 0.6
    
    # Function để thiết lập màu
    def get_colors(combo_list):
        return ['red' if c == "{1, 2, 4, 24}" else '#1f77b4' for c in combo_list]

    colors = get_colors(results_df['Combo'])
    
    # Vẽ MAE
    bars1 = ax1.bar(x, results_df['MAE'], width, color=colors)
    ax1.set_ylabel('MAE')
    ax1.set_title('Mean Absolute Error (MAE) by Lag Combination')
    ax1.set_xticks(x)
    ax1.set_xticklabels(results_df['Combo'], rotation=45, ha='right')
    
    # Gắn value lên bar
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.0001, round(yval, 4), ha='center', va='bottom', fontsize=9)

    # Vẽ RMSE
    bars2 = ax2.bar(x, results_df['RMSE'], width, color=colors)
    ax2.set_ylabel('RMSE')
    ax2.set_title('Root Mean Squared Error (RMSE) by Lag Combination')
    ax2.set_xticks(x)
    ax2.set_xticklabels(results_df['Combo'], rotation=45, ha='right')
    
    # Gắn value lên bar
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.0001, round(yval, 4), ha='center', va='bottom', fontsize=9)
        
    plt.tight_layout()
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(SAVE_CHART), exist_ok=True)
    plt.savefig(SAVE_CHART, dpi=300)
    print(f"Đã lưu biểu đồ vào {SAVE_CHART}")
    
if __name__ == "__main__":
    main()
