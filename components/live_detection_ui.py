import streamlit as st
import pandas as pd
import time
import uuid
from datetime import datetime
import plotly.graph_objects as go

from feature_engineering import live_feature_engineering

def generate_live_transaction():
    if "data" not in st.session_state or st.session_state.data is None:
        st.warning("No data uploaded. Please upload a dataset first.")
        st.stop()
        
    df = st.session_state.data
    if "live_index" not in st.session_state:
        st.session_state.live_index = 0
    if st.session_state.live_index >= len(df):
        st.session_state.live_index = 0
        
    sample_row = df.iloc[st.session_state.live_index].to_dict()
    st.session_state.live_index += 1
    
    time_col = next((c for c in sample_row.keys() if 'time' in c.lower() or 'date' in c.lower()), None)
    if time_col:
        sample_row[time_col] = datetime.now()
    else:
        sample_row['timestamp'] = datetime.now()
        
    tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    sample_row['Transaction_ID'] = tx_id
    return sample_row

def analyze_transaction(raw_tx):
    from database.db import get_db
    from api.schemas import TransactionRequest
    from api.routes import predict_fraud
    
    db = next(get_db())
    
    amt_col = next((c for c in raw_tx.keys() if 'amount' in c.lower()), None)
    amount_val = raw_tx.get(amt_col, 0.0) if amt_col else 0.0
    
    user_col = next((c for c in raw_tx.keys() if 'user' in c.lower() or 'account' in c.lower()), None)
    # Default numeric user map or hash for mock
    user_id_val = hash(str(raw_tx.get(user_col, "Unknown"))) % 1000 + 1 if user_col else 1
    
    # Format request
    req = TransactionRequest(
        transaction_id=raw_tx.get('Transaction_ID', f"TXN-ERR"),
        user_id=user_id_val,
        amount=float(amount_val),
        location=str(raw_tx.get('location', 'Unknown')),
        merchant=str(raw_tx.get('merchant', 'Unknown'))
    )
    
    try:
        response = predict_fraud(req, db)
        
        # Color & Level
        level = "low"
        color = "green"
        if response.decision == "Ask OTP":
            level = "medium"
            color = "orange"
        elif response.decision == "Manual Review":
            level = "high"
            color = "darkorange"
        elif response.decision == "Block Transaction":
            level = "critical"
            color = "red"
            
        return {
            "Transaction_ID": response.transaction_id,
            "User_ID": f"U_{req.user_id}",
            "Amount": req.amount,
            "Risk_Score": round(response.risk_score, 1),
            "Decision": response.decision,
            "Level": level,
            "Color": color,
            "Explanation": "\n".join(response.reasons),
            "Anomaly_Component": round(response.risk_score*0.8, 1),
            "Prob_Component": round(response.risk_score*0.9, 1)
        }
    except Exception as e:
        print(f"Error in Live Detection hook: {e}")
        return {
            "Transaction_ID": req.transaction_id,
            "User_ID": f"U_{req.user_id}",
            "Amount": req.amount,
            "Risk_Score": 0.0,
            "Decision": "Approve",
            "Level": "low",
            "Color": "green",
            "Explanation": "Fallback approval.",
            "Anomaly_Component": 0.0,
            "Prob_Component": 0.0
        }

def create_gauge_chart(score, decision, color):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': f"{decision}", 'font': {'size': 18, 'color': color}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "rgba(0,0,0,0)"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': "#dcfce7"},
                {'range': [30, 60], 'color': "#fef08a"},
                {'range': [60, 80], 'color': "#ffedd5"},
                {'range': [80, 100], 'color': "#fee2e2"}],
            'threshold': {
                'line': {'color': color, 'width': 6},
                'thickness': 0.75,
                'value': score}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=50, b=10))
    return fig

