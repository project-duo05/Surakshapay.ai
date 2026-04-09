import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix, roc_curve, auc, precision_recall_curve

from feature_engineering import build_behavioral_features
from data_processing import DataProcessor, standardize_columns
from model import HybridFraudModel
from risk_engine import RiskEngine

def plot_confusion(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    fig = px.imshow(cm, text_auto=True, color_continuous_scale='Reds',
                    labels=dict(x="Predicted Label", y="True Label", color="Count"),
                    x=['Normal', 'Fraud'], y=['Normal', 'Fraud'], title="Confusion Matrix")
    return fig

def plot_roc(y_true, y_probs):
    fpr, tpr, _ = roc_curve(y_true, y_probs)
    roc_auc = auc(fpr, tpr)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, name=f"ROC AUC = {roc_auc:.2f}", mode='lines'))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name="Random", mode='lines', line=dict(dash='dash')))
    fig.update_layout(title="ROC Curve", xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
    return fig
    
def plot_pr_curve(y_true, y_probs, optimal_thresh):
    precision, recall, thresholds = precision_recall_curve(y_true, y_probs)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recall, y=precision, mode='lines', name='PR Curve', line=dict(color='purple')))
    # Add a marker for the optimal threshold
    # thresholds expects 0 to 1, optimal_thresh is 0 to 100
    idx = np.abs((thresholds * 100) - optimal_thresh).argmin() if len(thresholds) > 0 else 0
    if idx < len(precision):
        fig.add_trace(go.Scatter(x=[recall[idx]], y=[precision[idx]], mode='markers', marker=dict(color='red', size=10), name=f'Optimal F1 (Thresh={optimal_thresh:.1f}%)'))
    fig.update_layout(title="Precision-Recall Curve", xaxis_title="Recall", yaxis_title="Precision")
    return fig

def render_train_model_page():
    if st.session_state.data is None:
        st.warning("Please upload data or generate mock data in the Overview section first.")
        return

    st.markdown("<h2 style='color: #1e293b;'>Hybrid Model Tuning & Threshold Calibration</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin-bottom: 25px;'>Optimize precision by tuning dynamic thresholds via Precision-Recall curves. Calibrate percentiles for real-time risk decisons.</p>", unsafe_allow_html=True)

    df_raw = st.session_state.data.copy()
    
    with st.spinner("Standardizing and generating behavioral features..."):
        df_clean = standardize_columns(df_raw)
        df_feat = build_behavioral_features(df_clean)
        
    has_labels = 'is_fraud' in df_feat.columns
    valid_cols = [c for c in df_feat.select_dtypes(include=[np.number]).columns if c not in ['is_fraud']]

    with st.container(border=True):
        st.markdown("#### Model Configurations")
        contamination = st.number_input("Unsupervised Contamination", value=0.0017, format="%.4f", help="Set ~0.0017 for highly imbalanced fraud datasets.")
        use_supervised = st.checkbox("Train Supervised Component (Logistic Reg)", value=has_labels, disabled=not has_labels)
        
        feature_cols = st.multiselect("Select Features for Modeling", options=valid_cols, default=valid_cols[:10] if len(valid_cols) > 10 else valid_cols)
        
        if st.button("🚀 Train & Calibrate Hybrid Model", type="primary", use_container_width=True):
            if not feature_cols:
                st.error("Please select at least one feature.")
                return
                
            my_bar = st.progress(0, text="Scaling data...")
            processor = DataProcessor()
            X = df_feat[feature_cols].fillna(0)
            y = df_feat['is_fraud'].values if use_supervised else None
            
            X_scaled = processor.fit_transform(X)
            processor.save("models/scaler.pkl")
            
            my_bar.progress(40, text="Fitting Hybrid Model...")
            model = HybridFraudModel(contamination=contamination, use_supervised=use_supervised)
            model.fit(X_scaled, y)
            
            my_bar.progress(70, text="Calibrating Risk Engine thresholds...")
            anomaly_scores = model.predict_anomaly(X_scaled)
            fraud_probs = model.predict_probability(X_scaled)
            
            # Predict labels based on optimal PR threshold
            if use_supervised:
                final_preds = (fraud_probs >= model.optimal_threshold).astype(int)
            else:
                final_preds = model.get_raw_anomaly_labels(X_scaled)
                
            # Calculate total risk scores across dataset to find percentiles
            calculated_risks = []
            for i in range(len(df_feat)):
                row_dict = df_feat.iloc[i].to_dict()
                rule_val, _ = RiskEngine.evaluate_rules(row_dict)
                final_r = RiskEngine.calculate_risk_score(anomaly_scores[i], fraud_probs[i], rule_val)
                calculated_risks.append(final_r)
                
            # Compute percentiles
            p70 = np.percentile(calculated_risks, 70) if calculated_risks else 30
            p90 = np.percentile(calculated_risks, 90) if calculated_risks else 60
            p98 = np.percentile(calculated_risks, 98) if calculated_risks else 80
            
            st.session_state.hybrid_model = model
            st.session_state.processor = processor
            st.session_state.model_features = feature_cols
            st.session_state.risk_percentiles = {"p70": p70, "p90": p90, "p98": p98}
            
            my_bar.progress(100, text="Complete!")
            time.sleep(0.5)
            my_bar.empty()
            
            st.success("Hybrid Model optimized. Dynamic risk thresholds cached for Live Detection!")
            st.info(f"**Percentiles Discovered:** 70th (Approve): < {p70:.1f} | 90th (OTP): < {p90:.1f} | 98th (Review): < {p98:.1f} | 100th (Block): > {p98:.1f}")
            
            st.markdown("---")
            st.markdown("### Optimized Model Evaluation")
            
            metrics_col = st.columns(4)
            fraud_detected = sum(final_preds)
            metrics_col[0].metric("Anomalies/Fraud Flagged", f"{fraud_detected:,}")
            
            if use_supervised and y is not None:
                prec = precision_score(y, final_preds, zero_division=0)
                rec = recall_score(y, final_preds, zero_division=0)
                f1 = f1_score(y, final_preds, zero_division=0)
                metrics_col[1].metric("Precision (Target > 0.8)", f"{prec:.2f}", delta=f"{prec-0.8:.2f}" if prec != 0.8 else None)
                metrics_col[2].metric("Recall (Target > 0.8)", f"{rec:.2f}", delta=f"{rec-0.8:.2f}" if rec != 0.8 else None)
                metrics_col[3].metric("F1 Score (Target > 0.8)", f"{f1:.2f}", delta=f"{f1-0.8:.2f}" if f1 != 0.8 else None)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.plotly_chart(plot_confusion(y, final_preds), use_container_width=True)
                with c2:
                    st.plotly_chart(plot_roc(y, fraud_probs / 100.0), use_container_width=True)
                with c3:
                    st.plotly_chart(plot_pr_curve(y, fraud_probs / 100.0, model.optimal_threshold), use_container_width=True)
            else:
                st.info("Showing unsupervised summary. Upload labeled data to see PR Curves.")
                fig = px.histogram(x=anomaly_scores, nbins=50, title="Normalized Anomaly Score Distribution", labels={'x': "Score"})
                st.plotly_chart(fig, use_container_width=True)
                
            importances = model.get_feature_importances(feature_cols)
            if importances:
                st.markdown("#### Top Predictive Behaviors")
                imp_df = pd.DataFrame(importances, columns=['Feature', 'Importance']).sort_values(by='Importance', ascending=True).tail(10)
                fig_imp = px.bar(imp_df, x='Importance', y='Feature', orientation='h', title="Feature Importance Factor")
                st.plotly_chart(fig_imp, use_container_width=True)
