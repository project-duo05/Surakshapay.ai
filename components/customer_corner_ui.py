import streamlit as st
import pandas as pd
import numpy as np
import os
import random
import uuid
import re
from datetime import datetime
from sklearn.ensemble import IsolationForest
import time

COMPLAINTS_FILE = "complaints.csv"

def init_complaints_db():
    if not os.path.exists(COMPLAINTS_FILE):
        df = pd.DataFrame(columns=[
            "Complaint_ID", "Name", "Email", "Transaction_ID", 
            "Date", "Fraud_Type", "Description", "Status", "Timestamp"
        ])
        df.to_csv(COMPLAINTS_FILE, index=False)

def check_phishing_url(url):
    url = url.lower().strip()
    blacklist = ["example-phish.com", "free-money.net", "update-bank-acc.com", "login-verify-now.xyz"]
    for bad in blacklist:
        if bad in url:
            return "Phishing Detected (Blacklist)", "High Risk"
            
    suspicious_keywords = ["login", "verify", "update", "secure", "account", "free", "gift", "auth"]
    score = 0
    reasons = []
    
    ip_pattern = re.compile(r"http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    if ip_pattern.findall(url):
        score += 50
        reasons.append("Uses IP address instead of domain")
        
    if len(url) > 75:
        score += 20
        reasons.append("Unusually long URL")
        
    for word in suspicious_keywords:
        if word in url:
            score += 15
            reasons.append(f"Contains suspicious keyword: '{word}'")
            
    domain_part = url.replace("http://", "").replace("https://", "").split("/")[0]
    if domain_part.count(".") > 3:
        score += 20
        reasons.append("Irregular subdomain structure")
        
    if "-" in domain_part:
        score += 10
        reasons.append("Hyphenated domain identifier")
        
    if score >= 60:
        return f"Phishing/Malicious (Score: {score}) - {', '.join(reasons)}", "High Risk"
    elif score >= 25:
        return f"Suspicious (Score: {score}) - {', '.join(reasons)}", "Medium Risk"
    else:
        return "Safe (No immediate threats detected)", "Low Risk"

def calculate_isolation_risk(amount, loc, time_val, merchant):
    X_train = np.random.randn(100, 4) * 10 
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(X_train)
    
    loc_val = 10 if "International" in loc else (5 if "New" in loc else 1)
    hr = time_val.hour
    time_risk = 10 if (hr >= 0 and hr <= 4) else 1
    merchant_val = 15 if "Crypto" in merchant or "Jewelry" in merchant else 2
    
    X_test = np.array([[amount / 1000, loc_val, time_risk, merchant_val]])
    anomaly_score = clf.decision_function(X_test)[0] 
    
    raw_score = np.interp(-anomaly_score, (-0.2, 0.4), (0, 100))
    raw_score += (amount / 5000) * 20 + loc_val + time_risk * 2 + merchant_val
    return min(100, max(1, raw_score))


def render_customer_corner_page():
    init_complaints_db()
    
    st.markdown('<div class="hero-banner" style="background: linear-gradient(135deg, #1e293b 0%, #0f52ba 100%);"><h1>Customer <span class="highlight" style="color: #FF9933;">Corner</span></h1></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b; margin-bottom: 40px; font-size: 1.1rem;'>Protect. Report. Stay Secure.</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚨 Report Fraud", 
        "🔍 Check Transaction Risk", 
        "🛑 Card & Account Control", 
        "🛡️ Track & Phishing Check", 
        "💡 Security Center"
    ])
    
    with tab1:
        st.markdown("<h3 style='color: #0f52ba;'>Report Fraud / Unauthorized Transaction</h3>", unsafe_allow_html=True)
        with st.form("fraud_report_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Customer Name *")
                email = st.text_input("Email Address *")
                txn_id = st.text_input("Transaction ID (if applicable)")
            with col_b:
                fraud_type = st.selectbox("Fraud Type *", ["UPI Fraud", "Credit Card Fraud", "Phishing", "OTP Scam", "Net Banking Fraud", "Other"])
                date_val = st.date_input("Date of Transaction")
                
            desc = st.text_area("Description of Event *", help="Provide as many details as possible.")
            st.file_uploader("Upload Screenshot / Proof (Optional)", type=['png', 'jpg', 'jpeg', 'pdf'])
            
            submitted = st.form_submit_button("Submit Complaint", type="primary", use_container_width=True)
            
            if submitted:
                if not name or not email or not desc:
                    st.error("Please fill in all mandatory fields (*).")
                else:
                    complaint_id = f"SP{random.randint(10000, 99999)}"
                    new_complaint = pd.DataFrame([{
                        "Complaint_ID": complaint_id,
                        "Name": name,
                        "Email": email,
                        "Transaction_ID": txn_id,
                        "Date": date_val,
                        "Fraud_Type": fraud_type,
                        "Description": desc,
                        "Status": "Submitted",
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    new_complaint.to_csv(COMPLAINTS_FILE, mode='a', header=False, index=False)
                    st.success(f"✅ Your complaint has been registered securely. **Complaint ID: {complaint_id}**")
                    st.info("Our fraud investigation team will contact you within 24 hours.")

    with tab2:
        st.markdown("<h3 style='color: #0f52ba;'>Check Transaction Risk</h3>", unsafe_allow_html=True)
        st.write("Before finalizing a large or unusual payment, check its risk profile using our AI core.")
        
        with st.form("txn_risk_form"):
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                amount = st.number_input("Transaction Amount ($)", min_value=1.0, value=500.0)
                location = st.selectbox("Receiver Location Profile", ["Known / Local", "Domestic (New)", "International (Safe Zone)", "International (High Risk Zone)"])
            with r_col2:
                time_val = st.time_input("Execution Time", datetime.now().time())
                merchant = st.selectbox("Merchant / Category", ["Grocery & Supermarket", "Online Retail", "Electronics", "Crypto Exchange", "High-Risk Goods / Offshore"])
                
            check_risk = st.form_submit_button("Evaluate Risk", use_container_width=True)
            
            if check_risk:
                score = calculate_isolation_risk(amount, location, time_val, merchant)
                st.markdown("---")
                if score < 40:
                    st.success(f"## 🟢 LOW RISK (Score: {score:.1f}/100)")
                    st.markdown("**Recommendation:** Safe to proceed. Standard routing applied.")
                elif score < 75:
                    st.warning(f"## 🟡 MEDIUM RISK (Score: {score:.1f}/100)")
                    st.markdown("**Recommendation:** Requires additional OTP / 2FA verification before processing.")
                else:
                    st.error(f"## 🔴 HIGH RISK (Score: {score:.1f}/100)")
                    st.markdown("**Recommendation:** We recommend BLOCKING this transaction. It matches known fraud patterns.")

    with tab3:
        st.markdown("<h3 style='color: #0f52ba;'>Emergency Controls</h3>", unsafe_allow_html=True)
        st.write("If you suspect your account is compromised, immediately restrict access below.")
        
        if 'card_status' not in st.session_state:
            st.session_state['card_status'] = "Active"
        if 'account_status' not in st.session_state:
            st.session_state['account_status'] = "Active"
            
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 💳 Card Controls")
            st.info(f"Current Status: **{st.session_state['card_status']}**")
            if st.session_state['card_status'] == "Active":
                if st.button("🚫 Block My Card", type="primary", use_container_width=True):
                    st.session_state['card_status'] = "Blocked"
                    st.rerun()
            else:
                if st.button("✅ Unblock Card", use_container_width=True):
                    st.session_state['card_status'] = "Active"
                    st.rerun()
                    
            if st.session_state['card_status'] == "Blocked":
                st.error("🔒 Your card has been temporarily blocked for security. No new transactions will be approved.")
                
        with c2:
            st.markdown("#### 🏦 Account Controls")
            st.info(f"Current Status: **{st.session_state['account_status']}**")
            if st.session_state['account_status'] == "Active":
                if st.button("❄️ Freeze My Account", type="primary", use_container_width=True):
                    st.session_state['account_status'] = "Frozen"
                    st.rerun()
            else:
                if st.button("🔥 Unfreeze Account", use_container_width=True):
                    st.session_state['account_status'] = "Active"
                    st.rerun()
                    
            if st.session_state['account_status'] == "Frozen":
                st.error("🔒 Your entire account is frozen. All incoming/outgoing transfers are halted. Please visit a branch.")

    with tab4:
        st.markdown("<h3 style='color: #0f52ba;'>Complaint & Threat Tracker</h3>", unsafe_allow_html=True)
        
        cmp_col, phish_col = st.columns(2)
        with cmp_col:
            st.markdown("#### Track Complaint Status")
            search_id = st.text_input("Enter Complaint ID (e.g. SP12345)")
            if st.button("Check Status", use_container_width=True):
                if os.path.exists(COMPLAINTS_FILE):
                    df = pd.read_csv(COMPLAINTS_FILE)
                    match = df[df["Complaint_ID"] == search_id]
                    if not match.empty:
                        status = match.iloc[0]["Status"]
                        st.info(f"**Complaint {search_id}** is currently: **{status}**")
                        if status == "Submitted": st.progress(33)
                        elif status == "Under Review": st.progress(66)
                        else: st.progress(100)
                    else:
                        st.error("Complaint ID not found.")
                else:
                    st.error("No complaints database found.")
                    
        with phish_col:
            st.markdown("#### 🔗 Phishing URL Checker")
            st.write("Not sure if a link is safe? Enter it here.")
            url_to_check = st.text_input("Enter Website URL", placeholder="https://www.example.com")
            
            if st.button("Analyze Link for Phishing", type="primary", use_container_width=True):
                if url_to_check:
                    with st.spinner("Analyzing URL patterns and checking blacklists..."):
                        message, risk_level = check_phishing_url(url_to_check)
                        if risk_level == "High Risk":
                            st.error(f"🚨 **{message}**")
                            st.markdown("Do NOT click this link or enter any personal information.")
                        elif risk_level == "Medium Risk":
                            st.warning(f"⚠️ **{message}**")
                            st.markdown("Proceed with caution. Verify the sender before interacting.")
                        else:
                            st.success(f"✅ **{message}**")
                            st.markdown("The URL appears to match safe parameters.")
                else:
                    st.error("Please enter a URL first.")

    with tab5:
        st.markdown("<h3 style='color: #0f52ba;'>Fraud Awareness & Security Tips</h3>", unsafe_allow_html=True)
        
        tips_col, aware_col = st.columns(2)
        with tips_col:
            st.markdown("""
            #### 🛡️ Top Security Tips
            Our golden rules to keep your finances safe:
            
            1. **Never Share OTPs:** Bank representatives will *never* ask for your OTP.
            2. **Do not click unknown links:** Always type the banking URL directly into your browser.
            3. **Verify UPI / VPA Before Payment:** Check the receiver's name strictly before entering your PIN.
            4. **Avoid Public Wi-Fi:** Do not perform sensitive transactions on open or unencrypted networks.
            5. **Enable Alerts:** Ensure SMS and Email transaction alerts are active for all your accounts.
            """)
            
        with aware_col:
            st.markdown("#### ⚠️ Common Fraud Types")
            
            st.markdown("""
            * **🎣 Phishing Scam:** Emails or SMS looking like your bank, asking you to "update KYC".
            * **📲 UPI Collect Request Fraud:** Scammers send a "Collect Request" instead of sending you money. Entering your PIN deducts your balance!
            * **💳 Card Skimming:** Devices hidden on ATMs steal your magnetic stripe data.
            * **📱 Fake Loan Apps:** Unverified apps that steal contacts and extort money with high interest.
            * **⬛ QR Code Scam:** Fraudsters paste their own QR codes over legitimate shop codes.
            """)
