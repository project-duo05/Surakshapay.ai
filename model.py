from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
import numpy as np

class HybridFraudModel:
    """
    Hybrid Fraud Detection Model incorporating:
    1. Isolation Forest for unsupervised anomaly detection.
    2. Logistic Regression for supervised fraud probability.
    """
    def __init__(self, contamination=0.0017, use_supervised=True):
        self.anomaly_detector = IsolationForest(contamination=contamination, random_state=42, n_jobs=-1)
        self.use_supervised = use_supervised
        
        # Logistic regression with class weights to handle imbalanced dataset
        self.supervised_model = LogisticRegression(class_weight='balanced', max_iter=1000, C=0.1, random_state=42)
        
        self.is_fitted = False
        self.supervised_fitted = False
        self.optimal_threshold = 50.0  # Default to 50%
        
    def fit(self, X, y=None):
        self.anomaly_detector.fit(X)
        if self.use_supervised and y is not None and len(np.unique(y)) > 1:
            self.supervised_model.fit(X, y)
            self.supervised_fitted = True
            
            # Find optimal threshold using Precision-Recall Curve on training data
            probs = self.predict_probability(X) / 100.0
            precision, recall, thresholds = precision_recall_curve(y, probs)
            f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10) # Avoid div by 0
            best_idx = np.argmax(f1_scores)
            
            # Thresholds array is len(precision) - 1, so handle bound
            if best_idx < len(thresholds):
                self.optimal_threshold = thresholds[best_idx] * 100.0
            
        self.is_fitted = True
        
    def predict_anomaly(self, X):
        """
        Returns anomaly scores normalized strictly 0-100.
        Isolation forest decision_function: < 0 is anomaly, > 0 is normal.
        Lower values = more anomalous.
        """
        if not self.is_fitted:
            return np.zeros(len(X))
            
        # raw_scores: lower means more anomalous
        raw_scores = self.anomaly_detector.decision_function(X)
        
        # Invert so higher is more anomalous
        inverted_scores = -raw_scores
        
        # MinMaxScaler dynamically based on batch or assumed bounds
        # Typically max is ~0.5 and min is ~-0.5. 
        min_score = inverted_scores.min()
        max_score = inverted_scores.max()
        
        if max_score > min_score:
            norm_scores = (inverted_scores - min_score) / (max_score - min_score)
        else:
            norm_scores = np.zeros(len(inverted_scores))
            
        return norm_scores * 100.0
        
    def predict_probability(self, X):
        """Returns fraud probability 0-100 from supervised model."""
        if not self.supervised_fitted:
            return np.zeros(len(X))
            
        probs = self.supervised_model.predict_proba(X)[:, 1]
        return probs * 100.0
        
    def get_feature_importances(self, feature_cols):
        if self.supervised_fitted and hasattr(self.supervised_model, 'coef_'):
            coefs = np.abs(self.supervised_model.coef_[0])
            return list(zip(feature_cols, coefs))
        return []
