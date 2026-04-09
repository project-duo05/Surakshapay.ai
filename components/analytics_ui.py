import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from report_generator import ReportGenerator

def render_analytics_page():
    st.markdown('<div class="hero-banner" style="background: linear-gradient(135deg, #1e293b 0%, #0f52ba 100%);"><h1>Bank-Grade Analytics <span class="highlight" style="color: #FF9933;">Dashboard</span></h1></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b; margin-bottom: 40px; font-size: 1.1rem;'>Comprehensive Insights, Risk Distributions, and System Health</p>", unsafe_allow_html=True)

    # Gather data (from live engine if active, otherwise base raw dataset + inference)
    df = None
    if "live_logs" in st.session_state and not st.session_state.live_logs.empty:
        df = st.session_state.live_logs.copy()
    else:
        st.info("The Analytics Dashboard shows data aggregated from the Live Engine. Start the Live Decision Engine to populate real-time analytics.")
        return
        
    st.markdown("### 🎛️ Real-Time Snapshot")
    k1, k2, k3, k4 = st.columns(4)
    total_tx = len(df)
    fraud_df = df[df['Decision'] == 'Block Transaction']
    fraud_count = len(fraud_df)
    
    k1.metric("Processed Transactions", f"{total_tx:,}")
    k2.metric("Critical / Blocked", f"{fraud_count:,}", delta=f"{(fraud_count/max(1, total_tx))*100:.1f}%", delta_color="inverse")
    k3.metric("Avg System Risk Score", f"{df['Risk_Score'].mean():.1f}/100")
    
    high_user_df = df.groupby('User_ID')['Risk_Score'].mean().reset_index()
    if not high_user_df.empty:
        top_user = str(high_user_df.loc[high_user_df['Risk_Score'].idxmax(), 'User_ID'])
        k4.metric("Highest Risk Profile", top_user)
    else:
        k4.metric("Highest Risk Profile", "N/A")
        
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Risk Score Distribution")
        fig1 = px.histogram(df, x="Risk_Score", nbins=20, title="")
        fig1.add_vline(x=80, line_dash="dash", line_color="red", annotation_text="Block Threshold")
        fig1.add_vline(x=60, line_dash="dash", line_color="orange", annotation_text="Review Threshold")
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.markdown("#### Decision Breakdown (Fraud vs Normal)")
        decision_counts = df['Decision'].value_counts().reset_index()
        color_map = {'Approve Transaction': 'green', 'Ask OTP Verification': 'orange', 'Flag for Manual Review': 'darkorange', 'Block Transaction': 'red'}
        fig2 = px.pie(decision_counts, values='count', names='Decision', color='Decision', color_discrete_map=color_map, hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)
        
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### Transactions Over Time")
        # Add index as fake time proxy if exact time not recorded properly in live logs
        plot_df = df.copy()
        plot_df['Seq'] = range(len(plot_df))
        fig3 = px.line(plot_df, x="Seq", y="Risk_Score", color="Decision", color_discrete_map=color_map, markers=True, title="Risk Trajectory")
        st.plotly_chart(fig3, use_container_width=True)
        
    with c4:
        st.markdown("#### Amount vs Risk Scatter")
        if 'Amount' in df.columns:
            fig4 = px.scatter(df, x="Amount", y="Risk_Score", color="Decision", color_discrete_map=color_map, size="Amount", hover_data=["Transaction_ID", "User_ID"])
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Amount data unavailable.")
            
    st.markdown("#### System Heatmap (Sequential vs Risk Density)")
    fig5 = px.density_heatmap(plot_df, x="Seq", y="Risk_Score", nbinsx=20, nbinsy=20, color_continuous_scale="Viridis")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("#### Top High Risk Users")
        top_users = df.groupby('User_ID').agg({'Risk_Score': 'mean', 'Transaction_ID': 'count'}).reset_index()
        top_users.rename(columns={'Transaction_ID': 'Count'}, inplace=True)
        st.dataframe(top_users.nlargest(10, 'Risk_Score'), use_container_width=True, hide_index=True)
        
    with t2:
        st.markdown("#### Top High Risk Transactions")
        st.dataframe(df.nlargest(10, 'Risk_Score')[['Transaction_ID', 'User_ID', 'Amount', 'Risk_Score', 'Decision']], use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Export Compliance Reporting")
    
    col_dl1, col_dl2 = st.columns(2)
    csv_bytes = ReportGenerator.generate_csv(df)
    
    # Calculate simple dict of high risk users for report
    high_user_dict = dict(zip(top_users.nlargest(5, 'Risk_Score')['User_ID'], top_users.nlargest(5, 'Risk_Score')['Risk_Score']))
    
    # Attempt to grab F1 if we had labels in training
    f1 = None
    if "hybrid_model" in st.session_state and st.session_state.hybrid_model.supervised_fitted:
        f1 = "Enabled (See Training metrics for exact F1)"
        
    pdf_bytes = ReportGenerator.generate_pdf_summary(df, fraud_count, high_user_dict, total_tx, f1)

    with col_dl1:
        st.download_button("📥 Export CSV Dump", data=csv_bytes, file_name="surakshapay_compliance.csv", mime="text/csv", type="primary", use_container_width=True)
    with col_dl2:
        st.download_button("📄 Export Summary Report (TXT/MD)", data=pdf_bytes, file_name="surakshapay_analytics_report.txt", mime="text/plain", use_container_width=True)
