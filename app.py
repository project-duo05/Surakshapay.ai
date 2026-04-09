import streamlit as st
import streamlit.components.v1 as components
import time
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from utils.style import inject_custom_css
from utils.data_loader import generate_mock_data
from components.cards import kpi_card, fraud_alert_card
from components.charts import plot_transactions_over_time, plot_fraud_distribution, plot_amount_distribution
from models.anomaly_detectors import AnomalyDetector
from components.search import get_animated_search_html
from components.about_us_ui import get_about_us_html
from components.login_component import render_login_component
import base64
import os
import requests
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

@st.cache_data(ttl=3600)
def fetch_news():
    api_key = "9fbc5e84ce364ce68ccace772cd9c615"
    from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    url = f"https://newsapi.org/v2/everything?q=fraud OR cybersecurity OR fintech OR AI&from={from_date}&sortBy=publishedAt&apiKey={api_key}"
    try:
        req = requests.get(url, timeout=10)
        return req.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Page configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="SurakshaPayAI | Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS
inject_custom_css()

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'data' not in st.session_state:
    st.session_state.data = None
if 'model' not in st.session_state:
    st.session_state.model = None

def login_page():
    logo_base64 = get_base64_image("assets/logo.png")
    img_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""
    st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-top: 20px; margin-bottom: 5px;">
            <img src="{img_src}" style="max-height: 180px; object-fit: contain;">
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 30px;'>Production-Level Fraud Detection System</p>", unsafe_allow_html=True)
    
    # Renders our native custom component
    login_result = render_login_component(key="flip_login")
    if isinstance(login_result, dict):
        import pandas as pd
        import os
        import uuid
        USERS_FILE = "users.csv"
        
        # Ensure db exists
        if not os.path.exists(USERS_FILE):
            df_init = pd.DataFrame([
                {"User_ID": "U-ADMIN01", "Name": "System Admin", "Role": "Admin", "Status": "Active", "Email": "admin@surakshapay.ai", "Password": "admin"},
            ])
            df_init.to_csv(USERS_FILE, index=False)
            
        df_users = pd.read_csv(USERS_FILE)
        # Ensure we have Email and Password columns for older databases
        if "Email" not in df_users.columns: 
            df_users["Email"] = ["admin@surakshapay.ai"] + [""] * (len(df_users)-1)
        if "Password" not in df_users.columns: 
            df_users["Password"] = ["admin"] + [""] * (len(df_users)-1)
        
        action = login_result.get("action")
        email = login_result.get("email", "").strip()
        pwd = login_result.get("password", "")
        
        if action == "login":
            user_row = df_users[(df_users["Email"] == email) & (df_users["Password"] == pwd)]
            if not user_row.empty:
                st.session_state.authenticated = True
                st.session_state.current_user = user_row.iloc[0].to_dict()
                st.rerun()
            else:
                st.error("Invalid email or password. Please try again.")
                
        elif action == "register":
            name = login_result.get("name", "").strip()
            if email in df_users["Email"].values and email != "":
                st.error("Account already exists with this email!")
            else:
                new_u = pd.DataFrame([{
                    "User_ID": f"U-{str(uuid.uuid4())[:6].upper()}", 
                    "Name": name, 
                    "Role": "Viewer", 
                    "Status": "Active",
                    "Email": email,
                    "Password": pwd
                }])
                df_users = pd.concat([df_users, new_u], ignore_index=True)
                df_users.to_csv(USERS_FILE, index=False)
                st.session_state.authenticated = True
                st.session_state.current_user = new_u.iloc[0].to_dict()
                st.rerun()

if not st.session_state.authenticated:
    login_page()
