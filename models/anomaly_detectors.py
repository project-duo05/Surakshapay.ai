from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import joblib
import os

class AnomalyDetector:
    def __init__(self, model_type='Isolation Forest', contamination=0.05):
        self.model_type = model_type
        self.contamination = contamination
        self.scaler = StandardScaler()
        self.model = self._get_model()
        
    def _get_model(self):
        if self.model_type == 'Isolation Forest':
            return IsolationForest(contamination=self.contamination, random_state=42, n_jobs=-1)
        elif self.model_type == 'One-Class SVM':
            return OneClassSVM(nu=self.contamination, kernel="rbf", gamma="scale")
        elif self.model_type == 'Local Outlier Factor':
            return LocalOutlierFactor(contamination=self.contamination, novelty=True, n_jobs=-1)
        elif self.model_type == 'Elliptic Envelope':
            return EllipticEnvelope(contamination=self.contamination, random_state=42)
        elif self.model_type == 'K-Means (Distance-Based)':
            return KMeans(n_clusters=3, random_state=42, n_init="auto")
        elif self.model_type == 'DBSCAN':
            return DBSCAN(eps=0.5, min_samples=5)
        elif self.model_type == 'PCA-Based Detection':
            return PCA(n_components=1) # Initial value, updated in fit
        elif self.model_type == 'Autoencoder (Deep Learning)':
            return MLPRegressor(hidden_layer_sizes=(16, 8, 16), activation='relu', random_state=42, max_iter=200)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
            
    def prepare_features(self, df, feature_cols):
        X = df[feature_cols].copy()
        X = pd.get_dummies(X, drop_first=True)
        # Ensure all columns are numeric
        X = X.select_dtypes(include=[np.number])
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled, X.columns
        
    def fit(self, X):
        self.train_X = X # Store for proximity-based prediction (DBSCAN)
        if self.model_type == 'PCA-Based Detection':
            self.model.n_components = max(1, int(X.shape[1] // 2))
            self.model.fit(X)
        elif self.model_type == 'Autoencoder (Deep Learning)':
            self.model.fit(X, X)
        else:
            self.model.fit(X)
        
    def predict(self, X):
        if self.model_type in ['Isolation Forest', 'One-Class SVM', 'Local Outlier Factor', 'Elliptic Envelope']:
            preds = self.model.predict(X)
            return np.where(preds == -1, 1, 0)
            
        elif self.model_type == 'DBSCAN':
            # Proximity fallback for DBSCAN
            from sklearn.neighbors import NearestNeighbors
            nn = NearestNeighbors(n_neighbors=1)
            nn.fit(self.train_X)
            distances, indices = nn.kneighbors(X)
            
            # If distance to nearest neighbor in training set is > eps, or if that neighbor was noise
            train_labels = self.model.labels_
            preds = []
            for i, dist in enumerate(distances):
                if dist[0] > self.model.eps:
                    preds.append(1) # Anomaly if too far from any cluster
                else:
                    label = train_labels[indices[i][0]]
                    preds.append(1 if label == -1 else 0)
            return np.array(preds)
            
        else:
            scores = self.score_samples(X)
            threshold = np.percentile(scores, 100 * (1 - self.contamination))
            return np.where(scores >= threshold, 1, 0)
        
    def score_samples(self, X):
        if hasattr(self.model, 'decision_function'):
            return self.model.decision_function(X)
        elif hasattr(self.model, 'score_samples'):
            return self.model.score_samples(X)
            
        elif self.model_type == 'K-Means (Distance-Based)':
            distances = self.model.transform(X)
            return np.min(distances, axis=1)
            
        elif self.model_type == 'PCA-Based Detection':
            X_pca = self.model.transform(X)
            X_inv = self.model.inverse_transform(X_pca)
            return np.mean(np.square(X - X_inv), axis=1)
            
        elif self.model_type == 'Autoencoder (Deep Learning)':
            X_pred = self.model.predict(X)
            return np.mean(np.square(X - X_pred), axis=1)
            
        elif self.model_type == 'DBSCAN':
            from sklearn.neighbors import NearestNeighbors
            nn = NearestNeighbors(n_neighbors=1)
            nn.fit(self.train_X)
            distances, _ = nn.kneighbors(X)
            return distances.flatten()
        else:
            return np.zeros(len(X))

    def save_model(self, filepath):
        """Saves the entire AnomalyDetector instance to a file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)
        
    @classmethod
    def load_model(cls, filepath):
        """Loads and returns an AnomalyDetector instance from a file."""
        return joblib.load(filepath)
        
    def get_feature_importances(self, feature_cols):
        """Returns feature importances if the underlying model supports it."""
        if self.model_type == 'Isolation Forest' and hasattr(self.model, 'feature_importances_'):
            return pd.DataFrame({
                'Feature': feature_cols,
                'Importance': self.model.feature_importances_
            }).sort_values(by='Importance', ascending=False)
        return None
