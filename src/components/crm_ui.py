"""
Shared UI components for CRM Import and Update pages.

Provides reusable Streamlit components to maintain consistent UI
across different CRM operations.
"""

import streamlit as st
import pandas as pd
from typing import Tuple, Optional
from .session_state import init_global_crm_state


def render_wip_warning():
    """Render a consistent 'Work in Progress' warning banner."""
    st.header("Dies ist :red[experimentell] - In Arbeit", divider="red")


def render_environment_selector() -> Tuple[str, Optional[str]]:
    """
    Render environment selection UI using global CRM session state.

    Returns:
        Tuple of (environment, custom_url)
    """
    # Initialize global state
    init_global_crm_state()

    st.subheader("🌍 Umgebungsauswahl")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Get current index from global state
        try:
            current_index = ["production", "staging", "custom"].index(st.session_state.crm_environment)
        except ValueError:
            current_index = 0

        env_option = st.radio(
            "Umgebung auswählen",
            options=["production", "staging", "custom"],
            index=current_index,
            key="crm_environment",  # Bind directly to session state for immediate updates
            help="Wählen Sie die Poool-Umgebung für die Verbindung"
        )

    with col2:
        custom_url = None
        if env_option == 'custom':
            custom_url = st.text_input(
                "Benutzerdefinierte URL (Sandbox)",
                value=st.session_state.crm_custom_url or '',
                placeholder="https://your-sandbox.poool.rocks",
                help="Geben Sie Ihre Sandbox-Umgebungs-URL ein"
            )
            st.session_state.crm_custom_url = custom_url
        else:
            st.session_state.crm_custom_url = None

    with col3:
        if env_option == 'production':
            st.info("🟢 Produktionsumgebung")
        elif env_option == 'staging':
            st.info("🟡 Staging-Umgebung")
        else:
            st.info("🧪 Sandbox-Umgebung")

    return env_option, custom_url


def render_api_configuration(test_connection_callback) -> Tuple[str, bool]:
    """
    Render API configuration UI with test connection using global CRM session state.

    Args:
        test_connection_callback: Function to call for testing connection

    Returns:
        Tuple of (api_key, is_connected)
    """
    # Initialize global state
    init_global_crm_state()

    st.subheader("🔑 API-Konfiguration")

    user_api_key = st.text_input(
        "Poool API-Schlüssel",
        value=st.session_state.crm_api_key,
        type="password",
        placeholder="Geben Sie Ihren API-Schlüssel ein...",
        help="Ihr Poool CRM API-Schlüssel"
    )

    if st.button("🔍 Verbindung testen", type="primary"):
        if not user_api_key:
            st.error("Bitte geben Sie einen API-Schlüssel ein")
            return user_api_key, False
        else:
            current_env = st.session_state.crm_environment
            custom_url = st.session_state.crm_custom_url if current_env == 'custom' else None

            if current_env == 'custom' and not custom_url:
                st.error("Bitte geben Sie eine benutzerdefinierte URL für die Sandbox-Umgebung ein")
                return user_api_key, False

            with st.spinner(f"Teste API-Verbindung zu {current_env}..."):
                is_valid, message = test_connection_callback(user_api_key, current_env, custom_url)

                if is_valid:
                    st.session_state.crm_api_key = user_api_key
                    st.success(f"✅ API-Verbindung zu **{current_env}** erfolgreich!")
                    st.rerun()
                else:
                    st.error(f"❌ Verbindung zu {current_env} fehlgeschlagen: {message}")
                    return user_api_key, False

    if st.session_state.crm_api_key and st.session_state.crm_api_key == user_api_key:
        st.success("🟢 API bereit")
        return user_api_key, True

    return user_api_key, False


def render_file_uploader(operation_type: str = "import") -> Optional[pd.DataFrame]:
    """
    Render file uploader with preview.

    Args:
        operation_type: "import" or "update"

    Returns:
        DataFrame or None
    """
    st.subheader("📁 Datei-Upload")

    if not st.session_state.get('api_key'):
        st.info("⚠️ Bitte konfigurieren Sie zuerst die API-Verbindung")
        return None

    action_text = "importieren" if operation_type == "import" else "aktualisieren"

    uploaded_file = st.file_uploader(
        f"CSV- oder Excel-Datei mit Daten zum {action_text} auswählen",
        type=['csv', 'xlsx', 'xls'],
        help=f"Datei mit den zu {action_text}den Daten hochladen"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, dtype=str)
            else:
                df = pd.read_excel(uploaded_file, dtype=str)

            st.session_state.uploaded_data = df
            row_count = len(df)
            col_count = len(df.columns)
            st.success(f"✅ Datei hochgeladen: {row_count:,} Zeilen, {col_count} Spalten")

            # Show sample
            with st.expander("📊 Datenvorschau (erste 5 Zeilen)"):
                st.dataframe(df.head(), use_container_width=True)

            return df

        except Exception as e:
            st.error(f"Fehler beim Lesen der Datei: {str(e)}")
            st.session_state.uploaded_data = None
            return None

    return st.session_state.get('uploaded_data')


