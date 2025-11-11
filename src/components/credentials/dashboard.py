"""
Connection Dashboard

Provides a visual dashboard showing the status of all API connections.
Can be rendered in sidebar or as a page section.
"""

import streamlit as st
from datetime import datetime
from typing import Optional
from .manager import get_credential_manager, ConnectionStatus


def render_connection_dashboard(location: str = 'sidebar',
                                title: str = "🔌 API Verbindungen",
                                show_test_buttons: bool = False,
                                expanded: bool = False) -> None:
    """
    Render a dashboard showing all API connection statuses.

    Args:
        location: Where to render ('sidebar', 'page', 'expander')
        title: Dashboard title
        show_test_buttons: Whether to show test connection buttons
        expanded: Whether expander should be expanded by default (only for expander mode)
    """
    manager = get_credential_manager()
    apis = manager.get_all_apis()

    if not apis:
        return

    def _render_dashboard_content():
        """Internal function to render dashboard content."""
        # Summary metrics
        total_apis = len(apis)
        connected = sum(1 for api in apis if manager.get_status(api.name).is_connected)
        configured = sum(1 for api in apis if manager.get_status(api.name).is_configured)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", total_apis)
        with col2:
            st.metric("Verbunden", connected)
        with col3:
            st.metric("Konfiguriert", configured)

        st.markdown("---")

        # Individual API status
        for api in apis:
            status = manager.get_status(api.name)
            _render_api_status_row(api.name, api.display_name, status, show_test_buttons)

    # Render based on location
    if location == 'sidebar':
        with st.sidebar:
            st.markdown(f"### {title}")
            _render_dashboard_content()
    elif location == 'expander':
        with st.expander(title, expanded=expanded):
            _render_dashboard_content()
    else:  # page
        st.markdown(f"## {title}")
        _render_dashboard_content()


def _render_api_status_row(api_name: str,
                           display_name: str,
                           status: ConnectionStatus,
                           show_test_button: bool = False) -> None:
    """
    Render a single API status row.

    Args:
        api_name: Internal API name
        display_name: Display name
        status: ConnectionStatus object
        show_test_button: Whether to show test button
    """
    manager = get_credential_manager()

    # Container for the row
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.markdown(f"**{display_name}**")

        with col2:
            # Status indicator
            if status.is_connected:
                st.markdown("🟢 Verbunden")
            elif status.is_configured and not status.is_tested:
                st.markdown("🟡 Konfiguriert")
            elif status.is_tested and not status.is_connected:
                st.markdown("🔴 Fehler")
            else:
                st.markdown("⚪ Nicht konfiguriert")

        with col3:
            if show_test_button and status.is_configured:
                if st.button("🔍", key=f"dashboard_test_{api_name}", help="Verbindung testen"):
                    with st.spinner("Teste..."):
                        success, message = manager.test_connection(api_name)
                        if success:
                            st.success("✅")
                        else:
                            st.error(f"❌ {message}")

        # Additional info in smaller text
        if status.last_tested:
            time_diff = datetime.now() - status.last_tested
            if time_diff.seconds < 60:
                time_str = "vor wenigen Sekunden"
            elif time_diff.seconds < 3600:
                time_str = f"vor {time_diff.seconds // 60} Minuten"
            else:
                time_str = f"vor {time_diff.seconds // 3600} Stunden"

            st.caption(f"Zuletzt getestet: {time_str}")

        if status.error_message and not status.is_connected:
            with st.expander("Fehlerdetails anzeigen", expanded=False):
                st.error(status.error_message)

        st.markdown("---")


def render_compact_status_bar(apis_to_show: Optional[list] = None) -> None:
    """
    Render a compact status bar showing connection status for specified APIs.

    Args:
        apis_to_show: List of API names to show (None = show all)
    """
    manager = get_credential_manager()
    apis = manager.get_all_apis()

    if apis_to_show:
        apis = [api for api in apis if api.name in apis_to_show]

    if not apis:
        return

    cols = st.columns(len(apis))

    for idx, api in enumerate(apis):
        status = manager.get_status(api.name)

        with cols[idx]:
            if status.is_connected:
                icon = "🟢"
                label = f"{api.display_name}"
            elif status.is_configured:
                icon = "🟡"
                label = f"{api.display_name}"
            else:
                icon = "⚪"
                label = f"{api.display_name}"

            st.markdown(f"{icon} **{label}**")


def render_api_quick_status(api_name: str, show_details: bool = True) -> None:
    """
    Render quick status for a single API with optional details.

    Args:
        api_name: Internal API name
        show_details: Whether to show detailed status info
    """
    manager = get_credential_manager()
    config = manager.get_api_config(api_name)
    status = manager.get_status(api_name)

    if not config:
        return

    if status.is_connected:
        st.success(f"✅ {config.display_name}: Verbunden")
    elif status.is_configured and not status.is_tested:
        st.warning(f"⚠️ {config.display_name}: Konfiguriert, aber nicht getestet")
        if show_details:
            st.info("💡 Bitte testen Sie die Verbindung")
    elif status.is_tested and not status.is_connected:
        st.error(f"❌ {config.display_name}: Verbindung fehlgeschlagen")
        if show_details and status.error_message:
            st.caption(f"Fehler: {status.error_message}")
    else:
        st.info(f"⚪ {config.display_name}: Nicht konfiguriert")


def check_required_apis(required_apis: list, show_warning: bool = True) -> bool:
    """
    Check if required APIs are configured and connected.

    Args:
        required_apis: List of required API names
        show_warning: Whether to show warning messages

    Returns:
        True if all required APIs are connected
    """
    manager = get_credential_manager()
    missing_apis = []
    disconnected_apis = []

    for api_name in required_apis:
        status = manager.get_status(api_name)

        if not status.is_configured:
            missing_apis.append(api_name)
        elif not status.is_connected:
            disconnected_apis.append(api_name)

    if show_warning:
        if missing_apis:
            api_names = ", ".join([manager.get_api_config(name).display_name for name in missing_apis])
            st.warning(f"⚠️ Bitte konfigurieren Sie: {api_names}")

        if disconnected_apis:
            api_names = ", ".join([manager.get_api_config(name).display_name for name in disconnected_apis])
            st.error(f"❌ Verbindung fehlgeschlagen für: {api_names}")

    return len(missing_apis) == 0 and len(disconnected_apis) == 0
