"""
Credential UI Components

Reusable UI components for credential input across different API types.
Integrates with CredentialManager for automatic state management.
"""

import streamlit as st
from typing import Optional, Callable, Dict, Any
from .manager import (
    get_credential_manager,
    CredentialType,
    CredentialScope
)


def render_api_key_credential(api_name: str,
                              display_name: str,
                              has_environment: bool = False,
                              environment_options: Optional[list] = None,
                              validator_func: Optional[Callable] = None,
                              help_text: Optional[str] = None) -> bool:
    """
    Render API key credential input with optional environment selection.

    Args:
        api_name: Internal API name
        display_name: Display name for UI
        has_environment: Whether to show environment selector
        environment_options: List of environment options
        validator_func: Function to test connection (api_key, environment, custom_url) -> (bool, str)
        help_text: Optional help text for API key input

    Returns:
        True if credentials are configured and tested
    """
    manager = get_credential_manager()

    # Ensure API is registered
    if not manager.get_api_config(api_name):
        manager.register_api(
            name=api_name,
            display_name=display_name,
            credential_type=CredentialType.API_KEY,
            scope=CredentialScope.GLOBAL,
            has_environment=has_environment,
            environment_options=environment_options,
            validator_func=validator_func,
            credential_fields=['api_key']
        )

    st.subheader(f"🔑 {display_name}")

    # Get current credentials
    current_creds = manager.get_credentials(api_name)
    current_api_key = current_creds.get('api_key', '')
    current_env = current_creds.get('environment', 'production')
    current_custom_url = current_creds.get('custom_url', '')

    # Environment selection (if enabled)
    environment = 'production'
    custom_url = None

    if has_environment:
        col1, col2, col3 = st.columns(3)

        with col1:
            env_options = environment_options or ['production', 'staging', 'custom']
            try:
                env_index = env_options.index(current_env)
            except ValueError:
                env_index = 0

            environment = st.radio(
                "Umgebung",
                options=env_options,
                index=env_index,
                key=f"{api_name}_env",
                help="Wählen Sie die Umgebung für die Verbindung"
            )

        with col2:
            if environment == 'custom':
                custom_url = st.text_input(
                    "Benutzerdefinierte URL",
                    value=current_custom_url,
                    placeholder="https://your-sandbox.example.com",
                    key=f"{api_name}_custom_url",
                    help="Geben Sie Ihre Sandbox-Umgebungs-URL ein"
                )

        with col3:
            if environment == 'production':
                st.info("🟢 Produktionsumgebung")
            elif environment == 'staging':
                st.info("🟡 Staging-Umgebung")
            else:
                st.info("🧪 Sandbox-Umgebung")

    # API Key input
    api_key = st.text_input(
        f"{display_name} Schlüssel",
        value=current_api_key,
        type="password",
        placeholder="Geben Sie Ihren API-Schlüssel ein...",
        help=help_text or f"Ihr {display_name} API-Schlüssel",
        key=f"{api_name}_key"
    )

    # Test connection button
    if st.button(f"🔍 Verbindung testen", type="primary", key=f"{api_name}_test"):
        if not api_key:
            st.error("Bitte geben Sie einen API-Schlüssel ein")
            return False

        if has_environment and environment == 'custom' and not custom_url:
            st.error("Bitte geben Sie eine benutzerdefinierte URL ein")
            return False

        # Store credentials
        creds = {'api_key': api_key}
        if has_environment:
            creds['environment'] = environment
            if custom_url:
                creds['custom_url'] = custom_url

        manager.set_credentials(api_name, **creds)

        # Test connection
        with st.spinner(f"Teste Verbindung zu {display_name}..."):
            success, message = manager.test_connection(api_name)

            if success:
                st.success(f"✅ Verbindung zu **{display_name}** erfolgreich!")
                st.rerun()
            else:
                st.error(f"❌ Verbindung fehlgeschlagen: {message}")
                return False

    # Show status if configured
    status = manager.get_status(api_name)
    if status.is_configured and api_key:
        if status.is_connected:
            st.success("🟢 API bereit")
            return True
        elif status.is_tested and not status.is_connected:
            st.warning(f"⚠️ Letzte Verbindung fehlgeschlagen: {status.error_message}")
        else:
            st.info("💡 API-Schlüssel eingegeben - bitte Verbindung testen")

    return status.is_connected if status else False


