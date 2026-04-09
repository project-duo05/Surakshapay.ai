import streamlit as st

def kpi_card(title, value, color=None, key=None):
    style = f"style='color: {color};'" if color else ""
    st.markdown(f"""
    <div class="glass-card" style="text-align: center;">
        <div class="metric-label">{title}</div>
        <div class="metric-value" {style}>{value}</div>
    </div>
    """, unsafe_allow_html=True)

def fraud_alert_card(message):
    st.markdown(f"""
    <div class="glass-card fraud-glow" style="text-align: center; border-color: #ff3366;">
        <div class="metric-label" style="color: #ff3366;">🚨 Alert</div>
        <div class="metric-value" style="font-size: 1.5rem; color: #ffebf0;">{message}</div>
    </div>
    """, unsafe_allow_html=True)