def render_results_display(results: dict, operation_type: str = "import"):
    """
    Render results display with success/failure breakdown.

    Args:
        results: Dict with 'successful' and 'failed' lists
        operation_type: "import" or "update"
    """
    if not results:
        return

    st.markdown("---")
    st.subheader(f"📊 {operation_type.title()} Results")

    successful = results.get('successful', [])
    failed = results.get('failed', [])

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("✅ Successful", len(successful))
    with col2:
        st.metric("❌ Failed", len(failed))
    with col3:
        total = len(successful) + len(failed)
        success_rate = (len(successful) / total * 100) if total > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")

    # Successful records
    if successful:
        with st.expander(f"✅ Successful {operation_type.title()}s ({len(successful)})", expanded=True):
            success_df = pd.DataFrame(successful)
            st.dataframe(success_df, use_container_width=True)

    # Failed records
    if failed:
        with st.expander(f"❌ Failed {operation_type.title()}s ({len(failed)})", expanded=True):
            failed_df = pd.DataFrame(failed)
            st.dataframe(failed_df, use_container_width=True)


def get_csv_columns(df: pd.DataFrame) -> list:
    """
    Get CSV columns with empty string prefix for unmapped option.

    Args:
        df: DataFrame

    Returns:
        List of columns with '' as first element
    """
    if df is None:
        return ['']
    return [''] + list(df.columns)


def render_mapping_summary(field_mapping: dict):
    """
    Render current field mapping summary.

    Args:
        field_mapping: Dict of CSV column to API field mappings
    """
    if not field_mapping:
        return

    st.markdown("### 📋 Aktuelle Zuordnungsübersicht")

    mapping_df = pd.DataFrame([
        {"CSV-Spalte": csv_col, "API-Feld": api_field}
        for csv_col, api_field in field_mapping.items()
    ])
    st.dataframe(mapping_df, use_container_width=True)

    mapped_count = len(field_mapping)
    st.info(f"✅ {mapped_count} Felder zugeordnet")


def render_preview_matches(df: pd.DataFrame, field_mapping: dict, identifier_field: str,
                           preview_function, entity_type: str = "company"):
    """
    Render preview matches section with results display.

    Args:
        df: DataFrame with data
        field_mapping: CSV column to API field mapping
        identifier_field: Field to use for matching
        preview_function: Function to call for preview (takes api_key, df, mapping, identifier, env, url, limit)
        entity_type: "company" or "person"
    """
    st.markdown("### 2️⃣ Vorschau Übereinstimmungen (Optional)")

    # Check if identifier is mapped
    identifier_mapped = identifier_field in field_mapping.values()

    if not identifier_mapped:
        st.warning(f"⚠️ Ordnen Sie das Identifikationsfeld '{identifier_field}' zu, um die Vorschau zu aktivieren")
        return

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("Vorschau, wie Datensätze vor der Aktualisierung abgeglichen werden:")

    with col2:
        if st.button("🔍 Vorschau Übereinstimmungen", type="secondary"):
            with st.spinner("Vorschau der ersten 20 Übereinstimmungen..."):
                current_env = st.session_state.get('environment', 'production')
                custom_url = st.session_state.get('custom_url') if current_env == 'custom' else None

                preview_results = preview_function(
                    st.session_state.crm_api_key,
                    df,
                    field_mapping,
                    identifier_field,
                    current_env,
                    custom_url,
                    preview_limit=20
                )

                st.session_state.preview_results = preview_results

    # Display preview results if available
    if st.session_state.get('preview_results'):
        st.markdown("#### Vorschau-Ergebnisse")

        preview_df = pd.DataFrame(st.session_state.preview_results)

        # Summary counts
        if 'status' in preview_df.columns:
            found_count = len(preview_df[preview_df['status'].str.contains('✅')])
            fuzzy_count = len(preview_df[preview_df['status'].str.contains('⚠️')])
            not_found_count = len(preview_df[preview_df['status'].str.contains('❌')])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Gefunden", found_count)
            with col2:
                st.metric("⚠️ Ungenaue Übereinstimmung", fuzzy_count)
            with col3:
                st.metric("❌ Nicht gefunden", not_found_count)

        # Show preview table
        st.dataframe(preview_df, use_container_width=True)

        if st.button("Vorschau löschen"):
            st.session_state.preview_results = None
            st.rerun()


