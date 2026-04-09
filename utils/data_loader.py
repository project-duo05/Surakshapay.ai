import pandas as pd
import numpy as np

def generate_mock_data(n_samples=5000, fraud_ratio=0.04):
    np.random.seed(42)
    
    # Normal transactions
    n_normal = int(n_samples * (1 - fraud_ratio))
    normal_amounts = np.random.lognormal(mean=3.5, sigma=1.0, size=n_normal)
    normal_locations = np.random.choice(['US', 'UK', 'CA', 'AU', 'EU'], size=n_normal)
    normal_time = pd.date_range(end=pd.Timestamp.now(), periods=n_normal, freq='10T')
    
    # Fraud transactions (anomalies)
    n_fraud = n_samples - n_normal
    fraud_amounts = np.random.lognormal(mean=7.0, sigma=1.5, size=n_fraud) # Much higher amounts
    fraud_locations = np.random.choice(['US', 'UK', 'CA', 'AU', 'EU', 'NG', 'RU'], size=n_fraud)
    
    # Generate random times for fraud within the same range
    time_min, time_max = normal_time.min(), normal_time.max()
    fraud_time = pd.Series([time_min + pd.Timedelta(seconds=np.random.randint(0, int((time_max - time_min).total_seconds()))) for _ in range(n_fraud)])
    
    df_normal = pd.DataFrame({
        'timestamp': normal_time,
        'amount': normal_amounts,
        'location': normal_locations,
        'is_fraud': 0
    })
    
    df_fraud = pd.DataFrame({
        'timestamp': fraud_time,
        'amount': fraud_amounts,
        'location': fraud_locations,
        'is_fraud': 1
    })
    
    df = pd.concat([df_normal, df_fraud]).sort_values('timestamp').reset_index(drop=True)
    
    # Generate base categories
    df['merchant_category'] = np.random.choice(
        ['retail', 'travel', 'food', 'digital_goods', 'services'], 
        size=len(df), p=[0.4, 0.1, 0.2, 0.2, 0.1]
    )
    df['device_type'] = np.random.choice(['mobile', 'desktop', 'tablet'], size=len(df))
    df['transaction_type'] = np.random.choice(['online', 'in-store', 'wire_transfer', 'crypto'], size=len(df), p=[0.6, 0.3, 0.05, 0.05])
    
    # Base risk score
    df['risk_score'] = np.random.uniform(0, 100, size=len(df))
    df.loc[df['is_fraud'] == 1, 'risk_score'] = np.clip(np.random.normal(85, 10, size=n_fraud), 0, 100)
    df.loc[df['is_fraud'] == 0, 'risk_score'] = np.clip(np.random.normal(20, 15, size=n_normal), 0, 100)
    
    # ----------------------------------------------------
    # NEW EXPANDED FEATURES
    # ----------------------------------------------------
    
    # Time-Based
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['weekend_flag'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Add fraud tendency on weekends/nights (adjusting the existing random distribution slightly mathematically)
    
    # User Behavior (Randomized approximations)
    df['transaction_frequency'] = np.clip(np.random.normal(15, 8, size=len(df)), 1, 100)
    df.loc[df['is_fraud'] == 1, 'transaction_frequency'] = np.clip(np.random.normal(60, 20, size=n_fraud), 30, 150) # High freq attacks
    
    df['avg_transaction_amount'] = df['amount'].copy() * np.random.uniform(0.5, 2.0, size=len(df))
    df['device_change_count'] = np.random.poisson(0.5, size=len(df))
    df.loc[df['is_fraud'] == 1, 'device_change_count'] = np.random.poisson(3.0, size=n_fraud)
    
    df['location_change_frequency'] = np.random.poisson(0.2, size=len(df))
    df.loc[df['is_fraud'] == 1, 'location_change_frequency'] = np.random.poisson(2.5, size=n_fraud)
    
    # Advanced Features
    df['velocity_score'] = np.random.lognormal(mean=2, sigma=0.5, size=len(df))
    df.loc[df['is_fraud'] == 1, 'velocity_score'] = np.random.lognormal(mean=4, sigma=0.8, size=n_fraud)
    
    df['rolling_avg_amount'] = df['amount'] * np.random.uniform(0.8, 1.2, size=len(df))
    df['spending_deviation'] = df['amount'] - df['rolling_avg_amount']
    
    # Z-Score mathematically derived globally for simulation
    mean_amt = df['amount'].mean()
    std_amt = df['amount'].std()
    df['amount_zscore'] = (df['amount'] - mean_amt) / std_amt
    
    return df
