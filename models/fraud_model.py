from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

class FraudProbabilityModel:
    def __init__(self):
        self.model = LogisticRegression(class_weight="balanced", random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def fit(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
    def predict_proba(self, X):
        if not self.is_fitted:
            return np.zeros(len(X)) # Fallback if not trained
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]
