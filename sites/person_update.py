import streamlit as st
import pandas as pd

from src.helpers.crm import (
    test_api_connection,
    get_required_person_fields, get_optional_person_fields,
    bulk_update_persons,
    preview_person_matches
)
from src.components.crm_ui import (
    render_environment_selector,
    render_api_configuration,
    render_file_uploader,
    render_mapping_summary,
    render_preview_matches,
    render_update_execution,
    render_update_results,
    render_wip_warning
)

st.set_page_config(
    page_title="Person Update Tool",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Person Update Tool")
st.markdown("Update existing persons in Poool CRM via API")

render_wip_warning()

# Environment Toggle
st.markdown("---")
environment, custom_url = render_environment_selector()
st.markdown("---")

# Local page-specific session state (not for API/environment)
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'field_mapping' not in st.session_state:
    st.session_state.field_mapping = {}
if 'identifier_field' not in st.session_state:
    st.session_state.identifier_field = 'id'
if 'update_results' not in st.session_state:
    st.session_state.update_results = None
if 'preview_results' not in st.session_state:
    st.session_state.preview_results = None

# API Configuration and File Upload
col1, col2 = st.columns([1, 2])

with col1:
    api_key, is_connected = render_api_configuration(test_api_connection)

with col2:
    df = render_file_uploader("update")

# Main update workflow
if st.session_state.uploaded_data is not None and st.session_state.crm_api_key:
    st.markdown("---")
    st.subheader("🎯 Update Configuration")

    df = st.session_state.uploaded_data
    csv_columns = [''] + list(df.columns)

    # Identifier Selection
    st.markdown("### 1️⃣ Select Identifier Field")
    st.markdown("Choose which field to use for matching existing records:")

    col1, col2 = st.columns(2)

    with col1:
        identifier_field = st.selectbox(
            "Match records by:",
            options=['id', 'email', 'firstname', 'lastname'],
            help="Field used to identify existing persons in the CRM"
        )
        st.session_state.identifier_field = identifier_field

    with col2:
        st.info(f"📌 Identifier: **{identifier_field}**\n\nMake sure to map this field in the next step!")

    # Field Mapping
    st.markdown("### 2️⃣ Map Fields to Update")
    st.markdown("Map CSV columns to API fields. Only mapped fields will be updated.")

    # Get all available fields
    all_fields = get_required_person_fields() + get_optional_person_fields()

    # Organize fields by category
    tabs = st.tabs(["Core Fields", "Contact Fields", "Additional Info"])

    with tabs[0]:
        st.markdown("**Person Core Fields**")
        core_fields = ['firstname', 'lastname', 'middlename', 'nickname',
                      'salutation', 'title', 'position', 'function', 'department']

        for field in core_fields:
            if field in all_fields:
                current_mapping = next((col for col, f in st.session_state.field_mapping.items() if f == field), '')
                selected = st.selectbox(
                    f"{field}",
                    options=csv_columns,
                    index=csv_columns.index(current_mapping) if current_mapping in csv_columns else 0,
                    key=f"update_core_{field}"
                )
                if selected and selected != '':
                    st.session_state.field_mapping[selected] = field
                elif current_mapping in st.session_state.field_mapping:
                    del st.session_state.field_mapping[current_mapping]

    with tabs[1]:
        st.markdown("**Contact Information**")

        for field in ['email', 'phone', 'company_id', 'company_subsidiary_id']:
            current_mapping = next((col for col, f in st.session_state.field_mapping.items() if f == field), '')
            selected = st.selectbox(
                f"{field}",
                options=csv_columns,
                index=csv_columns.index(current_mapping) if current_mapping in csv_columns else 0,
                key=f"update_contact_{field}"
            )
            if selected and selected != '':
                st.session_state.field_mapping[selected] = field
            elif current_mapping in st.session_state.field_mapping:
                del st.session_state.field_mapping[current_mapping]

    with tabs[2]:
        st.markdown("**Additional Information**")

        for field in ['maiden_name', 'additional_information_a',
                     'additional_information_b', 'additional_information_c', 'tags']:
            current_mapping = next((col for col, f in st.session_state.field_mapping.items() if f == field), '')
            selected = st.selectbox(
                f"{field}",
                options=csv_columns,
                index=csv_columns.index(current_mapping) if current_mapping in csv_columns else 0,
                key=f"update_additional_{field}"
            )
            if selected and selected != '':
                st.session_state.field_mapping[selected] = field
            elif current_mapping in st.session_state.field_mapping:
                del st.session_state.field_mapping[current_mapping]

    # Show current mapping summary
    render_mapping_summary(st.session_state.field_mapping)

    # Preview Matches
    render_preview_matches(df, st.session_state.field_mapping, st.session_state.identifier_field,
                          preview_person_matches, entity_type="person")

    # Execute Update
    render_update_execution(df, st.session_state.field_mapping, st.session_state.identifier_field,
                           bulk_update_persons, entity_type="person", entity_icon="👤")

# Show Results
render_update_results(st.session_state.get('update_results'))
