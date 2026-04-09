import streamlit as st
import pandas as pd
import numpy as np
import os
import random
import re
from datetime import datetime
import time

CONTACT_DB = "contact_requests.csv"

def init_contact_db():
    if not os.path.exists(CONTACT_DB):
        df = pd.DataFrame(columns=[
            "Ticket_ID", "Name", "Email", "Phone", 
            "Subject", "Message", "File_Name", "Date", "Status"
        ])
        df.to_csv(CONTACT_DB, index=False)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    # Basic phone validation: allows +, spaces, dashes, and digits. Must have at least 10 digits.
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10

def simulate_send_email(to_email, name, ticket_id):
    # Mocking smtplib for security and environment portability
    with st.spinner("Dispatching email notifications..."):
        time.sleep(1.5)
        st.info(f"📧 Simulated Email Sent to Support Team")
        st.info(f"📧 Simulated Confirmation Email Sent to {to_email}")

def render_contact_us_page():
    init_contact_db()
    
    st.markdown('<div class="hero-banner" style="background: linear-gradient(135deg, #0f52ba 0%, #1e293b 100%);"><h1>Contact <span class="highlight" style="color: #FF9933;">Us</span></h1></div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b; margin-bottom: 40px; font-size: 1.1rem;'>We're here to help you stay secure.</p>", unsafe_allow_html=True)
    
    tab_user, tab_admin = st.tabs(["💬 Submit a Request", "🛡️ Admin Console"])
    
    with tab_user:
        ui_col1, ui_col2 = st.columns([2, 1])
        
        with ui_col2:
            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; height: 100%;">
                <h3 style="color: #0f52ba; margin-top: 0; font-size: 1.3rem;">Get in Touch</h3>
                <hr>
                <p style="color: #475569; margin-bottom: 15px;"><strong>📧 Support Email:</strong><br>supportsurakshapay.ai@gmail.com</p>
                <p style="color: #475569; margin-bottom: 15px;"><strong>📍 Address:</strong><br>Cyber Hub, New Delhi, India</p>
                <p style="color: #475569; margin-bottom: 0px;"><strong>🕒 Working Hours:</strong><br>Mon–Fri, 9 AM – 6 PM (IST)</p>
            </div>
            """, unsafe_allow_html=True)
            
        with ui_col1:
            st.markdown("<h3 style='color: #0f52ba;'>How can we assist you?</h3>", unsafe_allow_html=True)
            
            with st.form("contact_form", clear_on_submit=False):
                name = st.text_input("Full Name *")
                
                c_email, c_phone = st.columns(2)
                with c_email:
                    email = st.text_input("Email Address *")
                with c_phone:
                    phone = st.text_input("Phone Number *", placeholder="+91 9876543210")
                    
                subject = st.selectbox("Subject *", ["Report Fraud", "Technical Issue", "General Inquiry", "Feedback", "Business Partnership"])
                message = st.text_area("Message / Details *", height=150)
                
                attached_file = st.file_uploader("Attach Context File (optional)", type=["png", "jpg", "jpeg", "pdf", "csv"])
                
                submit_btn = st.form_submit_button("Submit Request", type="primary", use_container_width=True)
                
                if submit_btn:
                    if not name or not email or not phone or not message:
                        st.error("Please fill in all mandatory fields (*).")
                    elif not is_valid_email(email):
                        st.error("Please enter a valid email address.")
                    elif not is_valid_phone(phone):
                        st.error("Please enter a valid phone number (minimum 10 digits).")
                    else:
                        # Success
                        ticket_id = f"SP-TKT-{random.randint(1000, 9999)}"
                        file_name = attached_file.name if attached_file else "None"
                        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        new_ticket = pd.DataFrame([{
                            "Ticket_ID": ticket_id,
                            "Name": name,
                            "Email": email,
                            "Phone": phone,
                            "Subject": subject,
                            "Message": message.replace("\n", " "),
                            "File_Name": file_name,
                            "Date": date_str,
                            "Status": "New"
                        }])
                        new_ticket.to_csv(CONTACT_DB, mode='a', header=False, index=False)
                        
                        st.success(f"✅ Your request has been submitted successfully. **Your Ticket ID is {ticket_id}**")
                        simulate_send_email(email, name, ticket_id)

    with tab_admin:
        st.markdown("<h3 style='color: #0f52ba;'>Support Tickets Admin Console</h3>", unsafe_allow_html=True)
        st.markdown("Monitor and adjust the status of incoming tickets.")
        
        if os.path.exists(CONTACT_DB):
            df = pd.read_csv(CONTACT_DB)
            if df.empty:
                st.info("No tickets in the system yet.")
            else:
                f_col1, f_col2 = st.columns(2)
                unique_statuses = ["All"] + list(df['Status'].unique())
                status_filter = f_col1.selectbox("Filter by Status", unique_statuses)
                
                if status_filter != "All":
                    display_df = df[df['Status'] == status_filter]
                else:
                    display_df = df
                    
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown("#### Update Ticket Status")
                
                u_col1, u_col2, u_col3 = st.columns(3)
                with u_col1:
                    ticket_to_update = st.selectbox("Select Ticket ID", df['Ticket_ID'].tolist())
                with u_col2:
                    new_status = st.selectbox("New Status", ["New", "In Progress", "Resolved"])
                with u_col3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Update Status", type="primary"):
                        row_idx = df.index[df['Ticket_ID'] == ticket_to_update].tolist()
                        if row_idx:
                            df.at[row_idx[0], 'Status'] = new_status
                            df.to_csv(CONTACT_DB, index=False)
                            st.success(f"Ticket {ticket_to_update} updated to {new_status}!")
                            st.rerun()
        else:
            st.warning("Database not initialized.")
