import streamlit as st
import pandas as pd

from src.helpers.crm import (
    test_api_connection,
    get_required_company_fields, get_optional_company_fields,
    get_required_person_fields, get_optional_person_fields,
    validate_import_data,
    detect_tag_columns, bulk_import_companies, bulk_import_persons
)
from src.helpers.mapping_utils import (
    get_current_mapping_for_field,
    export_mapping_to_json,
    import_mapping_from_json
)
from src.components.crm import render_environment_selector, render_api_configuration, render_wip_warning

st.set_page_config(
    page_title="CRM Import",
    page_icon="📥",
    layout="wide"
)

st.title("📥 CRM Import")
st.markdown("CSV/Excel-Dateien hochladen, um Firmen und Kontakte im Poool CRM über die API zu erstellen")

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
if 'import_type' not in st.session_state:
    st.session_state.import_type = 'companies'
if 'import_results' not in st.session_state:
    st.session_state.import_results = None
if 'final_tag_mappings' not in st.session_state:
    st.session_state.final_tag_mappings = {}
if 'mapping_file_processed' not in st.session_state:
    st.session_state.mapping_file_processed = False


def _update_field_mapping(field: str, selected_column: str):
    """Update field mapping for a given API field."""
    # Remove mapping if empty/none selected
    if not selected_column or not selected_column.strip() or selected_column.lower() == "select":
        if field in st.session_state.field_mapping:
            del st.session_state.field_mapping[field]
    else:
        # Map API field to CSV column (allows multiple API fields to use same CSV column)
        st.session_state.field_mapping[field] = selected_column

def _on_field_mapping_change(field: str):
    """Callback function triggered when a field mapping selectbox changes."""
    # Get the new value from session state (Streamlit stores widget values there)
    widget_key = f"selectbox_{field}"
    if widget_key in st.session_state:
        selected_column = st.session_state[widget_key]
        _update_field_mapping(field, selected_column)

def _get_field_examples():
    """Get examples and descriptions for each field."""
    return {
        # Company fields
        'name': 'Company display name (e.g., "Acme Corp")',
        'legal_name': 'Official registered name (e.g., "Acme Corporation GmbH")',
        'street': 'Street name only (e.g., "Hauptstraße")',
        'house_number': 'Building number (e.g., "15", "42A")',
        'zip_code': 'Postal code (e.g., "10115", "SW1A 1AA")',
        'city': 'City name (e.g., "Berlin", "London")',
        'phone': 'Phone with country code (e.g., "+49 30 12345678")',
        'email': 'Contact email (e.g., "info@company.com")',
        'website': 'Website URL (e.g., "www.company.com")',
        'tax_number': 'Tax identification (e.g., "12345678")',
        'vat_number': 'VAT ID (e.g., "DE123456789")',
        'notes': 'Free text comments or remarks',

        # Relationship fields
        'is_client': 'true/false or any value = true, empty = false',
        'is_supplier': 'true/false or any value = true, empty = false',

        # Client-specific fields
        'customer_number': 'Internal client number (e.g., "CLI-001", "C12345")',
        'payment_time_day_num': 'Payment terms in days (e.g., "30", "14")',
        'comment_client': 'Client-specific notes and comments',
        'send_bill_to_email_to': 'Invoice email address (e.g., "billing@client.com")',
        'reference_number_required': '1/0 or true/false - require reference on invoices',
        'dunning_blocked': '1/0 or true/false - block dunning/reminder process',

        # Supplier-specific fields
        'comment_supplier': 'Supplier-specific notes and comments',
        'discount_day_num': 'Early payment discount period in days (e.g., "14")',
        'discount_percentage': 'Early payment discount rate (e.g., "2.5", "1.0")',

        # German/EU specific
        'datev_account': 'DATEV accounting code (e.g., "1200", "KR001")',
        'leitweg_id': 'German e-invoicing Leitweg ID (e.g., "99ZZ-123456789")',
        'datev_is_client_collection': '1/0 - DATEV client collection flag',

        # Person fields
        'firstname': 'Given name (e.g., "John")',
        'lastname': 'Family name (e.g., "Smith")',
        'position': 'Job title (e.g., "CEO", "Project Manager")',
        'department': 'Department name (e.g., "Sales", "Development")',
        'salutation': 'Title/greeting (e.g., "Mr.", "Ms.", "Dr.")',
        'title': 'Academic/professional title (e.g., "Dr.", "Prof.")',
        'middle_name': 'Middle name or initial (e.g., "Michael")',
        'company': 'Company name they work for'
    }

