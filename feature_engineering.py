import pandas as pd
import numpy as np

def build_behavioral_features(df):
    """
    Creates derived behavioral features as per banking fraud detection standards.
    Requires: 'user_id', 'amount', 'timestamp' columns to exist.
    """
    if df.empty:
        return df

    # Work on a copy
    df_feat = df.copy()
    
    # Identify standard columns safely
    user_col = next((c for c in df_feat.columns if c.lower() in ['user_id', 'user', 'account', 'customer']), None)
    amt_col = next((c for c in df_feat.columns if c.lower() in ['amount', 'price', 'value', 'cost']), None)
    time_col = next((c for c in df_feat.columns if c.lower() in ['timestamp', 'time', 'date', 'datetime']), None)

    if not all([user_col, amt_col, time_col]):
        # Fallback if required columns are missing
        df_feat['night_transaction_flag'] = 0
        df_feat['high_risk_amount_flag'] = (df_feat.get(amt_col, pd.Series([0]*len(df_feat))) > 5000).astype(int)
        return df_feat

    # Ensure time is datetime
    df_feat['temp_time'] = pd.to_datetime(df_feat[time_col], errors='coerce')
    # If all NaT, just return
    if df_feat['temp_time'].isna().all():
        df_feat = df_feat.drop(columns=['temp_time'])
        return df_feat
        
    df_feat = df_feat.sort_values(by=[user_col, 'temp_time']).reset_index(drop=True)
    
    # 1. night_transaction_flag (12 AM - 5 AM)
    df_feat['hour'] = df_feat['temp_time'].dt.hour
    df_feat['night_transaction_flag'] = ((df_feat['hour'] >= 0) & (df_feat['hour'] < 6)).astype(int)
    
    # 2. Rolling window features (need index as datetime for rolling)
    df_feat = df_feat.set_index('temp_time')
    
    # We will use iter_tools or groupby rolling
    # avg_amount_24h, transaction_count_1h, transaction_count_24h per user
    grouped = df_feat.groupby(user_col)
    
    df_feat['transaction_count_1h'] = grouped.rolling('1h', min_periods=1)[amt_col].count().reset_index(level=0, drop=True)
    df_feat['transaction_count_24h'] = grouped.rolling('24h', min_periods=1)[amt_col].count().reset_index(level=0, drop=True)
    df_feat['avg_amount_24h'] = grouped.rolling('24h', min_periods=1)[amt_col].mean().reset_index(level=0, drop=True)
    
    # Velocity: transactions per minute (over last 1 hr to be stable)
    df_feat['velocity'] = df_feat['transaction_count_1h'] / 60.0
    
    # Restore index
    df_feat = df_feat.reset_index()
    
    # 3. amount_deviation_from_user_avg
    # overall historical mean per user
    df_feat['user_historical_avg'] = df_feat.groupby(user_col)[amt_col].transform(lambda x: x.expanding().mean())
    df_feat['amount_deviation_from_user_avg'] = df_feat[amt_col] - df_feat['user_historical_avg']
    
    # unusual_amount_flag (if amount is > 3 std devs from their expanding mean)
    df_feat['user_historical_std'] = df_feat.groupby(user_col)[amt_col].transform(lambda x: x.expanding().std().fillna(0))
    df_feat['unusual_amount_flag'] = np.where(
        (df_feat['user_historical_std'] > 0) & 
        (df_feat[amt_col] > (df_feat['user_historical_avg'] + 3 * df_feat['user_historical_std'])), 
        1, 0
    )
    
    # 4. high_risk_amount_flag (static rule > 5000 or top 5% overall)
    high_threshold = df_feat[amt_col].quantile(0.95) if len(df_feat) > 10 else 5000
    df_feat['high_risk_amount_flag'] = (df_feat[amt_col] > max(high_threshold, 2000)).astype(int)
    
    # 5. new_user_flag (if user has <= 3 transactions total historically)
    user_tx_counts = df_feat.groupby(user_col).cumcount() + 1
    df_feat['new_user_flag'] = (user_tx_counts <= 3).astype(int)

    # Clean up temp cols
    cols_to_drop = ['temp_time', 'hour', 'user_historical_avg', 'user_historical_std']
    df_feat = df_feat.drop(columns=[c for c in cols_to_drop if c in df_feat.columns])
    
    # Fill any NaNs created by rolling aggregations
    df_feat = df_feat.fillna(0)
    
    return df_feat

def live_feature_engineering(live_tx, df_history):
    """
    Applies the same feature engineering logic to a single new transaction based on historical context.
    live_tx is a dict or Series, df_history is the pandas DataFrame of past transactions.
    """
    # Simply append to history, run build_behavioral_features for that user, and return the last row
    user_col = next((c for c in df_history.columns if c.lower() in ['user_id', 'user', 'account', 'customer']), None)
    if not user_col:
        return pd.DataFrame([live_tx]) # Fallback
        
    uid = live_tx.get(user_col)
    
    user_history = df_history[df_history[user_col] == uid].copy()
    new_row = pd.DataFrame([live_tx])
    
    combined = pd.concat([user_history, new_row], ignore_index=True)
    engineered = build_behavioral_features(combined)
    return engineered.iloc[-1:]
