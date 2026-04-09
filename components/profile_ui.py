import streamlit as st

def render_profile_page():
    st.markdown('<div class="hero-banner" style="background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 100%); margin-bottom: 20px;"><h1>User <span class="highlight" style="color: #c4b5fd;">Profile</span></h1></div>', unsafe_allow_html=True)
    if st.button("← Back to Dashboard"):
        st.session_state.current_page = "Home"
        st.rerun()
        
    user = st.session_state.get("current_user", {})
    user_id = user.get("User_ID", "U-ADMIN01")
    name = user.get("Name", "System Admin")
    role = user.get("Role", "Admin")
    email = user.get("Email", "admin@surakshapay.ai")
    status = user.get("Status", "Active")
    
    st.markdown(f'''
    <div style="display: flex; gap: 20px; align-items: stretch; margin-bottom: 20px;">
        <div class="glass-card" style="text-align:center; padding: 20px; flex: 1; border: 1px solid #e2e8f0; border-radius: 12px; background: white;">
            <div style="width: 80px; height: 80px; border-radius: 50%; background-color: #6366f1; color: white; display: flex; align-items: center; justify-content: center; font-size: 35px; margin: 0 auto 15px auto;">
                {name[0].upper() if name else 'U'}
            </div>
            <h3 style="color: #1e293b; margin: 0; font-size: 1.2rem;">{name}</h3>
            <p style="color: #64748b; font-size: 0.95rem; margin-top: 5px;">{role}</p>
            <span style="background-color: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.8rem;">{status}</span>
        </div>
        <div class="glass-card" style="padding: 20px; flex: 2; border: 1px solid #e2e8f0; border-radius: 12px; background: white;">
            <h4 style="color: #0f52ba; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 15px; font-size: 1.05rem;">Personal Information</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <label style="color: #64748b; font-size: 0.85rem;">Full Name</label>
                    <p style="color: #1e293b; font-weight: 600; margin: 0;">{name}</p>
                </div>
                <div>
                    <label style="color: #64748b; font-size: 0.85rem;">Email Address</label>
                    <p style="color: #1e293b; font-weight: 600; margin: 0;">{email}</p>
                </div>
                <div>
                    <label style="color: #64748b; font-size: 0.85rem;">User ID</label>
                    <p style="color: #1e293b; font-weight: 600; margin: 0;">{user_id}</p>
                </div>
                <div>
                    <label style="color: #64748b; font-size: 0.85rem;">Role Access</label>
                    <p style="color: #1e293b; font-weight: 600; margin: 0;">{role}</p>
                </div>
            </div>
        </div>
    </div>
    <div class="glass-card" style="padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background: white; margin-bottom: 25px;">
        <h4 style="color: #0f52ba; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 15px; font-size: 1.05rem;">Account Security</h4>
        <div style="display: flex; gap: 15px;">
            <button disabled style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 8px 16px; border-radius: 6px; color: #94a3b8; font-weight: 600; cursor: not-allowed; font-size: 0.9rem;">Change Password</button>
            <button disabled style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 8px 16px; border-radius: 6px; color: #94a3b8; font-weight: 600; cursor: not-allowed; font-size: 0.9rem;">Enable 2FA</button>
        </div>
        <p style="color: #94a3b8; font-size: 0.75rem; margin-top: 10px; margin-bottom: 0;">Security features are managed by your organization's identity provider.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("Log out 👉", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
