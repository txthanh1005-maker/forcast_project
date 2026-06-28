import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt
import os
import sys

def main():
    try:
        print(str("Bat dau thuc thi script feature_selection_analysis.py"))
        
        # 1. Đọc data
        data_path = 'EV_train.csv'
        print(str("Doc du lieu tu: " + data_path))
        df = pd.read_csv(data_path)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # 2. Tạo lag features
        print(str("Tao cac dac trung lag..."))
        target_col = 'utilization_rate'
        lags = [1, 2, 4, 24]
        for lag in lags:
            df[f'lag_{lag}'] = df[target_col].shift(lag)
            
        # 3. Bỏ 24 dòng đầu
        df = df.iloc[24:].reset_index(drop=True)
        
        # Prepare categorical features
        cat_cols = ['weather_condition', 'local_event']
        for col in cat_cols:
            df[col] = df[col].astype('category')
            
        bool_cols = ['is_weekend', 'is_peak_hour']
        for col in bool_cols:
            df[col] = df[col].astype(int)
            
        # Select features
        features = [
            'hour_of_day', 'day_of_week', 'month', 'is_weekend', 'is_peak_hour',
            'temperature_f', 'precipitation_mm', 'weather_condition',
            'traffic_congestion_index', 'local_event', 'current_price',
            'gas_price_per_gallon', 'lag_1', 'lag_2', 'lag_4', 'lag_24'
        ]
        
        X = df[features]
        y = df[target_col]
        
        # 4. Tách Train/Test (80/20 tuần tự)
        print(str("Tach tap Train/Test (80/20)..."))
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 5. Huấn luyện mô hình LightGBM base
        print(str("Huan luyen mo hinh LGBMRegressor..."))
        model = lgb.LGBMRegressor(random_state=42)
        # Fix categorical_feature parameter handling
        model.fit(X_train, y_train, categorical_feature=cat_cols)
        
        print(str("Huan luyen xong. Trich xuat Feature Importance..."))
        
        # 6. SHAP / Feature importance
        save_dir = 'code/ACF_PACF'
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, 'feature_importance.png')
        
        try:
            import shap
            print(str("Su dung SHAP de ve Feature Importance..."))
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test)
            
            plt.figure(figsize=(10, 8))
            shap.summary_plot(shap_values, X_test, show=False)
            plt.title('SHAP Feature Importance')
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
            print(str("Da luu bieu do SHAP tai: " + save_path))
        except ImportError:
            print(str("Khong the import shap. Su dung plot_importance cua LightGBM..."))
            plt.figure(figsize=(10, 8))
            ax = lgb.plot_importance(model, max_num_features=20, importance_type='split', figsize=(10, 8))
            plt.title('LightGBM Feature Importance')
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
            print(str("Da luu bieu do LightGBM tai: " + save_path))
        except Exception as e:
            print(str("Co loi khi dung SHAP: " + str(e) + ". Chuyen sang LightGBM plot..."))
            plt.figure(figsize=(10, 8))
            ax = lgb.plot_importance(model, max_num_features=20, importance_type='split', figsize=(10, 8))
            plt.title('LightGBM Feature Importance')
            plt.tight_layout()
            plt.savefig(save_path)
            plt.close()
            print(str("Da luu bieu do LightGBM tai: " + save_path))
            
    except Exception as e:
        print(str("Loi he thong: " + str(e)))

if __name__ == "__main__":
    main()
