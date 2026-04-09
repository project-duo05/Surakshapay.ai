import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

import os
import joblib

def standardize_columns(df):
    """
    Normalizes column names to standard lowercase equivalents to handle varying datasets.
    """
    df.columns = [str(c).lower().replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]
    mapping = {
        'class': 'is_fraud',
        'label': 'is_fraud',
        'target': 'is_fraud',
        'time': 'timestamp',
        'date': 'timestamp',
        'datetime': 'timestamp'
    }
    for old_col, new_col in mapping.items():
        if old_col in df.columns and new_col not in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)
            
    # Ensure is_fraud is numeric
    if 'is_fraud' in df.columns:
        df['is_fraud'] = pd.to_numeric(df['is_fraud'], errors='coerce').fillna(0).astype(int)
        
    return df

class DataProcessor:
    """Class to hold scaler state and preprocess data."""
    def __init__(self):
        self.scaler = StandardScaler()
        
    def fit_transform(self, X):
        X_numeric = X.select_dtypes(include=[np.number])
        X_scaled = self.scaler.fit_transform(X_numeric)
        return pd.DataFrame(X_scaled, columns=X_numeric.columns, index=X.index)
        
    def transform(self, X):
        X_numeric = X.select_dtypes(include=[np.number])
        # Only scale columns that the scaler was fitted on
        cols_missing = set(self.scaler.feature_names_in_) - set(X_numeric.columns)
        for c in cols_missing:
            X_numeric[c] = 0.0 # Provide default 0 for missing features
            
        X_numeric = X_numeric[self.scaler.feature_names_in_]
        X_scaled = self.scaler.transform(X_numeric)
        return pd.DataFrame(X_scaled, columns=self.scaler.feature_names_in_, index=X.index)
        
    def save(self, path="models/scaler.pkl"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.scaler, path)
        
    def load(self, path="models/scaler.pkl"):
        if os.path.exists(path):
            self.scaler = joblib.load(path)
