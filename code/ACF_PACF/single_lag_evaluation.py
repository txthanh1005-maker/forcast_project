import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def main():
    # Ensure directory exists
    os.makedirs('code/ACF_PACF', exist_ok=True)

    # 1. Read data
    df = pd.read_csv('EV_train.csv')
    target_series = df['utilization_rate']

    # 2. Plot ACF and PACF
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    plot_acf(target_series.dropna(), lags=100, ax=axes[0], title="Autocorrelation Function (ACF)")
    plot_pacf(target_series.dropna(), lags=100, ax=axes[1], title="Partial Autocorrelation Function (PACF)")
    plt.tight_layout()
    plt.savefig('code/ACF_PACF/acf_pacf.png', dpi=300)
    plt.close()

    # 3. Evaluate single lags from 1 to 24
    lags = range(1, 25)
    maes = []
    rmses = []

    for k in lags:
        # Create dataset for lag k
        df_lag = pd.DataFrame({'target': target_series})
        df_lag['lag_k'] = df_lag['target'].shift(k)
        
        # Drop NaN
        df_lag.dropna(inplace=True)
        
        # Split 80/20 train/test
        split_idx = int(len(df_lag) * 0.8)
        train_df = df_lag.iloc[:split_idx]
        test_df = df_lag.iloc[split_idx:]
        
        X_train = train_df[['lag_k']]
        y_train = train_df['target']
        X_test = test_df[['lag_k']]
        y_test = test_df['target']
        
        # Train LGBM default
        model = LGBMRegressor(verbosity=-1)
        model.fit(X_train, y_train)
        
        # Predict
        preds = model.predict(X_test)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        
        maes.append(mae)
        rmses.append(rmse)

    # 4. Plot Lag Evaluation
    plt.figure(figsize=(10, 6))
    plt.plot(lags, maes, marker='o', label='MAE', color='blue')
    plt.plot(lags, rmses, marker='s', label='RMSE', color='red')
    plt.title('Single Lag Evaluation (LightGBM)')
    plt.xlabel('Lag (k)')
    plt.ylabel('Error')
    plt.xticks(lags)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('code/ACF_PACF/lag_evaluation_chart.png', dpi=300)
    plt.close()

    print("Evaluation completed successfully.")

if __name__ == "__main__":
    main()