def render_update_execution(df: pd.DataFrame, field_mapping: dict, identifier_field: str,
                            bulk_update_function, entity_type: str = "company",
                            entity_icon: str = "🔄"):
    """
    Render update execution section with dry run mode and execute button.

    Args:
        df: DataFrame with data
        field_mapping: CSV column to API field mapping
        identifier_field: Field to use for matching
        bulk_update_function: Function to call for bulk update (takes api_key, df, mapping, identifier, env, url, dry_run)
        entity_type: "company" or "person"
        entity_icon: Icon for the update button
    """
    st.markdown("### 3️⃣ Aktualisierung ausführen")

    # Dry run option
    dry_run_mode = st.checkbox(
        "🧪 Test-Modus (nur Vorschau, keine echten Aktualisierungen)",
        value=False,
        help="Wenn aktiviert, simuliert die Aktualisierung ohne echte API-Aufrufe"
    )

    if dry_run_mode:
        st.info("⚠️ **Test-Modus aktiv** - Es werden keine echten Aktualisierungen vorgenommen. Ergebnisse zeigen, was aktualisiert WÜRDE.")

    # Check if identifier is mapped
    identifier_mapped = identifier_field in field_mapping.values()

    if not identifier_mapped:
        st.error(f"⚠️ Bitte ordnen Sie das Identifikationsfeld '{identifier_field}' vor der Aktualisierung zu")
    elif not field_mapping:
        st.error("⚠️ Bitte ordnen Sie mindestens ein Feld zur Aktualisierung zu")
    else:
        row_count = len(df)

        button_text = f"🧪 Vorschau {row_count:,} Aktualisierungen" if dry_run_mode else f"{entity_icon} {row_count:,} Datensätze aktualisieren"
        button_type = "secondary" if dry_run_mode else "primary"

        if st.button(button_text, type=button_type):
            spinner_text = f"Simuliere Aktualisierungen für {row_count:,} {entity_type}..." if dry_run_mode else f"Aktualisiere {row_count:,} {entity_type}..."

            with st.spinner(spinner_text):
                current_env = st.session_state.get('environment', 'production')
                custom_url = st.session_state.get('custom_url') if current_env == 'custom' else None

                successful, failed = bulk_update_function(
                    st.session_state.crm_api_key,
                    df,
                    field_mapping,
                    identifier_field,
                    current_env,
                    custom_url,
                    dry_run=dry_run_mode
                )

                st.session_state.update_results = {
                    'successful': successful,
                    'failed': failed,
                    'dry_run': dry_run_mode
                }
                st.rerun()


def render_update_results(results: dict):
    """
    Render update results with dry run banner and success/failure breakdown.

    Args:
        results: Dict with 'successful', 'failed', and 'dry_run' keys
    """
    if not results:
        return

    st.markdown("---")

    # Show dry run banner if applicable
    if results.get('dry_run', False):
        st.warning("🧪 **TEST-MODUS ERGEBNISSE** - Es wurden keine echten Aktualisierungen vorgenommen. Dies zeigt, was aktualisiert WÜRDE.")

    st.subheader("📊 Aktualisierungsergebnisse")

    successful = results.get('successful', [])
    failed = results.get('failed', [])

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("✅ Erfolgreich", len(successful))
    with col2:
        st.metric("❌ Fehlgeschlagen", len(failed))
    with col3:
        total = len(successful) + len(failed)
        success_rate = (len(successful) / total * 100) if total > 0 else 0
        st.metric("Erfolgsquote", f"{success_rate:.1f}%")

    # Successful updates
    if successful:
        with st.expander(f"✅ Erfolgreiche Aktualisierungen ({len(successful)})", expanded=True):
            success_df = pd.DataFrame(successful)
            st.dataframe(success_df, use_container_width=True)

    # Failed updates
    if failed:
        with st.expander(f"❌ Fehlgeschlagene Aktualisierungen ({len(failed)})", expanded=True):
            failed_df = pd.DataFrame(failed)
            st.dataframe(failed_df, use_container_width=True)

    # Clear results button
    if st.button("🔄 Neue Aktualisierung starten"):
        st.session_state.update_results = None
        st.session_state.uploaded_data = None
        st.session_state.field_mapping = {}
        st.rerun()
