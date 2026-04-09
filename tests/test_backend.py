import sys
import os
import pandas as pd
import numpy as np

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.anomaly_detectors import AnomalyDetector
from utils.data_loader import generate_mock_data

def test_anomaly_detector():
    print("Starting backend verification tests...")
    
    # Generate mock data
    df = generate_mock_data(n_samples=200)
    features = ['amount', 'risk_score', 'velocity_score']
    
    model_types = [
        'Isolation Forest', 
        'One-Class SVM', 
        'Local Outlier Factor', 
        'Elliptic Envelope', 
        'K-Means (Distance-Based)', 
        'DBSCAN', 
        'PCA-Based Detection', 
        'Autoencoder (Deep Learning)'
    ]
    
    for mt in model_types:
        print(f"\nTesting model: {mt}")
        try:
            detector = AnomalyDetector(model_type=mt, contamination=0.1)
            X_scaled, final_cols = detector.prepare_features(df, features)
            
            print(f"  Fitting model...")
            detector.fit(X_scaled)
            
            print(f"  Predicting on training data...")
            preds_train = detector.predict(X_scaled)
            print(f"  Anomalies detected in train: {sum(preds_train)}")
            
            print(f"  Predicting on new data...")
            new_df = generate_mock_data(n_samples=50)
            X_new, _ = detector.prepare_features(new_df, features)
            preds_new = detector.predict(X_new)
            print(f"  Anomalies detected in new: {sum(preds_new)}")
            
            print(f"  Scoring samples...")
            scores = detector.score_samples(X_new)
            print(f"  Avg score: {np.mean(scores):.4f}")
            
            print(f"✅ {mt} passed!")
            
        except Exception as e:
            print(f"❌ {mt} FAILED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_anomaly_detector()