def _render_field_mapping_section(required_fields: list, optional_fields: list, csv_columns: list):
    """Render the complete field mapping section with organized tabs for different field categories."""
    from src.helpers.crm import get_company_field_tabs, get_company_field_labels
    from src.components.crm import FieldMappingBuilder

    # Get tab configuration and labels
    field_tabs = get_company_field_tabs()
    field_labels = get_company_field_labels()

    # Get field examples
    examples = _get_field_examples()

    # Create FieldMappingBuilder with labels
    builder = FieldMappingBuilder(
        csv_columns=csv_columns,
        field_mapping_key='field_mapping',
        field_examples=examples,
        field_labels=field_labels,
        on_change_callback=_on_field_mapping_change
    )

    # Create tabs (7 field tabs + 1 tag management tab)
    tab_names = list(field_tabs.keys()) + ["🏷️ Tag-Verwaltung"]
    tabs = st.tabs(tab_names)

    # Render each field tab
    for idx, (tab_name, fields) in enumerate(field_tabs.items()):
        with tabs[idx]:
            # Use 2-column layout
            if len(fields) > 1:
                cols = st.columns(2)
                for field_idx, field in enumerate(fields):
                    col_idx = field_idx % 2
                    with cols[col_idx]:
                        builder.render_field_selectbox(field, key_prefix=f"{tab_name.lower().replace(' ', '_')}_{col_idx}", use_callback=True)
            else:
                # Single field - no columns needed
                for field in fields:
                    builder.render_field_selectbox(field, key_prefix=tab_name.lower().replace(' ', '_'), use_callback=True)

    # Tag Management tab (last tab)
    tag_tab_idx = len(field_tabs)
    with tabs[tag_tab_idx]:
        st.markdown("**🏷️ Tag-Verwaltung & Zuweisung**")
        st.info("💡 Tags helfen, Ihre Firmen zu kategorisieren und zu organisieren. Konfigurieren Sie die automatische Tag-Erkennung oder weisen Sie Tag-Spalten manuell zu.")

        if uploaded_file is not None and df is not None:
            # Auto-detection section
            st.markdown("### 🔍 **Automatische Erkennungsergebnisse**")
            tag_mappings = detect_tag_columns(df)

            if tag_mappings:
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("**🎯 Erkannte Tag-Spalten**")
                    for csv_col, format_type in tag_mappings.items():
                        format_description = {
                            'comma_separated': '📝 Kommagetrennt (z.B. "VIP, Enterprise")',
                            'single_tag': '🏷️ Ein Tag pro Spalte',
                            'one_hot': '☑️ Boolean (1/0, true/false)'
                        }.get(format_type, '❓ Unbekanntes Format')

                        st.write(f"• **{csv_col}**: {format_description}")

                with col2:
                    st.markdown("**👀 Tag-Vorschau**")
                    if len(df) > 0:
                        # Show sample tag values from first few rows (optimized for large files)
                        total_rows = len(df)
                        if total_rows > 10000:
                            st.caption(f"📊 Großer Datensatz ({total_rows:,} Zeilen). Zeige Beispiel von den ersten 3 Zeilen.")
                            sample_rows = 3
                        else:
                            sample_rows = min(3, total_rows)

                        for i in range(sample_rows):
                            row_tags = []
                            for csv_col, format_type in tag_mappings.items():
                                value = df.iloc[i][csv_col] if csv_col in df.columns else ""
                                if pd.notna(value) and str(value).strip():
                                    if format_type == 'comma_separated':
                                        tags = [tag.strip().strip('"').strip("'") for tag in str(value).split(',')]
                                        row_tags.extend([tag for tag in tags if tag])
                                    elif format_type == 'single_tag':
                                        row_tags.append(str(value).strip())
                                    elif format_type == 'one_hot' and str(value).lower() in ['1', 'true', 'yes']:
                                        # Extract tag name from column (remove 'Tag_' prefix)
                                        tag_name = csv_col.replace('Tag_', '').replace('tag_', '').replace('_', ' ').title()
                                        row_tags.append(tag_name)

                            if row_tags:
                                company_name = df.iloc[i].get('name', df.iloc[i].get('Company Name', f'Row {i+1}'))
                                st.write(f"**{company_name}**: {', '.join(set(row_tags))}")

            st.markdown("---")

            # Manual assignment section
            st.markdown("### 🎛️ **Manuelle Tag-Spaltenzuweisung**")
            st.info("💡 Überschreiben Sie die automatische Erkennung oder fügen Sie fehlende Spalten hinzu, indem Sie CSV-Spalten manuell Tag-Formaten zuordnen.")

            # Initialize session state for manual tag mappings
            if 'manual_tag_mappings' not in st.session_state:
                st.session_state.manual_tag_mappings = {}

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.markdown("**📝 Kommagetrennte Tags**")
                st.caption("Spalten mit mehreren durch Kommas getrennten Tags")

                # Multi-select for comma-separated columns
                comma_cols = st.multiselect(
                    "Kommagetrennte Tag-Spalten auswählen:",
                    options=[col for col in csv_columns if col != "Select"],
                    default=[col for col, fmt in tag_mappings.items() if fmt == 'comma_separated'],
                    key="comma_tag_cols"
                )

                for col in comma_cols:
                    st.session_state.manual_tag_mappings[col] = 'comma_separated'

            with col2:
                st.markdown("**🏷️ Einzel-Tag-Spalten**")
                st.caption("Spalten mit einem Tag pro Zelle")

                single_cols = st.multiselect(
                    "Einzel-Tag-Spalten auswählen:",
                    options=[col for col in csv_columns if col != "Select"],
                    default=[col for col, fmt in tag_mappings.items() if fmt == 'single_tag'],
                    key="single_tag_cols"
                )

                for col in single_cols:
                    st.session_state.manual_tag_mappings[col] = 'single_tag'

            with col3:
                st.markdown("**☑️ One-Hot-Codiert**")
                st.caption("Boolean-Spalten (1/0, true/false)")

                onehot_cols = st.multiselect(
                    "One-Hot-Tag-Spalten auswählen:",
                    options=[col for col in csv_columns if col != "Select"],
                    default=[col for col, fmt in tag_mappings.items() if fmt == 'one_hot'],
                    key="onehot_tag_cols"
                )

                for col in onehot_cols:
                    st.session_state.manual_tag_mappings[col] = 'one_hot'

            # Combined mappings (auto + manual)
            final_tag_mappings = {**tag_mappings, **st.session_state.manual_tag_mappings}

            if final_tag_mappings:
                st.markdown("---")
                st.markdown("### ✅ **Finale Tag-Konfiguration**")

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("**📊 Zusammenfassung**")
                    format_counts = {}
                    for fmt in final_tag_mappings.values():
                        format_counts[fmt] = format_counts.get(fmt, 0) + 1

                    for fmt, count in format_counts.items():
                        format_emoji = {'comma_separated': '📝', 'single_tag': '🏷️', 'one_hot': '☑️'}.get(fmt, '❓')
                        st.write(f"{format_emoji} **{fmt.replace('_', ' ').title()}**: {count} Spalten")

                with col2:
                    st.markdown("**🗂️ Alle Tag-Spalten**")
                    for csv_col, format_type in final_tag_mappings.items():
                        format_emoji = {'comma_separated': '📝', 'single_tag': '🏷️', 'one_hot': '☑️'}.get(format_type, '❓')
                        st.write(f"{format_emoji} {csv_col}")

                # Store final mappings for import process
                st.session_state.final_tag_mappings = final_tag_mappings

            else:
                st.warning("⚠️ Keine Tag-Spalten konfiguriert. Tags werden beim Import nicht zugewiesen.")
                st.session_state.final_tag_mappings = {}

        else:
            st.info("📤 **Laden Sie eine CSV-Datei hoch**, um die Tag-Spaltenerkennung und -zuweisung zu konfigurieren.")

            # Show supported formats when no file is uploaded
            st.markdown("### 📋 **Unterstützte Tag-Formate**")
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.markdown("**📝 Kommagetrennt**")
                st.code('Tags\n"VIP, Enterprise, Marketing"\n"Client, Premium"')

            with col2:
                st.markdown("**🏷️ Einzel-Tag**")
                st.code('Primary Tag,Category\nVIP,Technology\nEnterprise,Marketing')

            with col3:
                st.markdown("**☑️ One-Hot-Codiert**")
                st.code('Tag_VIP,Tag_Enterprise\n1,0\n0,1')

