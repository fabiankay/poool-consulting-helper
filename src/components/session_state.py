"""
Global session state management for the Poool Consulting Helper app.

Provides centralized initialization for shared state variables across pages.
"""

import streamlit as st


def init_global_crm_state():
    """
    Initialize global CRM session state variables.

    These variables persist across all CRM pages (import, update, person update)
    to provide a seamless user experience without needing to re-enter credentials
    or re-select environment when navigating between pages.

    State variables:
        - crm_environment: 'production', 'staging', or 'custom'
        - crm_custom_url: Custom/sandbox URL when environment is 'custom'
        - crm_api_key: Poool CRM API key
    """
    if 'crm_environment' not in st.session_state:
        st.session_state.crm_environment = 'production'

    if 'crm_custom_url' not in st.session_state:
        st.session_state.crm_custom_url = None

    if 'crm_api_key' not in st.session_state:
        st.session_state.crm_api_key = ''
