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
    st.header("This is :red[experimental] - Work in Progress", divider="red")


def render_environment_selector() -> Tuple[str, Optional[str]]:
    """
    Render environment selection UI using global CRM session state.

    Returns:
        Tuple of (environment, custom_url)
    """
    # Initialize global state
    init_global_crm_state()

    st.subheader("🌍 Environment Selection")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Get current index from global state
        try:
            current_index = ["production", "staging", "custom"].index(st.session_state.crm_environment)
        except ValueError:
            current_index = 0

        env_option = st.radio(
            "Select Environment",
            options=["production", "staging", "custom"],
            index=current_index,
            help="Choose which Poool environment to connect to"
        )

        # Update global state
        st.session_state.crm_environment = env_option

    with col2:
        custom_url = None
        if env_option == 'custom':
            custom_url = st.text_input(
                "Custom URL (Sandbox)",
                value=st.session_state.crm_custom_url or '',
                placeholder="https://your-sandbox.poool.rocks",
                help="Enter your sandbox environment URL"
            )
            st.session_state.crm_custom_url = custom_url
        else:
            st.session_state.crm_custom_url = None

    with col3:
        if env_option == 'production':
            st.info("🟢 Production environment")
        elif env_option == 'staging':
            st.info("🟡 Staging environment")
        else:
            st.info("🧪 Sandbox environment")

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

    st.subheader("🔑 API Configuration")

    user_api_key = st.text_input(
        "Poool API Key",
        value=st.session_state.crm_api_key,
        type="password",
        placeholder="Enter your API key...",
        help="Your Poool CRM API key"
    )

    if st.button("🔍 Test Connection", type="primary"):
        if not user_api_key:
            st.error("Please enter an API key")
            return user_api_key, False
        else:
            current_env = st.session_state.crm_environment
            custom_url = st.session_state.crm_custom_url if current_env == 'custom' else None

            if current_env == 'custom' and not custom_url:
                st.error("Please enter a custom URL for sandbox environment")
                return user_api_key, False

            with st.spinner(f"Testing API connection to {current_env}..."):
                is_valid, message = test_connection_callback(user_api_key, current_env, custom_url)

                if is_valid:
                    st.session_state.crm_api_key = user_api_key
                    st.success(f"✅ API connection successful to **{current_env}**!")
                    st.rerun()
                else:
                    st.error(f"❌ Connection failed to {current_env}: {message}")
                    return user_api_key, False

    if st.session_state.crm_api_key and st.session_state.crm_api_key == user_api_key:
        st.success("🟢 API Ready")
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
    st.subheader("📁 File Upload")

    if not st.session_state.get('api_key'):
        st.info("⚠️ Please configure API connection first")
        return None

    action_text = "import" if operation_type == "import" else "update"

    uploaded_file = st.file_uploader(
        f"Choose CSV or Excel file with data to {action_text}",
        type=['csv', 'xlsx', 'xls'],
        help=f"Upload a file containing the data to {action_text}"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state.uploaded_data = df
            row_count = len(df)
            col_count = len(df.columns)
            st.success(f"✅ File uploaded: {row_count:,} rows, {col_count} columns")

            # Show sample
            with st.expander("📊 Preview Data (first 5 rows)"):
                st.dataframe(df.head(), use_container_width=True)

            return df

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
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

    st.markdown("### 📋 Current Mapping Summary")

    mapping_df = pd.DataFrame([
        {"CSV Column": csv_col, "API Field": api_field}
        for csv_col, api_field in field_mapping.items()
    ])
    st.dataframe(mapping_df, use_container_width=True)

    mapped_count = len(field_mapping)
    st.info(f"✅ {mapped_count} fields mapped")


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
    st.markdown("### 2️⃣ Preview Matches (Optional)")

    # Check if identifier is mapped
    identifier_mapped = identifier_field in field_mapping.values()

    if not identifier_mapped:
        st.warning(f"⚠️ Map the identifier field '{identifier_field}' to enable preview")
        return

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("Preview how records will be matched before updating:")

    with col2:
        if st.button("🔍 Preview Matches", type="secondary"):
            with st.spinner("Previewing first 20 matches..."):
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
        st.markdown("#### Preview Results")

        preview_df = pd.DataFrame(st.session_state.preview_results)

        # Summary counts
        if 'status' in preview_df.columns:
            found_count = len(preview_df[preview_df['status'].str.contains('✅')])
            fuzzy_count = len(preview_df[preview_df['status'].str.contains('⚠️')])
            not_found_count = len(preview_df[preview_df['status'].str.contains('❌')])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Found", found_count)
            with col2:
                st.metric("⚠️ Fuzzy Match", fuzzy_count)
            with col3:
                st.metric("❌ Not Found", not_found_count)

        # Show preview table
        st.dataframe(preview_df, use_container_width=True)

        if st.button("Clear Preview"):
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
    st.markdown("### 3️⃣ Execute Update")

    # Dry run option
    dry_run_mode = st.checkbox(
        "🧪 Dry Run Mode (preview only, no actual updates)",
        value=False,
        help="When enabled, simulates the update without making actual API calls"
    )

    if dry_run_mode:
        st.info("⚠️ **Dry Run Mode Active** - No actual updates will be made. Results will show what WOULD be updated.")

    # Check if identifier is mapped
    identifier_mapped = identifier_field in field_mapping.values()

    if not identifier_mapped:
        st.error(f"⚠️ Please map the identifier field '{identifier_field}' before updating")
    elif not field_mapping:
        st.error("⚠️ Please map at least one field to update")
    else:
        row_count = len(df)

        button_text = f"🧪 Preview {row_count:,} Updates" if dry_run_mode else f"{entity_icon} Update {row_count:,} Records"
        button_type = "secondary" if dry_run_mode else "primary"

        if st.button(button_text, type=button_type):
            spinner_text = f"Simulating updates for {row_count:,} {entity_type}s..." if dry_run_mode else f"Updating {row_count:,} {entity_type}s..."

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
        st.warning("🧪 **DRY RUN RESULTS** - No actual updates were made. This shows what WOULD have been updated.")

    st.subheader("📊 Update Results")

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

    # Successful updates
    if successful:
        with st.expander(f"✅ Successful Updates ({len(successful)})", expanded=True):
            success_df = pd.DataFrame(successful)
            st.dataframe(success_df, use_container_width=True)

    # Failed updates
    if failed:
        with st.expander(f"❌ Failed Updates ({len(failed)})", expanded=True):
            failed_df = pd.DataFrame(failed)
            st.dataframe(failed_df, use_container_width=True)

    # Clear results button
    if st.button("🔄 Start New Update"):
        st.session_state.update_results = None
        st.session_state.uploaded_data = None
        st.session_state.field_mapping = {}
        st.rerun()