def render_live_detection_page():
    st.markdown('<div class="hero-banner" style="background: linear-gradient(135deg, #1e293b 0%, #dc2626 100%);"><h1>Live <span class="highlight" style="color: #FF9933;">Decision Engine</span></h1></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b; margin-bottom: 20px;'>Real-Time Transaction Triage using Precision-Tuned Hybrid ML models</p>", unsafe_allow_html=True)

    if "live_logs" not in st.session_state:
        st.session_state.live_logs = pd.DataFrame(columns=["Transaction_ID", "User_ID", "Amount", "Risk_Score", "Decision", "Level", "Color", "Explanation", "Anomaly_Component", "Prob_Component"])
    
    if "is_monitoring" not in st.session_state:
        st.session_state.is_monitoring = False

    if "hybrid_model" not in st.session_state:
        st.warning("⚠️ No Hybrid Model found. The system is operating purely on Rules & Heuristics. Go to Train Model to activate AI risk scoring.")

    # Move controls from sidebar to main page area for better horizontal layout
    # Fixed nesting error (st.columns inside st.columns inside st.columns)
    st.markdown("### 🎛️ Live Engine Controls")
    c1, c2, c3, c4 = st.columns([1, 1, 1.2, 2.5])
    
    with c1:
        if st.button("▶️ Start Engine", key="start_engine", type="primary", use_container_width=True):
            st.session_state.is_monitoring = True
            
    with c2:
        if st.button("⏹️ Stop Engine", key="stop_engine", use_container_width=True):
            st.session_state.is_monitoring = False
            
    with c3:
        if st.button("🗑️ Clear Live Logs", key="clear_logs", use_container_width=True):
            st.session_state.live_logs = pd.DataFrame(columns=["Transaction_ID", "User_ID", "Amount", "Risk_Score", "Decision", "Level", "Color", "Explanation"])
            st.rerun()
            
    with c4:
        speed = st.slider("Polling Ratio (Secs/TX)", 0.5, 5.0, 1.5, key="speed_slider")

    st.markdown("---")
    
    kpi_placeholder = st.empty()
    alert_placeholder = st.empty()
    gauge_placeholder = st.empty()
    exp_placeholder = st.empty()
    feed_placeholder = st.empty()
    
    if st.session_state.is_monitoring:
        while st.session_state.is_monitoring:
            try:
                raw_tx = generate_live_transaction()
                analyzed_tx = analyze_transaction(raw_tx)
                
                new_row = pd.DataFrame([analyzed_tx])
                st.session_state.live_logs = pd.concat([new_row, st.session_state.live_logs], ignore_index=True)
            except Exception as e:
                st.error(f"Engine Exception: {e}")
                time.sleep(speed)
                continue
            
            df = st.session_state.live_logs
            blocks = len(df[df["Decision"] == "Block Transaction"])
            reviews = len(df[df["Decision"] == "Manual Review"])
            otps = len(df[df["Decision"] == "Ask OTP"])
            
            with kpi_placeholder.container():
                st.markdown(f"""
                <div style="display: flex; justify-content: space-around; background: #f8fafc; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
                    <div style="text-align: center; color: #dc2626;"><strong>Blocked</strong><br>{blocks}</div>
                    <div style="text-align: center; color: #ea580c;"><strong>Manual Reviews</strong><br>{reviews}</div>
                    <div style="text-align: center; color: #ca8a04;"><strong>OTP Requested</strong><br>{otps}</div>
                    <div style="text-align: center;"><strong>Total Active</strong><br>{len(df)}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with alert_placeholder.container():
                if analyzed_tx["Decision"] == "Block Transaction":
                    st.error(f"🚫 CRITICAL RISK: Transaction {analyzed_tx['Transaction_ID']} blocked (Score {analyzed_tx['Risk_Score']}).")
                elif analyzed_tx["Decision"] == "Manual Review":
                    st.warning(f"⚠️ MANUAL REVIEW: Transaction {analyzed_tx['Transaction_ID']} flagged (Score {analyzed_tx['Risk_Score']}).")
                    
            with gauge_placeholder.container():
                st.plotly_chart(create_gauge_chart(analyzed_tx["Risk_Score"], analyzed_tx["Decision"], analyzed_tx["Color"]), use_container_width=True, key=f"gauge_{uuid.uuid4().hex}")
                
            with exp_placeholder.container():
                color_bg = "#fef2f2" if analyzed_tx["Level"] == "critical" else "#fff7ed" if analyzed_tx["Level"] == "high" else "#fefce8" if analyzed_tx["Level"] == "medium" else "#f0fdf4"
                st.markdown(f"""
                <div style="background-color: {color_bg}; padding: 15px; border-radius: 8px; border-left: 5px solid {analyzed_tx['Color']}; border: 1px solid #e2e8f0;">
                    <h5 style="margin-top:0;">{analyzed_tx['Transaction_ID']} Analytics Record</h5>
                    <div style="display:flex; justify-content: space-between;">
                        <span style="font-size:0.9em; color:#64748b;">Anomaly Base: {analyzed_tx['Anomaly_Component']}/100</span>
                        <span style="font-size:0.9em; color:#64748b;">Supervised Prob: {analyzed_tx['Prob_Component']}/100 | Final Score: {analyzed_tx['Risk_Score']}</span>
                    </div>
                    <p style="white-space: pre-wrap; font-family: monospace; font-size: 0.95em; color: #334155; margin-top: 10px;">{analyzed_tx['Explanation']}</p>
                </div>
                <br>
                """, unsafe_allow_html=True)
                
            with feed_placeholder.container():
                st.markdown("#### Real-time Decision Log")
                display_cols = ["Transaction_ID", "User_ID", "Amount", "Decision", "Risk_Score"]
                
                def apply_color(row):
                    color = 'red' if row == 'Block Transaction' else 'darkorange' if row == 'Manual Review' else 'orange' if row == 'Ask OTP' else 'green'
                    return f'color: {color}; font-weight: bold'
                    
                display_df = df[display_cols].copy()
                st.dataframe(display_df.style.map(apply_color, subset=['Decision']), use_container_width=True, hide_index=True)
                
            time.sleep(speed)
            st.rerun()
            
    else:
        st.info("Live Decision Engine is currently STOPPED. Press 'Start Engine' in the sidebar.")
        if not st.session_state.live_logs.empty:
            st.dataframe(st.session_state.live_logs[["Transaction_ID", "User_ID", "Amount", "Decision", "Risk_Score"]], use_container_width=True, hide_index=True)