def render_oauth2_credential(api_name: str,
                            display_name: str,
                            fields: Optional[Dict[str, str]] = None,
                            authenticate_func: Optional[Callable] = None,
                            help_text: Optional[str] = None) -> bool:
    """
    Render OAuth2 credential input (client ID + secret).

    Args:
        api_name: Internal API name
        display_name: Display name for UI
        fields: Dictionary of field names and labels (e.g., {'client_id': 'Client-ID', 'client_secret': 'Client-Secret'})
        authenticate_func: Function to authenticate (client_id, client_secret) -> client_object
        help_text: Optional help text

    Returns:
        True if authenticated
    """
    manager = get_credential_manager()

    # Default fields
    field_config = fields or {
        'client_id': 'Client-ID',
        'client_secret': 'Client-Secret'
    }

    # Ensure API is registered
    if not manager.get_api_config(api_name):
        manager.register_api(
            name=api_name,
            display_name=display_name,
            credential_type=CredentialType.OAUTH2,
            scope=CredentialScope.PAGE_LOCAL,
            credential_fields=list(field_config.keys())
        )

    st.subheader(f"🔐 {display_name}")

    if help_text:
        st.markdown(help_text)

    # Get current credentials
    current_creds = manager.get_credentials(api_name)

    # Render input fields
    credentials = {}
    for field_key, field_label in field_config.items():
        is_secret = 'secret' in field_key.lower() or 'password' in field_key.lower()
        value = st.text_input(
            field_label,
            value=current_creds.get(field_key, ''),
            type="password" if is_secret else "default",
            key=f"{api_name}_{field_key}"
        )
        credentials[field_key] = value

    # Authenticate button
    if st.button("🔓 Authentifizieren", type="primary", key=f"{api_name}_auth"):
        # Check all fields are filled
        if not all(credentials.values()):
            st.error("Bitte füllen Sie alle Felder aus")
            return False

        # Store credentials
        manager.set_credentials(api_name, **credentials)

        # Authenticate
        if authenticate_func:
            with st.spinner(f"Authentifiziere mit {display_name}..."):
                try:
                    client = authenticate_func(**credentials)
                    manager.set_client(api_name, client)

                    # Update status
                    status = manager.get_status(api_name)
                    status.is_configured = True
                    status.is_tested = True
                    status.is_connected = True
                    status.error_message = None

                    st.success(f"✅ Erfolgreich bei {display_name} authentifiziert!")
                    st.rerun()

                except Exception as e:
                    status = manager.get_status(api_name)
                    status.is_configured = True
                    status.is_tested = True
                    status.is_connected = False
                    status.error_message = str(e)

                    st.error(f"❌ Authentifizierung fehlgeschlagen: {str(e)}")
                    return False

    # Show status
    client = manager.get_client(api_name)
    status = manager.get_status(api_name)

    if client and status.is_connected:
        st.success("🟢 Authentifiziert und bereit")

        # Check token expiration if client has the method
        if hasattr(client, 'is_token_valid'):
            if not client.is_token_valid():
                st.warning("⚠️ Token abgelaufen - bitte erneut authentifizieren")
                return False

        return True
    elif status.is_tested and not status.is_connected:
        st.error(f"❌ {status.error_message}")

    return False


def render_database_credential(api_name: str,
                               display_name: str,
                               fields: Optional[Dict[str, str]] = None,
                               test_func: Optional[Callable] = None,
                               help_text: Optional[str] = None) -> bool:
    """
    Render database credential input.

    Args:
        api_name: Internal API name
        display_name: Display name for UI
        fields: Dictionary of field names and labels
        test_func: Function to test connection (**credentials) -> (bool, str)
        help_text: Optional help text

    Returns:
        True if connection successful
    """
    manager = get_credential_manager()

    # Default fields
    field_config = fields or {
        'host': 'Host',
        'port': 'Port',
        'database': 'Database',
        'username': 'Username',
        'password': 'Password'
    }

    # Ensure API is registered
    if not manager.get_api_config(api_name):
        manager.register_api(
            name=api_name,
            display_name=display_name,
            credential_type=CredentialType.DATABASE,
            scope=CredentialScope.PAGE_LOCAL,
            validator_func=test_func,
            credential_fields=list(field_config.keys())
        )

    st.subheader(f"🗄️ {display_name}")

    if help_text:
        st.markdown(help_text)

    # Get current credentials
    current_creds = manager.get_credentials(api_name)

    # Render input fields
    credentials = {}
    col1, col2 = st.columns(2)

    for idx, (field_key, field_label) in enumerate(field_config.items()):
        is_secret = 'password' in field_key.lower() or 'secret' in field_key.lower()

        with col1 if idx % 2 == 0 else col2:
            value = st.text_input(
                field_label,
                value=current_creds.get(field_key, ''),
                type="password" if is_secret else "default",
                key=f"{api_name}_{field_key}"
            )
            credentials[field_key] = value

    # Test connection button
    if st.button("🔍 Verbindung testen", type="primary", key=f"{api_name}_test_db"):
        # Check all required fields
        if not all(credentials.values()):
            st.error("Bitte füllen Sie alle Felder aus")
            return False

        # Store credentials
        manager.set_credentials(api_name, **credentials)

        # Test connection
        with st.spinner(f"Teste Verbindung zu {display_name}..."):
            success, message = manager.test_connection(api_name)

            if success:
                st.success(f"✅ Verbindung zu {display_name} erfolgreich!")
                st.rerun()
            else:
                st.error(f"❌ Verbindung fehlgeschlagen: {message}")
                return False

    # Show status
    status = manager.get_status(api_name)
    if status.is_configured:
        if status.is_connected:
            st.success("🟢 Datenbank bereit")
            return True
        elif status.is_tested and not status.is_connected:
            st.error(f"❌ Letzte Verbindung fehlgeschlagen: {status.error_message}")

    return status.is_connected if status else False


def render_connection_status_badge(api_name: str, compact: bool = False) -> None:
    """
    Render a connection status badge for an API.

    Args:
        api_name: Internal API name
        compact: Whether to use compact display
    """
    manager = get_credential_manager()
    config = manager.get_api_config(api_name)
    status = manager.get_status(api_name)

    if not config:
        return

    if status.is_connected:
        icon = "🟢"
        text = "Verbunden" if not compact else ""
        st.success(f"{icon} {text}")
    elif status.is_configured and not status.is_tested:
        icon = "🟡"
        text = "Konfiguriert" if not compact else ""
        st.warning(f"{icon} {text}")
    elif status.is_tested and not status.is_connected:
        icon = "🔴"
        text = "Fehler" if not compact else ""
        st.error(f"{icon} {text}")
    else:
        icon = "⚪"
        text = "Nicht konfiguriert" if not compact else ""
        st.info(f"{icon} {text}")
