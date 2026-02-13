import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from auth import login_button, handle_callback
from data_generator import generate_synthetic_data
from analysis import get_comprehensive_score
from decision_engine import generate_credit_decision
from mailer import send_decision_email
from utils import create_pdf_report

# Page Configuration
st.set_page_config(
    page_title="Dynamic Credit Limit Analyzer",
    page_icon="💳",
    layout="wide"
)

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'analysis' not in st.session_state:
    st.session_state['analysis'] = None
if 'decision' not in st.session_state:
    st.session_state['decision'] = None
if 'current_limit' not in st.session_state:
    st.session_state['current_limit'] = 50000

# Custom CSS with Animations and Transitions
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #1e1e2e;
        color: #ffffff;
    }
    
    /* Full-height side image container */
    .side-image-container {
        height: 85vh;
        width: 100%;
        border-radius: 24px;
        overflow: hidden;
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://images.unsplash.com/photo-1611974714024-462745cb346d?auto=format&fit=crop&q=80&w=1000');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 40px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
    }

    /* Input styling */
    .stTextInput>div>div>input {
        background-color: #2b2b3b !important;
        color: white !important;
        border: 1px solid #3d3d4d !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
    }
    
    /* Button Styling (Purple Theme) */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #6c5ce7 !important;
        color: white !important;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #5b4bc4 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
    }

    /* Social Buttons Styling */
    .social-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        background-color: transparent;
        border: 1px solid #3d3d4d;
        border-radius: 10px;
        padding: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        text-decoration: none;
        width: 100%;
        margin-top: 10px;
    }
    
    .social-btn:hover {
        background-color: #2b2b3b;
        border-color: #6c5ce7;
    }

    /* Divider */
    .divider-container {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 20px 0;
        color: #a3a8c3;
    }
    .divider-container::before, .divider-container::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #3d3d4d;
    }
    .divider-container:not(:empty)::before { margin-right: .5em; }
    .divider-container:not(:empty)::after { margin-left: .5em; }

    /* Login Box */
    .auth-container {
        padding: 0 10%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }

    /* Tabs Overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: #a3a8c3;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #6c5ce7;
        border-bottom: 2px solid #6c5ce7;
    }
    </style>
    """, unsafe_allow_html=True)

# Callback Handling
handle_callback()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 💳 DCLA System")
    if st.session_state['logged_in']:
        st.success(f"Logged in as: \n{st.session_state['user_email']}")
        
        # Current Limit Input
        st.divider()
        st.subheader("Account Metadata")
        st.session_state['current_limit'] = st.number_input(
            "Enter Current Credit Card Limit (₹)",
            min_value=10000,
            max_value=1000000,
            value=st.session_state['current_limit'],
            step=5000
        )
        
        st.divider()
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
    else:
        st.info("Please login to access banking analytics.")

# --- MAIN APP LOGIC ---
if not st.session_state['logged_in']:
    # REDESIGNED LOGIN/SIGNUP PAGE (MATCHING REFERENCE IMAGE)
    
    col_img, col_auth = st.columns([1, 1], gap="large")
    
    with col_img:
        st.markdown(f"""
            <div class="side-image-container">
                <h2 style="font-size: 2.5rem; margin-bottom: 0; color: white;">Capturing Moments,</h2>
                <h2 style="font-size: 2.5rem; margin-top: 0; color: white;">Creating Memories</h2>
            </div>
        """, unsafe_allow_html=True)

    with col_auth:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        auth_mode = st.tabs(["🔑 Login", "📝 Sign Up"])
        
        with auth_mode[1]: # Default to Signup as per reference image
            st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0;'>Create an account</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #a3a8c3; margin-top: 0;'>Already have an account? <span style='color: #6c5ce7; cursor: pointer;'>Log in</span></p>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("First Name", placeholder="Fletcher", label_visibility="collapsed")
            with c2:
                st.text_input("Last Name", placeholder="Last name", label_visibility="collapsed")
            
            st.text_input("Email", placeholder="Email", label_visibility="collapsed")
            st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            
            st.checkbox("I agree to the Terms & Conditions")
            
            if st.button("Create account"):
                st.warning("Please use Google Login for this demo.")
            
            st.markdown('<div class="divider-container">Or register with</div>', unsafe_allow_html=True)
            
            sc1, sc2 = st.columns(2)
            with sc1:
                # Custom Google Button to match style
                st.markdown("""
                    <div class="social-btn">
                        <img src="https://www.gstatic.com/images/branding/product/1x/gsa_512dp.png" width="20">
                        Google
                    </div>
                """, unsafe_allow_html=True)
            with sc2:
                # Custom Apple Button to match style
                st.markdown("""
                    <div class="social-btn">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="20" style="filter: invert(1);">
                        Apple
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.write("Secure Google Auth")
            login_button()

        with auth_mode[0]: # Login tab
            st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0;'>Welcome Back</h1>", unsafe_allow_html=True)
            st.text_input("Email Address", placeholder="name@bank.com", key="login_email")
            st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            if st.button("Sign In"):
                st.warning("Please use Google Login for this demo.")
            
            st.markdown('<div class="divider-container">Or continue with</div>', unsafe_allow_html=True)
            login_button()
            
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # LOGGED IN DASHBOARD (Maintained original logic with new CSS)
    tabs = st.tabs(["📤 Data Input", "📊 Behavioral Analytics", "📝 Decision Report"])

    # TABS 1: DATA INPUT
    with tabs[0]:
        st.header("Transaction Data Upload")
        uploaded_file = st.file_uploader("Upload Transaction CSV (date, amount, category, payment_type, paid_on_time)", type="csv")
        
        col1, col2 = st.columns(2)
        with col1:
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    df['date'] = pd.to_datetime(df['date'])
                    # Validation: ensure current_limit is NOT in the CSV (as per refactor requirement)
                    if 'current_limit' in df.columns:
                        df = df.drop(columns=['current_limit'])
                    st.session_state['data'] = df
                    st.success("File uploaded successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        
        with col2:
            st.write("Don't have data? Use our generator:")
            if st.button("Generate Synthetic Demo Data"):
                with st.spinner("Simulating banking transactions..."):
                    st.session_state['data'] = generate_synthetic_data(150)
                    st.success("Synthetic data generated!")

        if st.session_state['data'] is not None:
            st.divider()
            st.subheader("Data Preview")
            st.dataframe(st.session_state['data'].head(10), use_container_width=True)
            
            # Summary Stats
            df = st.session_state['data']
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Transactions", len(df))
            m2.metric("Total Spend", f"₹{df['amount'].sum():,.2f}")
            m3.metric("Avg Transaction", f"₹{df['amount'].mean():,.2f}")

    # TABS 2: ANALYTICS
    with tabs[1]:
        if st.session_state['data'] is None:
            st.warning("Please upload or generate data first.")
        else:
            df = st.session_state['data']
            current_limit = st.session_state['current_limit']
            
            with st.spinner("Analyzing behavior..."):
                analysis = get_comprehensive_score(df, current_limit)
                st.session_state['analysis'] = analysis

            st.header("Behavioral Insights")
            
            # Row 1: Charts
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Spending Over Time")
                df_monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().reset_index()
                df_monthly['date'] = df_monthly['date'].astype(str)
                fig_line = px.line(df_monthly, x='date', y='amount', title="Monthly Spending Trend")
                st.plotly_chart(fig_line, use_container_width=True)
            
            with c2:
                st.subheader("Category Distribution")
                fig_pie = px.pie(df, values='amount', names='category', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)

            # Row 2: Gauges
            st.divider()
            st.subheader("Credit Health Metrics")
            g1, g2, g3 = st.columns(3)
            
            with g1:
                fig_g1 = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = analysis['repayment_score'],
                    title = {'text': "Repayment Score"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
                ))
                st.plotly_chart(fig_g1, use_container_width=True)
                
            with g2:
                util = analysis['utilization_ratio']
                color = "green" if util < 30 else "orange" if util < 70 else "red"
                fig_g2 = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = util,
                    title = {'text': "Utilization (%)"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': color}}
                ))
                st.plotly_chart(fig_g2, use_container_width=True)

            with g3:
                fig_g3 = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = analysis['stability_score'],
                    title = {'text': "Stability Score"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
                ))
                st.plotly_chart(fig_g3, use_container_width=True)

    # TABS 3: DECISION
    with tabs[2]:
        if st.session_state['analysis'] is None:
            st.warning("Please run analysis in the previous tab.")
        else:
            analysis = st.session_state['analysis']
            current_limit = st.session_state['current_limit']
            
            # Unpack decision results
            score, rec_limit, explanation = generate_credit_decision(analysis['final_score'], current_limit)
            st.session_state['decision'] = (score, rec_limit, explanation)
            
            st.header("Final Decision Report")
            
            col_res, col_score = st.columns([2, 1])
            
            with col_score:
                st.metric("FINAL CREDIT SCORE", f"{score}/100")
                fig_final = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'steps': [
                            {'range': [0, 40], 'color': "red"},
                            {'range': [40, 65], 'color': "yellow"},
                            {'range': [65, 90], 'color': "lightgreen"},
                            {'range': [90, 100], 'color': "green"}
                        ]
                    }
                ))
                st.plotly_chart(fig_final, use_container_width=True)

            with col_res:
                st.subheader("System Recommendation")
                
                # Determine status label
                if rec_limit > current_limit:
                    status = "LIMIT INCREASE APPROVED"
                elif rec_limit < current_limit:
                    status = "LIMIT REDUCTION RECOMMENDED"
                else:
                    status = "MAINTAIN CURRENT LIMIT"
                    
                st.info(f"STATUS: {status}")
                
                c_lim1, c_lim2 = st.columns(2)
                c_lim1.metric("Current Limit", f"₹{current_limit:,.2f}")
                c_lim2.metric("New Recommended Limit", f"₹{rec_limit:,.2f}", 
                             delta=f"{((rec_limit/current_limit)-1)*100:.1f}%")
                
                st.write("**Behavior Summary & Reasoning:**")
                st.write(explanation)
                
                st.divider()
                
                # Actions
                if st.button("🚀 Send Decision Email & Generate PDF"):
                    with st.spinner("Processing official communication..."):
                        # Email
                        success, msg = send_decision_email(
                            st.session_state['user_email'],
                            score,
                            current_limit,
                            rec_limit,
                            explanation
                        )
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                        
                        # PDF Download
                        pdf_bytes = create_pdf_report(
                            st.session_state['user_email'],
                            current_limit,
                            analysis,
                            st.session_state['decision']
                        )
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_bytes,
                            file_name="Credit_Decision_Report.pdf",
                            mime="application/pdf"
                        )
