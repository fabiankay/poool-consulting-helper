import streamlit as st
import pandas as pd

from src.helpers.crm import (
    test_api_connection,
    get_required_company_fields, get_optional_company_fields,
    get_client_fields, get_supplier_fields,
    bulk_update_companies,
    preview_company_matches
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
    page_title="CRM Aktualisierung",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 CRM Aktualisierung")
st.markdown("Bestehende Firmen im Poool CRM über die API aktualisieren")

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
    st.subheader("🎯 Aktualisierungskonfiguration")

    df = st.session_state.uploaded_data
    csv_columns = [''] + list(df.columns)

    # Identifier Selection
    st.markdown("### 1️⃣ Identifikationsfeld auswählen")
    st.markdown("Wählen Sie, welches Feld zum Abgleich bestehender Datensätze verwendet werden soll:")

    col1, col2 = st.columns(2)

    with col1:
        identifier_field = st.selectbox(
            "Datensätze abgleichen nach:",
            options=['id', 'name', 'customer_number'],
            help="Feld zum Identifizieren bestehender Firmen im CRM"
        )
        st.session_state.identifier_field = identifier_field

    with col2:
        st.info(f"📌 Identifikator: **{identifier_field}**\n\nStellen Sie sicher, dass Sie dieses Feld im nächsten Schritt zuordnen!")

    # Field Mapping
    st.markdown("### 2️⃣ Felder zum Aktualisieren zuordnen")
    st.markdown("Ordnen Sie CSV-Spalten den API-Feldern zu. Nur zugeordnete Felder werden aktualisiert.")

    # Get all available fields
    all_fields = get_required_company_fields() + get_optional_company_fields()
    client_fields = get_client_fields()
    supplier_fields = get_supplier_fields()

    # Organize fields by category
    tabs = st.tabs(["Kernfelder", "Kundenfelder", "Lieferantenfelder"])

    with tabs[0]:
        st.markdown("**Firmen-Kernfelder**")
        core_fields = ['name', 'name_legal', 'address_street', 'address_house_number',
                      'address_zip', 'address_city', 'contact_email', 'contact_phone', 'contact_website']

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
        st.markdown("**Kundenspezifische Felder** (verwendet `/clients/:id` Endpunkt)")

        for field in ['customer_number', 'payment_time_day_num', 'dunning_blocked',
                     'reference_number_required', 'datev_account']:
            current_mapping = next((col for col, f in st.session_state.field_mapping.items() if f == field), '')
            selected = st.selectbox(
                f"{field}",
                options=csv_columns,
                index=csv_columns.index(current_mapping) if current_mapping in csv_columns else 0,
                key=f"update_client_{field}"
            )
            if selected and selected != '':
                st.session_state.field_mapping[selected] = field
            elif current_mapping in st.session_state.field_mapping:
                del st.session_state.field_mapping[current_mapping]

    with tabs[2]:
        st.markdown("**Lieferantenspezifische Felder** (verwendet `/suppliers/:id` Endpunkt)")

        for field in ['discount_day_num', 'discount_percentage', 'comment_supplier']:
            current_mapping = next((col for col, f in st.session_state.field_mapping.items() if f == field), '')
            selected = st.selectbox(
                f"{field}",
                options=csv_columns,
                index=csv_columns.index(current_mapping) if current_mapping in csv_columns else 0,
                key=f"update_supplier_{field}"
            )
            if selected and selected != '':
                st.session_state.field_mapping[selected] = field
            elif current_mapping in st.session_state.field_mapping:
                del st.session_state.field_mapping[current_mapping]

    # Show current mapping summary
    render_mapping_summary(st.session_state.field_mapping)

    # Preview Matches
    render_preview_matches(df, st.session_state.field_mapping, st.session_state.identifier_field,
                          preview_company_matches, entity_type="company")

    # Execute Update
    render_update_execution(df, st.session_state.field_mapping, st.session_state.identifier_field,
                           bulk_update_companies, entity_type="company", entity_icon="🔄")

# Show Results
render_update_results(st.session_state.get('update_results'))
