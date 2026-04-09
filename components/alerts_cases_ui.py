import streamlit as st
from database.db import get_db
from database.models import Alert, Case

def render_alerts_cases_page():
    st.markdown("<h2 style='color: #0f52ba;'>Alerts & Case Management</h2>", unsafe_allow_html=True)
    
    db = next(get_db())
    
    tabs = st.tabs(["Active Alerts", "Case Management", "Audit Logs"])
    
    with tabs[0]:
        st.subheader("High-Risk Alerts")
        alerts = db.query(Alert).filter(Alert.is_resolved == False).all()
        if not alerts:
            st.success("No active alerts at this time.")
        else:
            for alert in alerts:
                with st.expander(f"Alert ID: {alert.id} | Score: {alert.risk_score:.1f}"):
                    st.write(f"**Transaction ID:** {alert.transaction_id}")
                    st.write(f"**Message:** {alert.message}")
                    st.write(f"**Time:** {alert.timestamp}")
                    if st.button("Mark as Resolved", key=f"resolve_{alert.id}"):
                        alert.is_resolved = True
                        db.commit()
                        st.rerun()

    with tabs[1]:
        st.subheader("Case Management")
        cases = db.query(Case).all()
        if not cases:
            st.info("No cases currently tracked.")
        else:
            for case in cases:
                st.write(f"**Case ID {case.id}** - Transaction: {case.transaction_id} | Status: {case.status} | Label: {case.fraud_label}")

    with tabs[2]:
        st.subheader("Audit Logs")
        from database.models import AuditLog
        logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
        if logs:
            import pandas as pd
            df = pd.DataFrame([{
                "Time": l.timestamp,
                "Txn ID": l.transaction_id,
                "Decision": l.decision,
                "User": l.user_id,
                "Risk Score": l.risk_score,
                "Reason": l.reason
            } for l in logs])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No audit logs yet.")
