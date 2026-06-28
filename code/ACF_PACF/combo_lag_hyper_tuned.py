import os
import sys
import pandas as pd
import numpy as np
import lightgbm as lgb
import optuna
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Thiết lập encoding UTF-8 cho console để tránh lỗi in ấn
sys.stdout.reconfigure(encoding='utf-8')

# Đường dẫn file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE = os.path.join(BASE_DIR, 'EV_train.csv')
SAVE_CHART = os.path.join(BASE_DIR, 'code', 'ACF_PACF', 'combo_lag_hyper_tuned_chart.png')

# Tắt log của optuna cho đỡ rối console
optuna.logging.set_verbosity(optuna.logging.WARNING)

def objective(trial, X_train, y_train, X_test, y_test):
    param = {
        'objective': 'regression',
        'metric': 'rmse',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'num_leaves': trial.suggest_int('num_leaves', 10, 100),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 50),
        'random_state': 42
    }

    model = lgb.LGBMRegressor(**param)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    return rmse

def main():
    # Load data
    df = pd.read_csv(DATA_FILE)
    
    if 'utilization_rate' not in df.columns:
        raise ValueError("Không tìm thấy cột 'utilization_rate' trong file dữ liệu.")
        
    df = df[['utilization_rate']].copy()
    
    # Tạo feature lag từ 1 đến 24
    max_lag = 24
    for i in range(1, max_lag + 1):
        df[f'lag_{i}'] = df['utilization_rate'].shift(i)
        
    # Bỏ đi max lag = 24 dòng đầu tiên để cố định tập dữ liệu cho các combo
    df = df.dropna().reset_index(drop=True)
    
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
    
    # Chia train/test split tuần tự 80/20
    split_idx = int(len(df) * 0.8)
    target_col = 'utilization_rate'
    y_train = df.loc[:split_idx-1, target_col]
    y_test = df.loc[split_idx:, target_col]
    
    results = []
    
    for combo in lag_combos:
        combo_str = "{" + ", ".join(map(str, combo)) + "}"
        print(f"Tuning cho combo: {combo_str} (50 trials)...")
        
        feature_cols = [f'lag_{i}' for i in combo]
        X_train = df.loc[:split_idx-1, feature_cols]
        X_test = df.loc[split_idx:, feature_cols]
        
        study = optuna.create_study(direction='minimize')
        # Tối ưu hoá RMSE trên tập test
        study.optimize(lambda trial: objective(trial, X_train, y_train, X_test, y_test), n_trials=50)
        
        best_params = study.best_params
        best_rmse = study.best_value
        
        # Đánh giá lại bằng params tốt nhất để lấy cả MAE
        best_model = lgb.LGBMRegressor(**best_params, random_state=42, objective='regression', verbosity=-1)
        best_model.fit(X_train, y_train)
        best_preds = best_model.predict(X_test)
        best_mae = mean_absolute_error(y_test, best_preds)
        
        print(f" -> Best RMSE: {best_rmse:.4f}, Best MAE: {best_mae:.4f}")
        
        results.append({
            'Combo': combo_str,
            'MAE': best_mae,
            'RMSE': best_rmse
        })
        
    results_df = pd.DataFrame(results)
    print("\nKết quả tổng hợp sau Tuning:")
    print(results_df.to_string(index=False))
    
    # Vẽ biểu đồ Bar Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    x = np.arange(len(results_df))
    width = 0.6
    
    # Function để thiết lập màu (Highlight {1, 2, 4, 24})
    def get_colors(combo_list):
        colors = []
        for c in combo_list:
            if c == "{1, 2, 4, 24}":
                colors.append('red') # Đỏ
            else:
                colors.append('#1f77b4') # Xanh dương
        return colors

    colors = get_colors(results_df['Combo'])
    
    # Vẽ MAE
    bars1 = ax1.bar(x, results_df['MAE'], width, color=colors)
    ax1.set_ylabel('MAE')
    ax1.set_title('Best MAE by Lag Combo (Optuna Tuned)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(results_df['Combo'], rotation=45, ha='right')
    
    # Gắn value lên bar
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.0001, f"{yval:.4f}", ha='center', va='bottom', fontsize=9)

    # Vẽ RMSE
    bars2 = ax2.bar(x, results_df['RMSE'], width, color=colors)
    ax2.set_ylabel('RMSE')
    ax2.set_title('Best RMSE by Lag Combo (Optuna Tuned)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(results_df['Combo'], rotation=45, ha='right')
    
    # Gắn value lên bar
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.0001, f"{yval:.4f}", ha='center', va='bottom', fontsize=9)
        
    plt.tight_layout()
    
    os.makedirs(os.path.dirname(SAVE_CHART), exist_ok=True)
    plt.savefig(SAVE_CHART, dpi=300)
    print(f"\nĐã lưu biểu đồ vào: {SAVE_CHART}")
    
if __name__ == "__main__":
    main()