else:
    # ---------------------------------------------------------
    # TOP HEADER
    # ---------------------------------------------------------
    st.markdown('<div class="top-header">', unsafe_allow_html=True)
    header_col1, header_col2, header_col3, header_col4 = st.columns([2, 3.5, 1.5, 1.0], vertical_alignment="center")
    
    with header_col1:
        logo_base64 = get_base64_image("assets/logo.png")
        img_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding-left: 10px;">
                <img src="{img_src}" style="max-height: 140px; max-width: 100%; object-fit: contain; transform-origin: left center;">
            </div>
        """, unsafe_allow_html=True)
        
    with header_col2:
        components.html(get_animated_search_html(), height=80)
        
    with header_col3:
        language = st.selectbox("Language", ["English", "Hindi", "Spanish", "French"], label_visibility="collapsed")
        
    with header_col4:
        # Profile placeholder
        st.write("") # spacing
        if st.button("👤 Profile"):
            st.session_state.current_page = "User Profile"
            st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # HORIZONTAL NAVIGATION MENU
    # ---------------------------------------------------------
    top_menu_selected = option_menu(
        menu_title=None,
        options=["HOME", "About Us", "Products", "News", "Customer Corner", "Contact Us"],
        icons=["house", "info-circle", "box", "newspaper", "people", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff", "border": "1px solid #e2e8f0", "border-radius": "8px", "margin-bottom": "20px"},
            "icon": {"color": "#0f52ba", "font-size": "16px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#f1f5f9", "color": "#1e293b", "padding": "10px"},
            "nav-link-selected": {"background-color": "#0f52ba", "color": "white", "font-weight": "bold"},
        }
    )

    # ---------------------------------------------------------
    # MAIN AREA
    # ---------------------------------------------------------
    # Detect navigation changes to clear profile view
    if "last_top_menu" not in st.session_state:
        st.session_state.last_top_menu = top_menu_selected
    if top_menu_selected != st.session_state.last_top_menu:
        st.session_state.current_page = top_menu_selected
        st.session_state.last_top_menu = top_menu_selected

    if st.session_state.get("current_page") == "User Profile":
        from components.profile_ui import render_profile_page
        render_profile_page()
    elif top_menu_selected == "HOME":
        # Create a layout that matches the 'Some Background' with a functional menu overlaid/on the right
        col_main, col_menu = st.columns([3, 1])
        
        with col_menu:
            st.markdown('<div class="glass-card" style="padding: 10px;">', unsafe_allow_html=True)
            st.markdown("<h4 style='text-align:center; color:#0f52ba; margin-top:10px;'>Main Dashboard</h4>", unsafe_allow_html=True)
            selected_func = option_menu(
                menu_title=None,
                options=["Overview", "Upload Data", "Train Model", "Live Detection", "Alerts & Cases", "Model Monitor", "Analytics", "Settings", "Log out"],
                icons=["clipboard-data", "cloud-upload", "cpu", "activity", "bell", "display", "bar-chart", "gear", "box-arrow-right"],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "#0f52ba", "font-size": "16px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"5px 0", "--hover-color": "#f8fafc", "color": "#475569", "border-radius": "5px"},
                    "nav-link-selected": {"background-color": "#f1f5f9", "color": "#0f52ba", "border-left": "4px solid #FF9933", "font-weight": "bold"},
                }
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if selected_func == "Log out":
                st.session_state.authenticated = False
                st.rerun()

        with col_main:
            # Render the functional page directly in the column
            # --- OVERVIEW ---
            if selected_func == "Overview":
                st.markdown('<div class="hero-banner"><h1>Let <span class="highlight">data</span> lead<br>the way.</h1></div>', unsafe_allow_html=True)
                st.markdown("<h2 style='color: #0f52ba;'>Overview Dashboard</h2>", unsafe_allow_html=True)
                
                if "data" not in st.session_state or st.session_state.data is None:
                    st.warning("Please navigate to 'Upload Data' to upload your dataset first.")
                    st.stop()
                    
                df = st.session_state.data
                fraud_col = 'is_fraud' if 'is_fraud' in df.columns else None
                fraud_df = df[df['is_fraud'] == 1] if fraud_col else pd.DataFrame()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    kpi_card("Total Transactions", f"{len(df):,}")
                with col2:
                    kpi_card("Fraud Detected", f"{len(fraud_df):,}" if fraud_col else "N/A")
                with col3:
                    if fraud_col and len(df) > 0:
                        fraud_pct = (len(fraud_df) / len(df)) * 100
                        kpi_card("Fraud Rate", f"{fraud_pct:.1f}%")
                    else:
                        kpi_card("Fraud Rate", "N/A")
                with col4:
                    if 'risk_score' in df.columns:
                        avg_risk = df['risk_score'].mean()
                        kpi_card("Avg Risk Score", f"{avg_risk:.1f}")
                    else:
                        kpi_card("Avg Risk Score", "N/A")
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                plot_col1, plot_col2 = st.columns([2, 1])
                with plot_col1:
                    if 'timestamp' in df.columns:
                        try:
                            # Ensure timestamp is parsed as datetime for resampling
                            df_time = df.copy()
                            df_time['timestamp'] = pd.to_datetime(df_time['timestamp'], errors='coerce')
                            df_time = df_time.dropna(subset=['timestamp'])
                            if not df_time.empty:
                                st.plotly_chart(plot_transactions_over_time(df_time), use_container_width=True)
                            else:
                                st.info("Could not parse 'timestamp' data for trend visualization.")
                        except:
                            st.info("Time series visualization not available for this dataset format.")
                    else:
                        st.info("No 'timestamp' column found. Time series visualization disabled.")
                with plot_col2:
                    if fraud_col:
                        st.plotly_chart(plot_fraud_distribution(df), use_container_width=True)
                    else:
                        st.info("No 'is_fraud' target available for distribution chart.")
                    
                st.markdown("### Recent Transactions")
                if 'timestamp' in df.columns:
                    recent_df = df.sort_values('timestamp', ascending=False).head(10)
                else:
                    recent_df = df.head(10)
                
                def highlight_fraud(val):
                    color = '#fee2e2' if val == 1 else ''
                    font_color = '#dc2626' if val == 1 else ''
                    return f'background-color: {color}; color: {font_color}'
                
                if fraud_col:
                    styled_df = recent_df.style.map(highlight_fraud, subset=['is_fraud'])
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                else:
                    st.dataframe(recent_df, use_container_width=True, hide_index=True)

            # --- UPLOAD DATA ---
            elif selected_func == "Upload Data":
                st.markdown("<h2 style='color: #0f52ba;'>Upload Data</h2>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
                
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                    except Exception as e:
                        st.error(f"Error reading CSV file. Please ensure it is a valid CSV: {e}")
                        st.stop()
                    # Normalize columns: lower case, replace spaces with underscores, remove parentheses
                    df.columns = [str(c).lower().replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]
                    
                    # --- SMART MAPPER ---
                    # Map standard aliases to internal names
                    mapping = {
                        'class': 'is_fraud',
                        'label': 'is_fraud',
                        'target': 'is_fraud',
                        'time': 'timestamp',
                        'date': 'timestamp',
                        'datetime': 'timestamp'
                    }
                    for old_col, new_col in mapping.items():
                        if old_col in df.columns and new_col not in df.columns:
                            df.rename(columns={old_col: new_col}, inplace=True)
                    
                    # Ensure is_fraud is numeric
                    if 'is_fraud' in df.columns:
                        df['is_fraud'] = pd.to_numeric(df['is_fraud'], errors='coerce').fillna(0).astype(int)
                    
                    # Clear any stale results to ensure a fresh experience
                    if "fraud_results" in st.session_state: del st.session_state["fraud_results"]
                    if "hybrid_model" in st.session_state: del st.session_state["hybrid_model"]
                    if "processor" in st.session_state: del st.session_state["processor"]
                    if "live_logs" in st.session_state: del st.session_state["live_logs"]
                    
                    st.session_state.data = df
                    st.session_state["current_data"] = df
                    st.success("Data uploaded and optimized! The platform is now tailored to your dataset schema.")
                    st.dataframe(df.head(10), use_container_width=True)
                elif st.session_state.data is not None:
                    st.info("Using currently active dataset.")
                    st.dataframe(st.session_state.data.head(10), use_container_width=True)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Generate Mock Data Instead"):
                        with st.spinner("Generating..."):
                            generated_data = generate_mock_data()
                            st.session_state.data = generated_data
                            st.session_state["current_data"] = generated_data
                        st.success("Mock data generated!")
                        st.rerun()

            # --- TRAIN MODEL ---
            elif selected_func == "Train Model":
                from components.train_model_ui import render_train_model_page
                render_train_model_page()

            # --- LIVE DETECTION ---
            elif selected_func == "Live Detection":
                from components.live_detection_ui import render_live_detection_page
                render_live_detection_page()

            # --- ALERTS & CASES ---
            elif selected_func == "Alerts & Cases":
                from components.alerts_cases_ui import render_alerts_cases_page
                render_alerts_cases_page()

            # --- MODEL MONITOR ---
            elif selected_func == "Model Monitor":
                from components.model_monitor_ui import render_model_monitor_page
                render_model_monitor_page()

            # --- ANALYTICS ---
            elif selected_func == "Analytics":
                from components.analytics_ui import render_analytics_page
                render_analytics_page()

            # --- SETTINGS ---
            elif selected_func == "Settings":
                from components.settings_ui import render_settings_page
                render_settings_page()

            
    elif top_menu_selected == "About Us":
        components.html(get_about_us_html(), height=1400, scrolling=True)
        
    elif top_menu_selected == "News":
        st.markdown('<div class="hero-banner"><h1>Latest <span class="highlight">Industry</span> News.</h1></div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; margin-bottom: 30px; text-align: center;'>Stay updated with real-time news on Cybersecurity, Fraud, and AI advancements.</p>", unsafe_allow_html=True)
        
        with st.spinner("Fetching latest articles..."):
            news_data = fetch_news()
            
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])[:12] # Show top 12
            if not articles:
                st.info("No articles found for the given topics right now.")
            else:
                for i in range(0, len(articles), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(articles):
                            article = articles[i + j]
                            with cols[j]:
                                img_url = article.get("urlToImage") or "https://via.placeholder.com/400x200?text=No+Image"
                                title = article.get("title", "No Title")
                                source = article.get("source", {}).get("name", "Unknown Source")
                                desc = article.get("description", "")
                                if desc and len(desc) > 120: desc = desc[:120] + "..."
                                link = article.get("url", "#")
                                
                                st.markdown(f'''
                                <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; height: 100%; display: flex; flex-direction: column; margin-bottom: 20px; transition: transform 0.2s;">
                                    <div style="height: 150px; overflow: hidden; background: #f8fafc;">
                                        <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src='https://via.placeholder.com/400x200?text=No+Image'">
                                    </div>
                                    <div style="padding: 20px; flex-grow: 1; display: flex; flex-direction: column;">
                                        <span style="color: #0f52ba; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">{source}</span>
                                        <h4 style="margin: 10px 0; font-size: 1.1rem; color: #1e293b; line-height: 1.4;">{title}</h4>
                                        <p style="color: #64748b; font-size: 0.95rem; flex-grow: 1; margin-bottom: 20px;">{desc}</p>
                                        <a href="{link}" target="_blank" style="display: inline-block; width: 100%; color: #0f52ba; font-weight: 600; text-decoration: none; border: 2px solid #0f52ba; padding: 10px 15px; border-radius: 8px; text-align: center; transition: all 0.2s;">Read Full Article</a>
                                    </div>
                                </div>
                                ''', unsafe_allow_html=True)
                                
        elif news_data.get("status") == "error" and "rateLimited" in news_data.get("code", ""):
            st.warning("NewsAPI rate limit reached. Please try again later.")
        else:
            st.error(f"Failed to fetch news: {news_data.get('message', 'Unknown Error')}")

    elif top_menu_selected == "Products":
        from components.products_ui import render_products_page
        render_products_page()
        
    elif top_menu_selected == "Customer Corner":
        from components.customer_corner_ui import render_customer_corner_page
        render_customer_corner_page()
        
    elif top_menu_selected == "Contact Us":
        from components.contact_us_ui import render_contact_us_page
        render_contact_us_page()
        
    elif top_menu_selected == "Live Detection (Standalone)":
        from components.live_detection_ui import render_live_detection_page
        render_live_detection_page()
        
    else:
        # For HOME alternatives like Products, News, etc.
        st.markdown(f'<div class="glass-card" style="text-align:center; padding: 100px; min-height: 60vh;"><h2 style="color: #0f52ba;">{top_menu_selected}</h2><p style="color: #64748b;">This section is under construction.</p></div>', unsafe_allow_html=True)

