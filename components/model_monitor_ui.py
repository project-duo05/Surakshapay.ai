import streamlit as st
from database.db import get_db
from database.models import ModelMetric
import pandas as pd
import plotly.express as px

def render_model_monitor_page():
    st.markdown("<h2 style='color: #0f52ba;'>Model Monitoring Dashboard</h2>", unsafe_allow_html=True)
    
    try:
        db = next(get_db())
        metrics = db.query(ModelMetric).order_by(ModelMetric.timestamp.asc()).all()
    except Exception as e:
        st.error(f"Failed to fetch model metrics from database: {e}")
        return
        
    if not metrics:
        st.info("No model metrics recorded yet. Metrics are generated after scheduled tests or retraining.")
        if st.button("Generate Dummy Metrics"):
            import random
            from datetime import datetime, timedelta
            for i in range(10):
                m = ModelMetric(
                    timestamp=datetime.utcnow() - timedelta(days=10-i),
                    accuracy=random.uniform(0.85, 0.95),
                    precision=random.uniform(0.80, 0.92),
                    recall=random.uniform(0.75, 0.89),
                    f1_score=random.uniform(0.78, 0.90),
                    fraud_detection_rate=random.uniform(0.70, 0.85),
                    data_drift_detected=random.choice([True, False, False, False])
                )
                db.add(m)
            db.commit()
            st.rerun()
        return

    df = pd.DataFrame([{
        "Time": m.timestamp,
        "Accuracy": m.accuracy,
        "Precision": m.precision,
        "Recall": m.recall,
        "F1": m.f1_score,
        "Detection Rate": m.fraud_detection_rate,
        "Drift": m.data_drift_detected
    } for m in metrics])
    
    col1, col2, col3, col4 = st.columns(4)
    latest = df.iloc[-1]
    col1.metric("Latest Accuracy", f"{latest['Accuracy']:.2%}")
    col2.metric("Latest F1 Score", f"{latest['F1']:.2%}")
    col3.metric("Detection Rate", f"{latest['Detection Rate']:.2%}")
    col4.metric("Data Drift", "Detected" if latest['Drift'] else "Stable", delta_color="inverse")
    
    st.markdown("### Metrics Over Time")
    fig = px.line(df, x="Time", y=["Accuracy", "Precision", "Recall", "F1"], 
                  title="Model Performance Metrics Trend")
    st.plotly_chart(fig, use_container_width=True)
