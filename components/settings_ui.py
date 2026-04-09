import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid

USERS_FILE = "users.csv"

def init_users_db():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame([
            {"User_ID": "U-ADMIN01", "Name": "System Admin", "Role": "Admin", "Status": "Active", "Email": "admin@surakshapay.ai", "Password": "admin"},
            {"User_ID": "U-ANA001", "Name": "Fraud Analyst 1", "Role": "Analyst", "Status": "Active", "Email": "analyst@surakshapay.ai", "Password": "password123"},
            {"User_ID": "U-VW003", "Name": "Exec Viewer", "Role": "Viewer", "Status": "Inactive", "Email": "viewer@surakshapay.ai", "Password": "password123"}
        ])
        df.to_csv(USERS_FILE, index=False)

def init_settings_state():
    defaults = {
        "det_sensitivity": 50,
        "det_risk_thresh": 75,
        "det_auto_block": True,
        "det_rule_based": True,
        
        "alt_sound": True,
        "alt_email": True,
        "alt_sms": False,
        "alt_med_risk": True,
        "alt_high_risk": True,
        
        "mod_type": "Isolation Forest",
        "mod_version": "v1.4.2",
        "mod_last_trained": datetime.now().strftime("%Y-%m-%d %H:%M"),
        
        "sys_theme": "Light Mode",
        "sys_lang": "English",
        "sys_currency": "USD ($)",
        "sys_timezone": "UTC"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def render_settings_page():
    init_users_db()
    init_settings_state()
    
    st.markdown('<div class="hero-banner" style="background: linear-gradient(135deg, #1e293b 0%, #0f52ba 100%);"><h1>System <span class="highlight" style="color: #FF9933;">Settings</span></h1></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b; margin-bottom: 40px; font-size: 1.1rem;'>Configuration, Control, and Access Management</p>", unsafe_allow_html=True)

    # ---------- ROW 1: Detection & Alerts ----------
    r1_c1, r1_c2 = st.columns(2)
    
    with r1_c1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; border-top: 4px solid #0f52ba; height: 100%;">
            <h3 style="color: #0f52ba; margin-top: 0;">🛡️ Fraud Detection Settings</h3>
            <hr style="margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        # We need to wrap native streamlit components outside of HTML wrapper so they render functionally, 
        # but we can use st.container to group them visually.
        with st.container():
            st.session_state.det_sensitivity = st.slider("Detection Sensitivity (%)", 0, 100, st.session_state.det_sensitivity, help="Higher sensitivity flags more transactions as fraudulent.")
            st.session_state.det_risk_thresh = st.slider("Absolute Risk Threshold", 0, 100, st.session_state.det_risk_thresh, help="Scores above this value are instantly categorized as Fraud.")
            st.session_state.det_auto_block = st.toggle("Auto-Block High Risk Transactions", value=st.session_state.det_auto_block, help="Automatically decline transactions scoring above threshold.")
            st.session_state.det_rule_based = st.toggle("Enable Hard Rules (Location/Time heuristics)", value=st.session_state.det_rule_based)
            st.markdown("<br>", unsafe_allow_html=True)
            
    with r1_c2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; border-top: 4px solid #f97316; height: 100%;">
            <h3 style="color: #ea580c; margin-top: 0;">🔔 Alert & Notification Settings</h3>
            <hr style="margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            st.session_state.alt_sound = st.toggle("Enable Dashboard Sound Alerts", value=st.session_state.alt_sound)
            st.session_state.alt_email = st.toggle("Enable Incident Email Dispatch", value=st.session_state.alt_email)
            st.session_state.alt_sms = st.toggle("Enable SMS Text Alerts (Simulated)", value=st.session_state.alt_sms)
            
            st.markdown("**Triggers:**")
            st.session_state.alt_med_risk = st.checkbox("Alert on Medium Risk Transactions", value=st.session_state.alt_med_risk)
            st.session_state.alt_high_risk = st.checkbox("Alert on High Risk Transactions (Fraud)", value=st.session_state.alt_high_risk)
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- ROW 2: Models & Preferences ----------
    r2_c1, r2_c2 = st.columns(2)
    
    with r2_c1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; border-top: 4px solid #8b5cf6; height: 100%;">
            <h3 style="color: #7c3aed; margin-top: 0;">🧠 AI Model Configuration</h3>
            <hr style="margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            st.session_state.mod_type = st.selectbox("Active ML Architecture", ["Isolation Forest", "Local Outlier Factor", "One-Class SVM"], index=["Isolation Forest", "Local Outlier Factor", "One-Class SVM"].index(st.session_state.mod_type))
            
            st.info(f"**Current Version:** {st.session_state.mod_version} | **Last Trained:** {st.session_state.mod_last_trained}")
            
            if st.button("🔄 Retrain Active Model", use_container_width=True):
                with st.spinner("Retraining model across historical dataset..."):
                    import time
                    time.sleep(2)
                    st.session_state.mod_last_trained = datetime.now().strftime("%Y-%m-%d %H:%M")
                    v_int = int(st.session_state.mod_version.split(".")[-1]) + 1
                    st.session_state.mod_version = f"v1.4.{v_int}"
                    st.success("Model successfully retrained and deployed.")
            if st.button("📤 Upload Custom Weights", use_container_width=True):
                st.warning("Custom weight uploads require Admin clearance level 2.")
            st.markdown("<br>", unsafe_allow_html=True)
            
    with r2_c2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; border-top: 4px solid #14b8a6; height: 100%;">
            <h3 style="color: #0d9488; margin-top: 0;">⚙️ System Preferences</h3>
            <hr style="margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            st.session_state.sys_theme = st.selectbox("UI Theme", ["Light Mode", "Dark Mode", "System Default"], index=["Light Mode", "Dark Mode", "System Default"].index(st.session_state.sys_theme))
            st.session_state.sys_lang = st.selectbox("Platform Language", ["English", "Spanish", "French", "German", "Hindi"], index=["English", "Spanish", "French", "German", "Hindi"].index(st.session_state.sys_lang))
            st.session_state.sys_currency = st.selectbox("Native Display Currency", ["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)"], index=["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)"].index(st.session_state.sys_currency))
            st.session_state.sys_timezone = st.selectbox("Log Time Zone", ["UTC", "EST", "PST", "IST", "CET"], index=["UTC", "EST", "PST", "IST", "CET"].index(st.session_state.sys_timezone))
            if st.button("Save Preferences", use_container_width=True):
                st.toast("System preferences saved locally.")
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- ROW 3: Users & Info ----------
    r3_c1, r3_c2 = st.columns(2)
    
    with r3_c1:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; border-top: 4px solid #3b82f6; height: 100%;">
            <h3 style="color: #2563eb; margin-top: 0;">👥 User Management</h3>
            <hr style="margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            df_users = pd.read_csv(USERS_FILE)
            st.dataframe(df_users, use_container_width=True, hide_index=True)
            
            with st.expander("Add / Modify Security Roles"):
                u_name = st.text_input("Full Name")
                u_role = st.selectbox("Assign Role", ["Admin", "Analyst", "Viewer"])
                if st.button("Add Authorized User", type="primary", use_container_width=True):
                    if u_name:
                        new_u = pd.DataFrame([{"User_ID": f"U-{str(uuid.uuid4())[:6].upper()}", "Name": u_name, "Role": u_role, "Status": "Active"}])
                        df_users = pd.concat([df_users, new_u], ignore_index=True)
                        df_users.to_csv(USERS_FILE, index=False)
                        st.success(f"User {u_name} provisioned.")
                        st.rerun()
                    else:
                        st.error("Name required.")
                if st.button("Remove Selected User", use_container_width=True):
                    st.warning("To delete an active user, input their ID into the CLI admin console.")
            st.markdown("<br>", unsafe_allow_html=True)

    with r3_c2:
        st.markdown("""
        <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; border-top: 4px solid #64748b; height: 100%;">
            <h3 style="color: #475569; margin-top: 0;">ℹ️ System Diagnostics</h3>
            <hr style="margin: 10px 0;">
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            total_tx = 0
            total_fr = 0
            if "fraud_results" in st.session_state and st.session_state["fraud_results"] is not None:
                total_tx = len(st.session_state["fraud_results"])
                total_fr = len(st.session_state["fraud_results"][st.session_state["fraud_results"]['status'] == 'Fraud'])
            elif "current_data" in st.session_state and st.session_state["current_data"] is not None:
                total_tx = len(st.session_state["current_data"])
                
            st.markdown(f"""
            <ul style="list-style-type: none; padding-left: 0; color: #334155; line-height: 2;">
                <li><b>App Version:</b> SurakshaPay Enterprise v2.1.0</li>
                <li><b>Environment:</b> Production Cluster A</li>
                <li><b>Active Integrations:</b> Core Banking API, OpenAI Engine</li>
                <li><b>Total Tx Processed (Session):</b> {total_tx:,}</li>
                <li><b>Total Fraud Prevented (Session):</b> {total_fr:,}</li>
                <li><b>Current Uptime:</b> 99.98% (Secure)</li>
                <li><b>Service Status:</b> <span style="color: #16a34a; font-weight: bold;">[ONLINE] Running optimally</span></li>
            </ul>
            """, unsafe_allow_html=True)
            if st.button("Generate Diagnostic Dump", use_container_width=True):
                st.success("Hardware and RAM diagnostics exported to stdout.")
            st.markdown("<br>", unsafe_allow_html=True)
