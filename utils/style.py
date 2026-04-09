import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* Formal Light Cards */
    .glass-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 20px;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Suraksha Pay AI Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #0f52ba 0%, #4eb5f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: 1px;
    }

    /* Hero Banner matching user image */
    .hero-banner {
        background-color: #08408b;
        border-radius: 12px;
        padding: 80px 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    }
    .hero-banner h1 {
        color: #ffffff !important;
        font-size: 4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .hero-banner .highlight {
        color: #5bc0de !important;
    }

    /* KPI Metric Values */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: #0f52ba; /* Formal Blue */
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 5px;
    }

    /* Red Glow for Fraud */
    .fraud-glow {
        box-shadow: 0 0 15px rgba(220, 38, 38, 0.3) !important;
        border: 1px solid rgba(220, 38, 38, 0.5) !important;
        background-color: #fef2f2 !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Top Header Layout Adjustments */
    .top-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 2px solid #f1f5f9;
        margin-bottom: 10px;
        background-color: white;
    }

    .top-header-logo {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .top-header-logo h1 {
        margin: 0;
        padding: 0;
        font-size: 2rem;
    }
    
    .top-header-actions {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    /* Custom Scrollbar for Light Theme */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9; 
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8; 
    }
    
    /* Base text adjustment - removing forced light colors */
    h1, h2, h3, p {
        color: #1e293b;
    }
    
    /* DataFrame Styling - Light Theme */
    .dataframe {
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-radius: 8px;
        overflow: hidden;
        width: 100%;
    }
    .dataframe thead tr {
        background-color: #f8fafc;
        color: #475569;
        text-align: left;
        border-bottom: 2px solid #e2e8f0;
    }
    .dataframe th, .dataframe td {
        padding: 12px 15px;
        color: #334155;
    }
    .dataframe tbody tr {
        border-bottom: 1px solid #e2e8f0;
        background-color: #ffffff;
    }
    .dataframe tbody tr:nth-of-type(even) {
        background-color: #f8fafc;
    }
    .dataframe tbody tr:last-of-type {
        border-bottom: 2px solid #0f52ba;
    }
    .dataframe tbody tr:hover {
        background-color: #f1f5f9;
    }
    
    /* SaaS Dashboard Redesign Styles */
    
    /* Step Labels */
    .step-label {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #0f52ba;
        margin-bottom: -5px;
    }
    
    /* Model Info Panel */
    .model-info-panel {
        background-color: #f8fafc;
        border-left: 4px solid #0f52ba;
        padding: 15px;
        border-radius: 6px;
        margin: 15px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .model-info-panel h4 {
        margin-top: 0;
        margin-bottom: 5px;
        font-size: 1rem;
        color: #1e293b;
    }
    
    .model-info-panel p {
        margin: 0;
        font-size: 0.9rem;
        color: #475569;
    }
    
    /* Enhance Streamlit Native Containers (Cards) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        padding: 1.5rem !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        margin-bottom: 20px !important;
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04) !important;
    }
    
    /* Full-width Gradient Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0f52ba 0%, #4eb5f1 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(15, 82, 186, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 15px -3px rgba(15, 82, 186, 0.4) !important;
        filter: brightness(1.1) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #475569 !important;
        font-weight: 600 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f8fafc !important;
        color: #0f52ba !important;
        border-color: #0f52ba !important;
    }
    </style>
    """, unsafe_allow_html=True)
