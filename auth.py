import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import streamlit as st

# Scopes required as per instructions
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_google_auth_flow():
    """Initializes the OAuth2 flow using Streamlit secrets."""
    try:
        # Read credentials from st.secrets (works on both local and cloud)
        client_config = {
            "web": {
                "client_id": st.secrets["GOOGLE_CLIENT_ID"],
                "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        }
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri='http://localhost:8501' # Standard Streamlit local port
        )
        return flow
    except KeyError as e:
        st.error(f"Error: Missing secret {e}. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in Streamlit secrets.")
        return None

def login_button():
    """Generates the login URL and displays a button."""
    flow = get_google_auth_flow()
    if not flow: return
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    st.session_state['oauth_state'] = state
    st.link_button("Login with Google", authorization_url)

def handle_callback():
    """Handles the redirect callback from Google."""
    if 'code' in st.query_params:
        flow = get_google_auth_flow()
        if not flow: return
        
        flow.fetch_token(code=st.query_params['code'])
        credentials = flow.credentials
        
        st.session_state['credentials'] = credentials_to_dict(credentials)
        st.session_state['logged_in'] = True
        
        # Fetch user info
        from googleapiclient.discovery import build
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        st.session_state['user_email'] = user_info.get('email')
        st.session_state['user_name'] = user_info.get('name')
        
        # Clear query params
        st.query_params.clear()
        st.rerun()

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def get_credentials():
    if 'credentials' in st.session_state:
        return Credentials(**st.session_state['credentials'])
    return None
