"""
Session State Manager

Centralized management for Streamlit session state initialization
to reduce code duplication across pages.
"""

import streamlit as st
from typing import Dict, Any, Optional


# Predefined state configurations for common page types
STATE_CONFIGS = {
    'update_page': {
        'uploaded_data': None,
        'field_mapping': {},
        'identifier_field': 'id',
        'update_results': None,
        'preview_results': None
    },
    'import_page': {
        'uploaded_data': None,
        'field_mapping': {},
        'import_type': 'companies',
        'import_results': None,
        'final_tag_mappings': {},
        'manual_tag_mappings': {},
        'mapping_file_processed': False
    },
    'personio_page': {
        'personio_client': None,
        'employees_df': None,
        'employees_column_mapping': {},
        'absences_df': None,
        'absences_column_mapping': {},
        'attendances_df': None,
        'attendances_column_mapping': {}
    },
    'cost_calculator': {
        'calculation_results': None,
        'calculation_details': None,
        'basic_params': None,
        'overhead_costs': None,
        'pricing_params': None
    }
}


def init_session_state(page_type: str,
                      custom_states: Optional[Dict[str, Any]] = None,
                      overrides: Optional[Dict[str, Any]] = None) -> None:
    """
    Initialize session state for a page with predefined or custom configurations.

    Args:
        page_type: Type of page ('update_page', 'import_page', 'personio_page', 'cost_calculator', or 'custom')
        custom_states: Custom state configuration (used when page_type='custom')
        overrides: Override specific default values from the predefined configuration

    Example:
        # Use predefined configuration
        init_session_state('update_page')

        # Use predefined configuration with overrides
        init_session_state('update_page', overrides={'identifier_field': 'email'})

        # Use custom configuration
        init_session_state('custom', custom_states={'my_data': None, 'my_flag': False})

        # Combine predefined with additional custom states
        init_session_state('update_page', custom_states={'extra_field': []})
    """
    # Get base configuration
    if page_type in STATE_CONFIGS:
        base_config = STATE_CONFIGS[page_type].copy()
    elif page_type == 'custom' and custom_states:
        base_config = custom_states.copy()
    else:
        raise ValueError(f"Invalid page_type '{page_type}'. Use one of: {list(STATE_CONFIGS.keys())} or 'custom'")

    # Apply overrides if provided
    if overrides:
        base_config.update(overrides)

    # Add custom states if provided (for extending predefined configs)
    if custom_states and page_type != 'custom':
        base_config.update(custom_states)

    # Initialize all states
    for key, default_value in base_config.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def ensure_state_exists(key: str, default_value: Any = None) -> None:
    """
    Ensure a specific session state key exists with a default value.

    Args:
        key: Session state key
        default_value: Default value if key doesn't exist
    """
    if key not in st.session_state:
        st.session_state[key] = default_value


def reset_page_state(page_type: str) -> None:
    """
    Reset all session state keys for a specific page type to default values.

    Args:
        page_type: Type of page to reset
    """
    if page_type not in STATE_CONFIGS:
        raise ValueError(f"Unknown page_type '{page_type}'. Use one of: {list(STATE_CONFIGS.keys())}")

    config = STATE_CONFIGS[page_type]
    for key, default_value in config.items():
        st.session_state[key] = default_value


def clear_page_state(page_type: str) -> None:
    """
    Clear (delete) all session state keys for a specific page type.

    Args:
        page_type: Type of page to clear
    """
    if page_type not in STATE_CONFIGS:
        raise ValueError(f"Unknown page_type '{page_type}'. Use one of: {list(STATE_CONFIGS.keys())}")

    config = STATE_CONFIGS[page_type]
    for key in config.keys():
        if key in st.session_state:
            del st.session_state[key]


def get_state_config(page_type: str) -> Dict[str, Any]:
    """
    Get the predefined state configuration for a page type.

    Args:
        page_type: Type of page

    Returns:
        Dictionary of state keys and default values
    """
    if page_type not in STATE_CONFIGS:
        raise ValueError(f"Unknown page_type '{page_type}'. Use one of: {list(STATE_CONFIGS.keys())}")

    return STATE_CONFIGS[page_type].copy()


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