def _execute_import_with_progress(import_type: str, row_count: int):
    """Execute the import process with progress tracking."""
    import time
    start_time = time.time()

    progress_bar = st.progress(0)
    status_text = st.empty()

    # Show realistic progress estimates based on file size
    if row_count > 5000:
        status_text.text(f"🚀 Starting import of {row_count:,} rows... This may take several minutes.")
    elif row_count > 1000:
        status_text.text(f"🚀 Starting import of {row_count:,} rows... Estimated time: 1-2 minutes.")
    else:
        status_text.text(f"🚀 Starting import of {row_count:,} rows...")

    try:
        status_text.text("Validating data and preparing import...")
        progress_bar.progress(10)

        if import_type == 'companies':
            status_text.text(f"Creating {row_count} companies...")
            progress_bar.progress(20)
            successful, failed = bulk_import_companies(
                st.session_state.crm_api_key,
                st.session_state.uploaded_data,
                st.session_state.field_mapping,
                st.session_state.get('crm_environment', 'production'),
                st.session_state.get('crm_custom_url'),
                st.session_state.get('final_tag_mappings', {})
            )
        else:
            status_text.text(f"Creating {row_count} persons...")
            progress_bar.progress(20)
            successful, failed = bulk_import_persons(
                st.session_state.crm_api_key,
                st.session_state.uploaded_data,
                st.session_state.field_mapping,
                st.session_state.get('crm_environment', 'production'),
                st.session_state.get('crm_custom_url'),
                st.session_state.get('final_tag_mappings', {})
            )

        progress_bar.progress(90)
        status_text.text("Processing results...")

        st.session_state.import_results = {
            'successful': successful,
            'failed': failed,
            'import_type': import_type
        }

        progress_bar.progress(100)

        # Calculate and display completion time
        end_time = time.time()
        duration = end_time - start_time
        if duration > 60:
            duration_text = f"{duration/60:.1f} minutes"
        else:
            duration_text = f"{duration:.1f} seconds"

        status_text.text(f"✅ Import complete! ({duration_text})")

        # Clear progress indicators after a brief pause
        time.sleep(2)
        progress_bar.empty()
        status_text.empty()

        st.rerun()

    except Exception as e:
        st.error(f"Import failed: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def _check_for_internal_duplicates(df, field_mapping: dict, import_type: str) -> list:
    """Check for potential duplicates within the uploaded data."""
    warnings = []

    try:
        if import_type == 'companies':
            # Check for duplicate company names
            name_col = None
            for csv_col, api_field in field_mapping.items():
                if api_field == 'name':
                    name_col = csv_col
                    break

            if name_col and name_col in df.columns:
                # Find duplicate names (case-insensitive)
                duplicate_names = df[df[name_col].str.lower().duplicated(keep=False)]
                if not duplicate_names.empty:
                    duplicate_count = len(duplicate_names)
                    warnings.append(f"Warning: Found {duplicate_count} rows with duplicate company names. This may create duplicate records.")

        else:  # persons
            # Check for duplicate person combinations (firstname + lastname + email)
            firstname_col = lastname_col = email_col = None
            for csv_col, api_field in field_mapping.items():
                if api_field == 'firstname':
                    firstname_col = csv_col
                elif api_field == 'lastname':
                    lastname_col = csv_col
                elif api_field == 'email':
                    email_col = csv_col

            # Check combinations that could indicate duplicates
            if firstname_col and lastname_col:
                # Create full name for duplicate checking
                df_temp = df.copy()
                df_temp['full_name'] = df_temp[firstname_col].astype(str) + ' ' + df_temp[lastname_col].astype(str)
                duplicate_names = df_temp[df_temp['full_name'].str.lower().duplicated(keep=False)]
                if not duplicate_names.empty:
                    warnings.append(f"Warning: Found {len(duplicate_names)} rows with duplicate person names (firstname + lastname).")

            if email_col and email_col in df.columns:
                # Check for duplicate emails
                duplicate_emails = df[df[email_col].str.lower().duplicated(keep=False)]
                if not duplicate_emails.empty:
                    warnings.append(f"Warning: Found {len(duplicate_emails)} rows with duplicate email addresses.")

    except Exception as e:
        # If duplicate checking fails, don't block the process
        warnings.append(f"Warning: Could not check for duplicates: {str(e)}")

    return warnings

def _display_validation_messages(validation_errors: list):
    """Display validation warnings and errors."""
    warnings = [msg for msg in validation_errors if msg.startswith("Warning:")]
    errors = [msg for msg in validation_errors if not msg.startswith("Warning:")]

    if warnings:
        for warning in warnings:
            st.warning(warning[9:])  # Remove "Warning: " prefix

    if errors:
        for error in errors:
            st.error(error)

col1, col2 = st.columns([1, 2])

with col1:
    api_key, is_connected = render_api_configuration(test_api_connection)

with col2:
    st.subheader("📁 Datei-Upload & Typ")

    if st.session_state.crm_api_key:
        import_type = st.selectbox(
            "Import-Typ",
            options=['companies', 'persons'],
            index=0 if st.session_state.import_type == 'companies' else 1,
            help="Wählen Sie aus, was Sie importieren möchten"
        )
        st.session_state.import_type = import_type

        uploaded_file = st.file_uploader(
            f"CSV- oder Excel-Datei für {import_type} auswählen",
            type=['csv', 'xlsx', 'xls'],
            help=f"Datei mit {import_type}-Daten hochladen"
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, dtype=str)
                else:
                    df = pd.read_excel(uploaded_file, dtype=str)

                st.session_state.uploaded_data = df
                # Don't clear field_mapping on file upload - user might want to keep mappings
                row_count = len(df)
                col_count = len(df.columns)
                st.success(f"✅ Datei hochgeladen: {row_count:,} Zeilen, {col_count} Spalten")

                # Show appropriate preview based on file size
                preview_expanded = row_count <= 100  # Only expand by default for small files
                with st.expander("📋 Datenvorschau", expanded=preview_expanded):
                    if row_count > 1000:
                        st.info(f"📊 Große Datei erkannt ({row_count:,} Zeilen). Zeige erste 10 Zeilen zur Performance.")
                        preview_rows = 10
                    elif row_count > 100:
                        st.info(f"📊 Mittlere Datei ({row_count:,} Zeilen). Zeige erste 20 Zeilen.")
                        preview_rows = 20
                    else:
                        preview_rows = min(row_count, 50)

                    st.dataframe(df.head(preview_rows), use_container_width=True)

            except Exception as e:
                st.error(f"❌ Fehler beim Lesen der Datei: {str(e)}")
    else:
        st.info("Bitte testen Sie zuerst die API-Verbindung")

if st.session_state.uploaded_data is not None:
    st.subheader("🔄 Spaltenzuordnung")

    if st.session_state.import_type == 'companies':
        required_fields = get_required_company_fields()
        optional_fields = get_optional_company_fields()
        st.info("📋 **Firmenfelder**: Ordnen Sie Ihre CSV-Spalten den Poool-Firmenfeldern zu")
    else:
        required_fields = get_required_person_fields()
        optional_fields = get_optional_person_fields()
        st.info("👤 **Personenfelder**: Ordnen Sie Ihre CSV-Spalten den Poool-Personenfeldern zu")

    csv_columns = [''] + list(st.session_state.uploaded_data.columns)
    all_fields = required_fields + optional_fields

    # Mapping import/export section
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        # Download mapping as JSON
        if st.session_state.field_mapping or st.session_state.get('final_tag_mappings'):
            json_str = export_mapping_to_json(
                st.session_state.field_mapping,
                st.session_state.get('final_tag_mappings', {}),
                st.session_state.get('manual_tag_mappings', {})
            )
            st.download_button(
                label="📥 Zuordnung herunterladen",
                data=json_str,
                file_name=f"mapping_config_{st.session_state.import_type}.json",
                mime="application/json",
                help="Aktuelle Zuordnungskonfiguration als JSON herunterladen"
            )
        else:
            st.button("📥 Zuordnung herunterladen", disabled=True, help="Keine Zuordnungen zum Exportieren")

    with col2:
        # Upload mapping from JSON
        uploaded_mapping = st.file_uploader(
            "Zuordnung hochladen",
            type=['json'],
            help="Eine zuvor gespeicherte Zuordnungskonfiguration hochladen",
            key="mapping_upload",
            label_visibility="collapsed"
        )

        # Process uploaded file only once
        if uploaded_mapping is not None and not st.session_state.mapping_file_processed:
            try:
                json_content = uploaded_mapping.read().decode('utf-8')
                imported_config, messages = import_mapping_from_json(json_content, csv_columns)

                # Apply imported configuration to session state
                if imported_config['field_mapping']:
                    st.session_state.field_mapping = imported_config['field_mapping']
                if imported_config['final_tag_mappings']:
                    st.session_state.final_tag_mappings = imported_config['final_tag_mappings']
                if imported_config['manual_tag_mappings']:
                    st.session_state.manual_tag_mappings = imported_config['manual_tag_mappings']

                # Display messages and check for errors
                has_errors = False
                for message in messages:
                    if message.startswith("Success:") or message.startswith("Erfolg:"):
                        st.success(message.split(":", 1)[1].strip())
                    elif message.startswith("Warning:") or message.startswith("Warnung:"):
                        st.warning(message.split(":", 1)[1].strip())
                    elif message.startswith("Error:") or message.startswith("Fehler:"):
                        st.error(message.split(":", 1)[1].strip())
                        has_errors = True

                # Mark as processed if import was successful (no errors and got some mappings)
                if not has_errors and imported_config['field_mapping']:
                    st.session_state.mapping_file_processed = True
                    st.rerun()

            except Exception as e:
                st.error(f"Failed to read mapping file: {str(e)}")

        # Reset flag when file is removed
        if uploaded_mapping is None and st.session_state.mapping_file_processed:
            st.session_state.mapping_file_processed = False

    with col3:
        if st.button("🗑️ Alle löschen", help="Alle Feldzuordnungen entfernen"):
            st.session_state.field_mapping = {}
            st.session_state.final_tag_mappings = {}
            st.session_state.manual_tag_mappings = {}
            st.rerun()

    with col4:
        mapped_count = len([v for v in st.session_state.field_mapping.values() if v and v != ""])
        st.metric("Zugeordnet", f"{mapped_count}/{len(all_fields)}")

    # Render the field mapping section using refactored helper functions
    _render_field_mapping_section(required_fields, optional_fields, csv_columns)

    with st.expander("📋 Aktuelle Zuordnung", expanded=False):
        if st.session_state.field_mapping:
            mapping_df = pd.DataFrame([
                {"CSV-Spalte": csv_col, "API-Feld": api_field}
                for csv_col, api_field in st.session_state.field_mapping.items()
                if api_field
            ])
            st.dataframe(mapping_df, use_container_width=True, hide_index=True)
        else:
            st.info("Noch keine Zuordnungen konfiguriert")

    # Check if ALL required fields are mapped
    mapped_required_fields = set(
        api_field for csv_col, api_field in st.session_state.field_mapping.items()
        if api_field in required_fields
    )
    required_mapped = len(mapped_required_fields) == len(required_fields)

    st.subheader("📊 Import-Vorschau")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Zu verarbeitende Zeilen", len(st.session_state.uploaded_data))
    with col2:
        st.metric("Zugeordnete Felder", len([x for x in st.session_state.field_mapping.values() if x]))
    with col3:
        if required_mapped:
            st.metric("Status", "✅ Bereit", delta="Pflichtfelder zugeordnet")
        else:
            st.metric("Status", "⚠️ Pflichtfelder fehlen", delta="Pflichtfelder zuordnen")

    if required_mapped:
        # Pre-validation before showing import button
        try:
            is_valid, validation_errors = validate_import_data(
                st.session_state.uploaded_data,
                st.session_state.field_mapping,
                st.session_state.import_type
            )
        except:
            # Fallback validation if function import fails
            is_valid = True
            validation_errors = []

        # Check for potential duplicates within the uploaded data
        duplicate_warnings = _check_for_internal_duplicates(
            st.session_state.uploaded_data,
            st.session_state.field_mapping,
            st.session_state.import_type
        )
        validation_errors.extend(duplicate_warnings)

        # Show validation warnings and errors
        _display_validation_messages(validation_errors)

        # Only show import button if validation passes
        if is_valid:
            row_count = len(st.session_state.uploaded_data)

            # Show performance warning for large files
            if row_count > 5000:
                st.warning(f"⏳ Sehr große Datei ({row_count:,} Zeilen). Import kann mehrere Minuten dauern. Bitte haben Sie Geduld und aktualisieren Sie die Seite nicht.")
            elif row_count > 1000:
                st.info(f"📊 Große Datei ({row_count:,} Zeilen). Import kann 1-2 Minuten dauern.")
            elif row_count > 500:
                st.info(f"📊 Mittlere Datei ({row_count:,} Zeilen). Sollte in unter einer Minute fertig sein.")

            if st.button(f"🚀 {st.session_state.import_type.title()} erstellen", type="primary"):
                _execute_import_with_progress(st.session_state.import_type, row_count)
        else:
            st.error("⚠️ Bitte beheben Sie die Validierungsfehler oben, bevor Sie importieren.")

# Display import results
# noinspection PyUnreachableCode
if st.session_state.import_results:
    results = st.session_state.import_results
    st.subheader("📊 Import-Ergebnisse")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Erfolgreich", len(results['successful']))
    with col2:
        st.metric("❌ Fehlgeschlagen", len(results['failed']))
    with col3:
        total = len(results['successful']) + len(results['failed'])
        success_rate = (len(results['successful']) / total * 100) if total > 0 else 0
        st.metric("Erfolgsquote", f"{success_rate:.1f}%")

    # Show successful imports
    if results['successful']:
        success_count = len(results['successful'])
        expanded = success_count <= 100  # Only expand by default for small results

        with st.expander("✅ Erfolgreiche Imports", expanded=expanded):
            success_data = []

            # Limit display for large results sets
            if success_count > 1000:
                st.info(f"📊 Großer Import ({success_count:,} erfolgreich). Zeige erste 100 zur Performance.")
                items_to_show = results['successful'][:100]
            elif success_count > 500:
                st.info(f"📊 Mittlerer Import ({success_count:,} erfolgreich). Zeige erste 200.")
                items_to_show = results['successful'][:200]
            else:
                items_to_show = results['successful']

            for item in items_to_show:
                row_info = {"Zeile": item['row']}
                if results['import_type'] == 'companies':
                    row_info.update({
                        "Name": item['created'].get('name', 'N/A'),
                        "ID": item['created'].get('id', 'N/A')
                    })
                else:
                    row_info.update({
                        "Vorname": item['created'].get('firstname', 'N/A'),
                        "Nachname": item['created'].get('lastname', 'N/A'),
                        "ID": item['created'].get('id', 'N/A')
                    })
                success_data.append(row_info)

            if success_data:
                st.dataframe(pd.DataFrame(success_data), use_container_width=True, hide_index=True)

                if len(items_to_show) < success_count:
                    st.caption(f"Zeige {len(items_to_show)} von {success_count:,} erfolgreichen Imports")


    # Show failed imports with enhanced context
    if results['failed']:
        failed_count = len(results['failed'])
        expanded = failed_count <= 50  # Only expand by default for small failure sets

        with st.expander("❌ Fehlgeschlagene Imports", expanded=expanded):
            st.warning(f"💡 **Tipp**: Überprüfen Sie die Daten in diesen Zeilen und beheben Sie die Probleme, bevor Sie erneut importieren.")

            # Limit display for large failure sets
            if failed_count > 100:
                st.info(f"📊 Große Fehleranzahl ({failed_count:,} fehlgeschlagen). Zeige erste 50 zur Performance.")
                items_to_show = results['failed'][:50]
            else:
                items_to_show = results['failed']

            failure_data = []
            for item in items_to_show:
                error_msg = item['error']
                suggestions = []

                # Add contextual suggestions based on error type
                if 'Missing required field' in error_msg:
                    suggestions.append("Prüfen Sie die Spaltenzuordnung für Pflichtfelder")
                elif 'email' in error_msg.lower():
                    suggestions.append("Überprüfen Sie das E-Mail-Format (z.B. benutzer@domain.com)")
                elif 'phone' in error_msg.lower():
                    suggestions.append("Fügen Sie Ländervorwahl hinzu (z.B. +49 30 12345678)")
                elif 'duplicate' in error_msg.lower():
                    suggestions.append("Dieser Datensatz existiert möglicherweise bereits im CRM")
                elif '400' in error_msg or 'Bad Request' in error_msg:
                    suggestions.append("Prüfen Sie Datenformat und Pflichtfelder")
                elif '401' in error_msg or 'Unauthorized' in error_msg:
                    suggestions.append("Überprüfen Sie, ob der API-Schlüssel korrekt ist")
                elif '403' in error_msg or 'Forbidden' in error_msg:
                    suggestions.append("Prüfen Sie API-Berechtigungen")

                # Show sample data from the failed row
                sample_data = []
                if 'data' in item and item['data']:
                    # Show first few fields as context
                    for k, v in list(item['data'].items())[:3]:
                        sample_data.append(f"{k}: {v}")

                failure_data.append({
                    "Zeile": item['row'],
                    "Fehler": error_msg,
                    "Beispieldaten": " | ".join(sample_data) if sample_data else "N/A",
                    "Vorschlag": " | ".join(suggestions) if suggestions else "Datenformat überprüfen"
                })

            if failure_data:
                st.dataframe(pd.DataFrame(failure_data), use_container_width=True, hide_index=True)

                if len(items_to_show) < failed_count:
                    st.caption(f"Zeige {len(items_to_show)} von {failed_count:,} fehlgeschlagenen Imports")

                # Common error patterns summary
                error_types = {}
                for item in results['failed']:
                    error = item['error']
                    if 'Missing required field' in error:
                        error_types['Fehlende Pflichtfelder'] = error_types.get('Fehlende Pflichtfelder', 0) + 1
                    elif any(code in error for code in ['400', '401', '403', '500']):
                        error_types['API-Fehler'] = error_types.get('API-Fehler', 0) + 1
                    else:
                        error_types['Datenformat-Probleme'] = error_types.get('Datenformat-Probleme', 0) + 1

                if error_types:
                    st.subheader("📊 Fehlerzusammenfassung")
                    cols = st.columns(len(error_types))
                    for i, (error_type, count) in enumerate(error_types.items()):
                        cols[i].metric(error_type, count)

    if st.button("🔄 Ergebnisse löschen"):
        st.session_state.import_results = None
        st.rerun()

st.markdown("---")
st.markdown("💡 **Tipp:** Überprüfen Sie die Zuordnung sorgfältig vor dem Import, um Fehler zu vermeiden")
