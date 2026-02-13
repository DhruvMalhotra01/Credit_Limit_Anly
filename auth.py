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

CLIENT_SECRET_FILE = 'client_secret.json'

def get_google_auth_flow():
    """Initializes the OAuth2 flow."""
    if not os.path.exists(CLIENT_SECRET_FILE):
        st.error(f"Error: {CLIENT_SECRET_FILE} not found. Please place your Google Cloud credentials file in the root directory.")
        return None
        
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:8501' # Standard Streamlit local port
    )
    return flow

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
