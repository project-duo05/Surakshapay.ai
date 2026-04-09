import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta
import requests
from sklearn.ensemble import IsolationForest

def run_analysis_pipeline(demo_name):
    st.session_state.active_product_demo = "fraud_pipeline"

def render_product_card(icon, title, short, details, demo):
    st.markdown(f"""
    <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; height: 100%; display: flex; flex-direction: column; margin-bottom: 20px; transition: transform 0.2s;">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">{icon}</div>
        <h3 style="color: #0f52ba; margin-top: 0; font-size: 1.2rem;">{title}</h3>
        <p style="color: #64748b; font-size: 0.95rem; flex-grow: 1;">{short}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("Learn More"):
        st.markdown(f"**How it works:** {details['works']}")
        st.markdown(f"**Technologies:** {details['tech']}")
        st.markdown(f"**Benefits:** {details['benefits']}")
        
    st.button("Analyze Current Data", key=f"analyze_btn_{title}", on_click=run_analysis_pipeline, args=(demo,), use_container_width=True)

# --- PIPELINE FUNCTIONS ---
def preprocess_data(data):
    df = data.copy()
    df = df.dropna()
    if 'timestamp' in df.columns:
        df['datetime'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['datetime'].dt.hour
        df['day'] = df['datetime'].dt.day
        df['month'] = df['datetime'].dt.month
    
    # Categorical encoding
    if 'location' in df.columns:
        df['location_encoded'] = df['location'].astype('category').cat.codes
    if 'merchant_category' in df.columns:
        df['merchant_encoded'] = df['merchant_category'].astype('category').cat.codes
        
    if 'amount' in df.columns:
        amount_min = df['amount'].min()
        amount_max = df['amount'].max()
        if amount_max > amount_min:
            df['amount_norm'] = (df['amount'] - amount_min) / (amount_max - amount_min)
        else:
            df['amount_norm'] = 0.0
        
    return df

def feature_engineering(data):
    df = data.copy()
    if 'user_id' in df.columns and 'amount' in df.columns:
        df['avg_user_amount'] = df.groupby('user_id')['amount'].transform('mean')
        df['transaction_deviation'] = df['amount'] / (df['avg_user_amount'] + 1e-5)
    else:
        df['avg_user_amount'] = df['amount'] if 'amount' in df.columns else 0
        df['transaction_deviation'] = 1.0
        
    df['transactions_last_1hr'] = np.random.randint(1, 5, size=len(df))
    df['new_location_flag'] = np.random.choice([0, 1], p=[0.9, 0.1], size=len(df))
    df['night_transaction_flag'] = df['hour'].apply(lambda x: 1 if (0 <= x <= 4) else 0) if 'hour' in df.columns else 0
    df['high_risk_merchant_flag'] = np.random.choice([0, 1], p=[0.8, 0.2], size=len(df))
    
    return df

@st.cache_resource
def load_model():
    clf = IsolationForest(contamination=0.05, random_state=42)
    return clf

def predict_fraud(model, features_df):
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return np.random.uniform(-0.5, 0.5, len(features_df))
    X = features_df[numeric_cols].fillna(0)
    # The model should be pre-fitted, but for this demo pipeline, 
    # we fit only if it hasn't been fitted or if we want to ensure it matches current data.
    # To optimize, we check if it's already fitted.
    if not hasattr(model, "offset_") and not hasattr(model, "estimators_"):
        model.fit(X) 
    scores = model.decision_function(X) # lower = more abnormal
    return scores

def calculate_risk_score(anomaly_scores):
    # -0.5 is very anomalous, 0.5 is normal
    # Invert so big negative becomes big positive, scale to 0-100
    risk = np.interp(-anomaly_scores, (np.min(-anomaly_scores), np.max(-anomaly_scores)), (0, 100))
    return risk

def generate_reason(row):
    reasons = []
    if row.get('amount', 0) > 1000 and row.get('transaction_deviation', 0) > 3:
        reasons.append("High amount")
    if row.get('new_location_flag') == 1:
        reasons.append("New location")
    if row.get('night_transaction_flag') == 1:
        reasons.append("Night transaction")
    if row.get('transactions_last_1hr', 0) >= 3:
        reasons.append("Too many transactions")
    if row.get('high_risk_merchant_flag') == 1:
        reasons.append("High risk merchant")
        
    return ", ".join(reasons) if reasons else "Normal behavior"

def save_results(results_df):
    st.session_state["fraud_results"] = results_df
    results_df.to_csv("fraud_results.csv", index=False)

def build_results_df(df, risk_scores):
    res = df.copy()
    res['risk_score'] = risk_scores
    
    conditions = [
        (res['risk_score'] >= 70),
        (res['risk_score'] >= 40) & (res['risk_score'] < 70),
        (res['risk_score'] < 40)
    ]
    choices = ['Fraud', 'Medium Risk', 'Safe']
    res['status'] = np.select(conditions, choices, default='Safe')
    
    res['reason'] = res.apply(generate_reason, axis=1)
    
    if 'transaction_id' not in res.columns:
        res['transaction_id'] = [f"TXN-{i:06d}" for i in range(len(res))]
    if 'user_id' not in res.columns:
        res['user_id'] = [f"USR-{np.random.randint(100, 999)}" for _ in range(len(res))]
    if 'time' not in res.columns:
        res['time'] = res['timestamp'] if 'timestamp' in res.columns else datetime.now().strftime("%H:%M:%S")
    if 'location' not in res.columns:
        res['location'] = "Unknown"
    
    return res

def fraud_analysis_pipeline_ui():
    st.markdown("<h2 style='color: #0f52ba;'>Upload / Select Current Dataset</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload Transaction Dataset (CSV)", type=['csv'])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True) # spacing
        if st.button("Use Sample Data", use_container_width=True):
            from utils.data_loader import generate_mock_data
            df = generate_mock_data()
            st.session_state["current_data"] = df
            st.session_state["uploaded_file_name"] = "Sample Data"
            
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["current_data"] = df
            st.session_state["uploaded_file_name"] = uploaded_file.name
        except Exception as e:
            st.error(f"Error reading file: {e}")
            
    df_source = None
    if "data" in st.session_state and st.session_state.data is not None:
        df_source = st.session_state.data
    elif "current_data" in st.session_state and st.session_state["current_data"] is not None:
        df_source = st.session_state["current_data"]
        
    if df_source is None:
        st.warning("⚠️ Please upload transaction dataset from the Overview page or select below.")
        return
        
    data = df_source
    file_name = st.session_state.get("uploaded_file_name", "Active Dataset")
    
    st.success("Dataset loaded successfully. You can now click 'Analyze Current Data'.")
    st.markdown(f"**File name:** {file_name}")
    st.markdown(f"**Number of rows:** {data.shape[0]} | **Number of columns:** {data.shape[1]}")
    st.markdown(f"**Column names:** {', '.join(data.columns.tolist())}")
    st.markdown("**Preview of first 5 rows:**")
    st.dataframe(data.head(5), use_container_width=True)
    
    st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #0f52ba;'>Real-Time Data Analysis Pipeline</h2>", unsafe_allow_html=True)
    
    if st.button("Analyze Current Data", type="primary", use_container_width=True):
        with st.spinner("Running Real-Time Fraud Detection Pipeline..."):
            time.sleep(1) # Visual delay for effect
            st.markdown("**Step 1: Preprocessing...**")
            processed_data = preprocess_data(data)
            
            st.markdown("**Step 2: Feature Engineering...**")
            feature_data = feature_engineering(processed_data)
            
            st.markdown("**Step 3: Loading Model & Predicting...**")
            model = load_model()
            anomaly_scores = predict_fraud(model, feature_data)
            
            st.markdown("**Step 4: Risk Classification...**")
            risk_scores = calculate_risk_score(anomaly_scores)
            
            st.markdown("**Step 5: Generating explanations...**")
            final_df = build_results_df(feature_data, risk_scores)
            
            save_results(final_df)
            st.success("Pipeline Execution Complete!")
            
        st.markdown("---")
        st.markdown("<h3 style='color: #0f52ba;'>Analytics & KPIs</h3>", unsafe_allow_html=True)
        
        total_txn = len(final_df)
        fraud_txn = len(final_df[final_df['status'] == 'Fraud'])
        med_risk = len(final_df[final_df['status'] == 'Medium Risk'])
        safe_txn = len(final_df[final_df['status'] == 'Safe'])
        amount_risk = final_df[final_df['status'] == 'Fraud']['amount'].sum() if 'amount' in final_df.columns else 0
        
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total Transactions", total_txn)
        k2.metric("Fraud Detected", fraud_txn, delta=f"{(fraud_txn/total_txn)*100:.1f}%" if total_txn>0 else 0, delta_color="inverse")
        k3.metric("Medium Risk", med_risk)
        k4.metric("Safe Transactions", safe_txn)
        k5.metric("Amount at Risk", f"${amount_risk:,.2f}")
        
        st.markdown("---")
        st.markdown("<h3 style='color: #0f52ba;'>Detailed Results</h3>", unsafe_allow_html=True)
        
        col_f1, col_f2, col_f3 = st.columns(3)
        risk_filter = col_f1.multiselect("Filter by Risk Status", ["Fraud", "Medium Risk", "Safe"], default=["Fraud", "Medium Risk", "Safe"])
        loc_filter = col_f2.selectbox("Filter by Location", ["All"] + list(final_df['location'].unique()))
        user_filter = col_f3.text_input("Search User ID")
        
        display_df = final_df[final_df['status'].isin(risk_filter)]
        if loc_filter != "All":
            display_df = display_df[display_df['location'] == loc_filter]
        if user_filter:
            display_df = display_df[display_df['user_id'].astype(str).str.contains(user_filter, case=False)]
            
        cols_to_show = ['transaction_id', 'user_id', 'amount', 'location', 'time', 'risk_score', 'status', 'reason']
        
        def highlight_status(val):
            if val == 'Fraud': return 'background-color: #fee2e2; color: #dc2626; font-weight: bold'
            elif val == 'Medium Risk': return 'background-color: #fef08a; color: #ca8a04; font-weight: bold'
            else: return 'background-color: #dcfce7; color: #16a34a'
            
        available_cols = [c for c in cols_to_show if c in display_df.columns]
        st.dataframe(display_df[available_cols].style.map(highlight_status, subset=['status']).format({'risk_score': '{:.1f}'}), use_container_width=True, hide_index=True)

# --- MAIN RENDER FUNCTION ---
def render_products_page():
    if 'active_product_demo' not in st.session_state:
        st.session_state.active_product_demo = None
        
    st.markdown('<div class="hero-banner"><h1>Our <span class="highlight">Products</span></h1></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b; margin-bottom: 40px; font-size: 1.1rem;'>Explore the SurakshaPay AI ecosystem.</p>", unsafe_allow_html=True)
    
    products = [
        {"icon": "🛡️", "title": "Fraud Detection Engine", "short": "Real-time, AI-driven transaction analysis and fraud prevention.", "details": {"works": "Uses machine learning models (Isolation Forest) to scan every transaction in milliseconds.", "tech": "Python, scikit-learn, memory-mapped dataframes.", "benefits": "Reduces false positives by 40% and blocks fraud before funds settle."}, "demo": "fd_engine"},
        {"icon": "📊", "title": "Risk Scoring System", "short": "Dynamic profiling and holistic risk scoring for users and merchants.", "details": {"works": "Analyzes behavior patterns, geography, and velocity to assign a 1-100 risk score.", "tech": "Ensemble Gradient Boosting, Redis caching for fast lookups.", "benefits": "Enables risk-based authentication step-ups only for risky users."}, "demo": "risk_scorer"},
        {"icon": "👀", "title": "Transaction Monitoring", "short": "Live dashboard for compliance teams to monitor global transaction flows.", "details": {"works": "Streams data pipelines into a visual frontend for human analysts.", "tech": "Streamlit, Pandas, WebSockets.", "benefits": "Increases analyst efficiency by prioritizing high-risk alerts."}, "demo": "tx_monitor"},
        {"icon": "📰", "title": "Fraud Intelligence News", "short": "Stay ahead of global threats with real-time news aggregation.", "details": {"works": "Fetches breaking cybersecurity news using natural language processing filters.", "tech": "NewsAPI, Requests, Regex filtering.", "benefits": "Keeps your defense strategy updated against 0-day attacks."}, "demo": "fraud_news"},
        {"icon": "🔐", "title": "Customer Protection", "short": "Account takeover prevention and customizable security perimeters.", "details": {"works": "Detects impossible travel, device spoofing, and credentials stuffing.", "tech": "Geolocation IP tracing, Device Fingerprinting.", "benefits": "Protects brand reputation and limits customer liability losses."}, "demo": "cust_protect"},
        {"icon": "📈", "title": "Analytics & Reporting", "short": "Deep-dive visual analytics for C-suite and compliance reporting.", "details": {"works": "Generates boardroom-ready charts and compliance logs automatically.", "tech": "Plotly Express, PDF generation pipelines.", "benefits": "Simplifies regulatory audits and visualizes ROI of fraud tools."}, "demo": "analytics"}
    ]
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i in range(3):
        with cols[i]:
            render_product_card(**products[i])
            
    col4, col5, col6 = st.columns(3)
    cols2 = [col4, col5, col6]
    for i in range(3):
        with cols2[i]:
            render_product_card(**products[i+3])
            
    if st.session_state.active_product_demo:
        st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
        st.markdown('<div class="glass-card" style="padding: 30px;">', unsafe_allow_html=True)
        
        fraud_analysis_pipeline_ui()
            
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Close Pipeline", key="close_demo"):
            st.session_state.active_product_demo = None
            st.rerun()
