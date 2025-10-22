import streamlit as st
import pandas as pd

from src.helpers.crm import (
    test_api_connection,
    get_required_company_fields, get_optional_company_fields,
    get_required_person_fields, get_optional_person_fields,
    validate_import_data,
    detect_tag_columns, bulk_import_companies, bulk_import_persons
)
from src.helpers.poool_api_client import PooolAPIClient

st.set_page_config(
    page_title="Kontakte Import Tool",
    page_icon="🐨",
    layout="wide"
)

st.title("🏢 CRM Import Tool")
st.markdown("Upload CSV/Excel files to create companies and contacts in Poool CRM via API")

# Environment Toggle
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Initialize environment in session state if not present
    if 'environment' not in st.session_state:
        st.session_state.environment = 'production'

    # Get current index safely
    try:
        current_index = ["production", "staging", "custom"].index(st.session_state.environment)
    except ValueError:
        current_index = 0
        st.session_state.environment = 'production'  # Reset to valid state

    environment = st.radio(
        "🌐 **API Environment**",
        options=["production", "staging", "custom"],
        index=current_index,
        horizontal=True,
        help="Choose whether to connect to production, staging, or custom environment"
    )

    # Update session state and rerun if changed
    if environment != st.session_state.environment:
        st.session_state.environment = environment
        st.rerun()

    # Custom URL input when custom environment is selected
    if environment == "custom":
        if 'custom_url' not in st.session_state:
            st.session_state.custom_url = ''

        custom_url = st.text_input(
            "Custom Base URL",
            value=st.session_state.custom_url,
            placeholder="https://your-sandbox.poool.rocks",
            help="Enter your custom Poool API base URL (e.g., https://your-sandbox.poool.rocks)",
            key="custom_url_input"
        )

        # Update session state only if changed
        if custom_url != st.session_state.custom_url:
            st.session_state.custom_url = custom_url
    else:
        # Clear custom URL when not using custom environment
        if st.session_state.get('custom_url'):
            st.session_state.custom_url = None

with col2:
    # Use API client to get environment info for consistent display
    try:
        dummy_client = PooolAPIClient("dummy", environment, st.session_state.get('custom_url'))
        env_info = dummy_client.environment_info

        if environment == "production":
            st.success(f"{env_info['display']} **{env_info['name']}**")
        elif environment == "staging":
            st.warning(f"{env_info['display']} **{env_info['name']}**")
        else:  # custom
            st.info(f"{env_info['display']} **{env_info['name']}**")

        st.caption(env_info['url'])
    except:
        # Fallback to manual display if client creation fails
        if environment == "production":
            st.success("🟢 **LIVE** Production")
            st.caption("app.poool.cc")
        elif environment == "staging":
            st.warning("🟡 **TEST** Staging")
            st.caption("staging-app.poool.rocks")
        else:
            st.info("🔧 **CUSTOM** Sandbox")
            st.caption("URL not configured")

with col3:
    if environment == "production":
        st.error("⚠️ **CAUTION**: Live data!")
    elif environment == "staging":
        st.info("💡 Safe testing environment")
    else:  # custom
        st.info("🧪 Sandbox environment")

st.markdown("---")

if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
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

def _get_current_mapping_for_field(field: str) -> str:
    """Get the currently mapped CSV column for a given API field."""
    for csv_col, api_field in st.session_state.field_mapping.items():
        if api_field == field:
            return csv_col
    return ''

def _export_mapping_to_json() -> str:
    """Export current mapping configuration to JSON format."""
    import json

    mapping_config = {
        "field_mapping": st.session_state.field_mapping,
        "final_tag_mappings": st.session_state.get('final_tag_mappings', {}),
        "manual_tag_mappings": st.session_state.get('manual_tag_mappings', {})
    }

    return json.dumps(mapping_config, indent=2)

def _import_mapping_from_json(json_content: str, csv_columns: list) -> tuple[bool, list[str]]:
    """
    Import mapping configuration from JSON.
    Returns (success, messages) where messages contains warnings/errors.
    """
    import json

    messages = []

    try:
        mapping_config = json.loads(json_content)

        # Validate JSON structure
        if not isinstance(mapping_config, dict):
            return False, ["Error: JSON must be an object/dictionary"]

        # Get available CSV columns (excluding empty string)
        available_columns = set(csv_columns) - {''}

        # Import field_mapping with validation
        if 'field_mapping' in mapping_config:
            field_mapping = mapping_config['field_mapping']
            matched_mappings = {}
            missing_columns = []

            for csv_col, api_field in field_mapping.items():
                if csv_col in available_columns:
                    matched_mappings[csv_col] = api_field
                else:
                    missing_columns.append(csv_col)

            st.session_state.field_mapping = matched_mappings

            if matched_mappings:
                messages.append(f"Success: Imported {len(matched_mappings)} field mappings")

            if missing_columns:
                messages.append(f"Warning: {len(missing_columns)} columns from JSON not found in CSV: {', '.join(missing_columns[:5])}")

        # Import tag mappings
        if 'final_tag_mappings' in mapping_config:
            tag_mappings = mapping_config['final_tag_mappings']
            matched_tag_mappings = {}
            missing_tag_columns = []

            for csv_col, format_type in tag_mappings.items():
                if csv_col in available_columns:
                    matched_tag_mappings[csv_col] = format_type
                else:
                    missing_tag_columns.append(csv_col)

            st.session_state.final_tag_mappings = matched_tag_mappings

            if matched_tag_mappings:
                messages.append(f"Success: Imported {len(matched_tag_mappings)} tag mappings")

            if missing_tag_columns:
                messages.append(f"Warning: {len(missing_tag_columns)} tag columns from JSON not found in CSV")

        # Import manual tag mappings
        if 'manual_tag_mappings' in mapping_config:
            manual_mappings = mapping_config['manual_tag_mappings']
            matched_manual_mappings = {}

            for csv_col, format_type in manual_mappings.items():
                if csv_col in available_columns:
                    matched_manual_mappings[csv_col] = format_type

            st.session_state.manual_tag_mappings = matched_manual_mappings

        if not messages:
            messages.append("Warning: No mappings found in JSON file")

        return True, messages

    except json.JSONDecodeError as e:
        return False, [f"Error: Invalid JSON format - {str(e)}"]
    except Exception as e:
        return False, [f"Error: Failed to import mappings - {str(e)}"]


def _update_field_mapping(field: str, selected_column: str):
    """Update field mapping, removing old mappings for the same field."""
    # Remove old mapping for this field
    for csv_col, api_field in list(st.session_state.field_mapping.items()):
        if api_field == field:
            del st.session_state.field_mapping[csv_col]

    # Add new mapping if selected (and not empty string or "Select")
    if selected_column and selected_column.strip() and selected_column.lower() != "select":
        st.session_state.field_mapping[selected_column] = field

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

def _render_field_mapping_selectbox(field: str, csv_columns: list, field_type: str):
    """Render a selectbox for field mapping with consistent logic."""
    current_mapping = _get_current_mapping_for_field(field)
    examples = _get_field_examples()

    help_text = examples.get(field, f"Map CSV column to {field}")

    # Calculate index safely
    try:
        default_index = csv_columns.index(current_mapping) if current_mapping and current_mapping in csv_columns else 0
    except (ValueError, IndexError):
        default_index = 0

    # Create unique widget key
    widget_key = f"selectbox_{field}"

    # Render selectbox with on_change callback
    st.selectbox(
        f"{field}",
        options=csv_columns,
        index=default_index,
        key=widget_key,
        help=help_text,
        on_change=_on_field_mapping_change,
        args=(field,)
    )

def _show_relationship_preview(csv_columns: list):
    """Show a preview of detected relationships based on current mapping."""
    if not st.session_state.uploaded_data.empty:
        # Get current client/supplier mappings
        client_col = _get_current_mapping_for_field('is_client')
        supplier_col = _get_current_mapping_for_field('is_supplier')

        if client_col or supplier_col:
            st.markdown("**Relationship Preview** 🔍")

            total_rows = len(st.session_state.uploaded_data)
            if total_rows > 5000:
                st.caption(f"📊 Large dataset ({total_rows:,} rows). Preview shows first 3 rows only.")

            preview_data = []
            sample_rows = st.session_state.uploaded_data.head(3)

            for idx, row in sample_rows.iterrows():
                company_name = row.get(list(st.session_state.uploaded_data.columns)[0], f"Row {idx+1}")

                # Check client status
                client_status = "❌"
                if client_col and client_col in row:
                    client_val = str(row[client_col]).strip()
                    if client_val and client_val.lower() not in ['false', '0', 'no']:
                        client_status = "✅"

                # Check supplier status
                supplier_status = "❌"
                if supplier_col and supplier_col in row:
                    supplier_val = str(row[supplier_col]).strip()
                    if supplier_val and supplier_val.lower() not in ['false', '0', 'no']:
                        supplier_status = "✅"

                preview_data.append({
                    "Company": company_name[:20] + "..." if len(str(company_name)) > 20 else company_name,
                    "Client": client_status,
                    "Supplier": supplier_status
                })

            if preview_data:
                preview_df = pd.DataFrame(preview_data)
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
        else:
            st.info("💡 Map relationship columns to see preview")

def _show_client_preview(csv_columns: list):
    """Show a preview of detected client relationships based on current mapping."""
    if not st.session_state.uploaded_data.empty:
        client_col = _get_current_mapping_for_field('is_client')

        if client_col:
            st.markdown("**Client Preview** 💼")

            preview_data = []
            sample_rows = st.session_state.uploaded_data.head(3)

            client_count = 0
            for idx, row in sample_rows.iterrows():
                company_name = row.get(list(st.session_state.uploaded_data.columns)[0], f"Row {idx+1}")

                # Check client status
                is_client = False
                if client_col and client_col in row:
                    client_val = str(row[client_col]).strip()
                    if client_val and client_val.lower() not in ['false', '0', 'no']:
                        is_client = True
                        client_count += 1

                if is_client:
                    preview_data.append({
                        "Client": company_name[:25] + "..." if len(str(company_name)) > 25 else company_name,
                        "Status": "✅ Active Client"
                    })

            if preview_data:
                preview_df = pd.DataFrame(preview_data)
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
                st.info(f"📊 Found {client_count} clients in sample data")
            else:
                st.warning("No clients detected in sample data")
        else:
            st.info("💡 Map 'is_client' column to see preview")

def _show_supplier_preview(csv_columns: list):
    """Show a preview of detected supplier relationships based on current mapping."""
    if not st.session_state.uploaded_data.empty:
        supplier_col = _get_current_mapping_for_field('is_supplier')

        if supplier_col:
            st.markdown("**Supplier Preview** 🏭")

            preview_data = []
            sample_rows = st.session_state.uploaded_data.head(3)

            supplier_count = 0
            for idx, row in sample_rows.iterrows():
                company_name = row.get(list(st.session_state.uploaded_data.columns)[0], f"Row {idx+1}")

                # Check supplier status
                is_supplier = False
                if supplier_col and supplier_col in row:
                    supplier_val = str(row[supplier_col]).strip()
                    if supplier_val and supplier_val.lower() not in ['false', '0', 'no']:
                        is_supplier = True
                        supplier_count += 1

                if is_supplier:
                    preview_data.append({
                        "Supplier": company_name[:25] + "..." if len(str(company_name)) > 25 else company_name,
                        "Status": "✅ Active Supplier"
                    })

            if preview_data:
                preview_df = pd.DataFrame(preview_data)
                st.dataframe(preview_df, use_container_width=True, hide_index=True)
                st.info(f"📊 Found {supplier_count} suppliers in sample data")
            else:
                st.warning("No suppliers detected in sample data")
        else:
            st.info("💡 Map 'is_supplier' column to see preview")

def _render_field_mapping_section(required_fields: list, optional_fields: list, csv_columns: list):
    """Render the complete field mapping section with organized tabs for different field categories."""
    # Organize fields by category
    basic_fields = []
    client_fields = []
    supplier_fields = []

    for field in optional_fields:
        if field in ['is_client', 'customer_number', 'payment_time_day_num', 'comment_client',
                    'send_bill_to_email_to', 'reference_number_required', 'dunning_blocked',
                    'datev_account', 'leitweg_id', 'datev_is_client_collection']:
            client_fields.append(field)
        elif field in ['is_supplier', 'comment_supplier', 'discount_day_num', 'discount_percentage']:
            supplier_fields.append(field)
        else:
            basic_fields.append(field)

    # Create tabs for different field categories
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Basic Info", "💼 Client Settings", "🏭 Supplier Settings", "🏷️ Tag Management"])

    with tab1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Required Fields** ⭐")
            for field in required_fields:
                _render_field_mapping_selectbox(field, csv_columns, "required")

        with col2:
            st.markdown("**Optional Company Info**")
            for field in basic_fields:
                _render_field_mapping_selectbox(field, csv_columns, "basic_optional")

    with tab2:
        st.markdown("**Client Relationship Configuration** 💼")
        st.info("💡 Configure fields for companies that are your **clients** (they pay you for services)")

        # Show relationship toggle and preview
        col1, col2 = st.columns([1, 1])
        with col1:
            # Client relationship flag
            if 'is_client' in client_fields:
                _render_field_mapping_selectbox('is_client', csv_columns, "client")
                client_fields.remove('is_client')  # Remove from list to avoid duplicate

        with col2:
            # Show client preview if flag is mapped
            _show_client_preview(csv_columns)

        # Client-specific configuration fields
        st.markdown("**Client Business Settings**")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("*Payment & Invoicing*")
            payment_fields = ['customer_number', 'payment_time_day_num', 'send_bill_to_email_to',
                            'reference_number_required', 'dunning_blocked']
            for field in payment_fields:
                if field in client_fields:
                    _render_field_mapping_selectbox(field, csv_columns, "client_payment")

        with col2:
            st.markdown("*Accounting & Compliance*")
            accounting_fields = ['comment_client', 'datev_account', 'leitweg_id', 'datev_is_client_collection']
            for field in accounting_fields:
                if field in client_fields:
                    _render_field_mapping_selectbox(field, csv_columns, "client_accounting")

    with tab3:
        st.markdown("**Supplier Relationship Configuration** 🏭")
        st.info("💡 Configure fields for companies that are your **suppliers** (you pay them for services/goods)")

        # Show relationship toggle and preview
        col1, col2 = st.columns([1, 1])
        with col1:
            # Supplier relationship flag
            if 'is_supplier' in supplier_fields:
                _render_field_mapping_selectbox('is_supplier', csv_columns, "supplier")
                supplier_fields.remove('is_supplier')  # Remove from list to avoid duplicate

        with col2:
            # Show supplier preview if flag is mapped
            _show_supplier_preview(csv_columns)

        # Supplier-specific configuration fields
        st.markdown("**Supplier Business Settings**")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("*Payment Terms*")
            for field in ['discount_day_num', 'discount_percentage']:
                if field in supplier_fields:
                    _render_field_mapping_selectbox(field, csv_columns, "supplier_payment")

        with col2:
            st.markdown("*Notes & Comments*")
            for field in ['comment_supplier']:
                if field in supplier_fields:
                    _render_field_mapping_selectbox(field, csv_columns, "supplier_notes")

    with tab4:
        st.markdown("**🏷️ Tag Management & Assignment**")
        st.info("💡 Tags help categorize and organize your companies. Configure automatic tag detection or manually assign tag columns.")

        if uploaded_file is not None and df is not None:
            # Auto-detection section
            st.markdown("### 🔍 **Auto-Detection Results**")
            tag_mappings = detect_tag_columns(df)

            if tag_mappings:
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("**🎯 Detected Tag Columns**")
                    for csv_col, format_type in tag_mappings.items():
                        format_description = {
                            'comma_separated': '📝 Comma-separated (e.g., "VIP, Enterprise")',
                            'single_tag': '🏷️ Single tag per column',
                            'one_hot': '☑️ Boolean (1/0, true/false)'
                        }.get(format_type, '❓ Unknown format')

                        st.write(f"• **{csv_col}**: {format_description}")

                with col2:
                    st.markdown("**👀 Tag Preview**")
                    if len(df) > 0:
                        # Show sample tag values from first few rows (optimized for large files)
                        total_rows = len(df)
                        if total_rows > 10000:
                            st.caption(f"📊 Large dataset ({total_rows:,} rows). Showing sample from first 3 rows.")
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
            st.markdown("### 🎛️ **Manual Tag Column Assignment**")
            st.info("💡 Override auto-detection or add missed columns by manually mapping CSV columns to tag formats.")

            # Initialize session state for manual tag mappings
            if 'manual_tag_mappings' not in st.session_state:
                st.session_state.manual_tag_mappings = {}

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.markdown("**📝 Comma-Separated Tags**")
                st.caption("Columns with multiple tags separated by commas")

                # Multi-select for comma-separated columns
                comma_cols = st.multiselect(
                    "Select comma-separated tag columns:",
                    options=[col for col in csv_columns if col != "Select"],
                    default=[col for col, fmt in tag_mappings.items() if fmt == 'comma_separated'],
                    key="comma_tag_cols"
                )

                for col in comma_cols:
                    st.session_state.manual_tag_mappings[col] = 'comma_separated'

            with col2:
                st.markdown("**🏷️ Single Tag Columns**")
                st.caption("Columns with one tag per cell")

                single_cols = st.multiselect(
                    "Select single tag columns:",
                    options=[col for col in csv_columns if col != "Select"],
                    default=[col for col, fmt in tag_mappings.items() if fmt == 'single_tag'],
                    key="single_tag_cols"
                )

                for col in single_cols:
                    st.session_state.manual_tag_mappings[col] = 'single_tag'

            with col3:
                st.markdown("**☑️ One-Hot Encoded**")
                st.caption("Boolean columns (1/0, true/false)")

                onehot_cols = st.multiselect(
                    "Select one-hot tag columns:",
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
                st.markdown("### ✅ **Final Tag Configuration**")

                col1, col2 = st.columns([1, 1])

                with col1:
                    st.markdown("**📊 Summary**")
                    format_counts = {}
                    for fmt in final_tag_mappings.values():
                        format_counts[fmt] = format_counts.get(fmt, 0) + 1

                    for fmt, count in format_counts.items():
                        format_emoji = {'comma_separated': '📝', 'single_tag': '🏷️', 'one_hot': '☑️'}.get(fmt, '❓')
                        st.write(f"{format_emoji} **{fmt.replace('_', ' ').title()}**: {count} columns")

                with col2:
                    st.markdown("**🗂️ All Tag Columns**")
                    for csv_col, format_type in final_tag_mappings.items():
                        format_emoji = {'comma_separated': '📝', 'single_tag': '🏷️', 'one_hot': '☑️'}.get(format_type, '❓')
                        st.write(f"{format_emoji} {csv_col}")

                # Store final mappings for import process
                st.session_state.final_tag_mappings = final_tag_mappings

            else:
                st.warning("⚠️ No tag columns configured. Tags will not be assigned during import.")
                st.session_state.final_tag_mappings = {}

        else:
            st.info("📤 **Upload a CSV file** to configure tag column detection and assignment.")

            # Show supported formats when no file is uploaded
            st.markdown("### 📋 **Supported Tag Formats**")
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.markdown("**📝 Comma-Separated**")
                st.code('Tags\n"VIP, Enterprise, Marketing"\n"Client, Premium"')

            with col2:
                st.markdown("**🏷️ Single Tag**")
                st.code('Primary Tag,Category\nVIP,Technology\nEnterprise,Marketing')

            with col3:
                st.markdown("**☑️ One-Hot Encoded**")
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
                st.session_state.api_key,
                st.session_state.uploaded_data,
                st.session_state.field_mapping,
                st.session_state.get('environment', 'production'),
                st.session_state.get('custom_url'),
                st.session_state.get('final_tag_mappings', {})
            )
        else:
            status_text.text(f"Creating {row_count} persons...")
            progress_bar.progress(20)
            successful, failed = bulk_import_persons(
                st.session_state.api_key,
                st.session_state.uploaded_data,
                st.session_state.field_mapping,
                st.session_state.get('environment', 'production'),
                st.session_state.get('custom_url'),
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
    st.subheader("🔑 API Configuration")

    user_api_key = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        help="Your Poool API Key"
    )

    if st.button("🔍 Test Connection", type="primary"):
        if not user_api_key:
            st.error("Please enter an API key")
        else:
            current_env = st.session_state.get('environment', 'production')
            custom_url = st.session_state.get('custom_url') if current_env == 'custom' else None

            # Validate custom URL if required
            if current_env == 'custom' and not custom_url:
                st.error("Please enter a custom URL for sandbox environment")
                st.stop()

            with st.spinner(f"Testing API connection to {current_env}..."):
                is_valid, message = test_api_connection(user_api_key, current_env, custom_url)

                if is_valid:
                    st.session_state.api_key = user_api_key
                    st.success(f"✅ API connection successful to **{current_env}**!")
                    st.rerun()
                else:
                    st.error(f"❌ Connection failed to {current_env}: {message}")

    if st.session_state.api_key and st.session_state.api_key == user_api_key:
        st.success("🟢 API Ready")

with col2:
    st.subheader("📁 File Upload & Type")

    if st.session_state.api_key:
        import_type = st.selectbox(
            "Import Type",
            options=['companies', 'persons'],
            index=0 if st.session_state.import_type == 'companies' else 1,
            help="Choose what you want to import"
        )
        st.session_state.import_type = import_type

        uploaded_file = st.file_uploader(
            f"Choose CSV or Excel file for {import_type}",
            type=['csv', 'xlsx', 'xls'],
            help=f"Upload a file containing {import_type} data"
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.session_state.uploaded_data = df
                # Don't clear field_mapping on file upload - user might want to keep mappings
                row_count = len(df)
                col_count = len(df.columns)
                st.success(f"✅ File uploaded: {row_count:,} rows, {col_count} columns")

                # Show appropriate preview based on file size
                preview_expanded = row_count <= 100  # Only expand by default for small files
                with st.expander("📋 Preview Data", expanded=preview_expanded):
                    if row_count > 1000:
                        st.info(f"📊 Large file detected ({row_count:,} rows). Showing first 10 rows for performance.")
                        preview_rows = 10
                    elif row_count > 100:
                        st.info(f"📊 Medium file ({row_count:,} rows). Showing first 20 rows.")
                        preview_rows = 20
                    else:
                        preview_rows = min(row_count, 50)

                    st.dataframe(df.head(preview_rows), use_container_width=True)

            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    else:
        st.info("Please test API connection first")

if st.session_state.uploaded_data is not None:
    st.subheader("🔄 Column Mapping")

    if st.session_state.import_type == 'companies':
        required_fields = get_required_company_fields()
        optional_fields = get_optional_company_fields()
        st.info("📋 **Company Fields**: Map your CSV columns to Poool company fields")
    else:
        required_fields = get_required_person_fields()
        optional_fields = get_optional_person_fields()
        st.info("👤 **Person Fields**: Map your CSV columns to Poool person fields")

    csv_columns = [''] + list(st.session_state.uploaded_data.columns)
    all_fields = required_fields + optional_fields

    # Mapping import/export section
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        # Download mapping as JSON
        if st.session_state.field_mapping or st.session_state.get('final_tag_mappings'):
            json_str = _export_mapping_to_json()
            st.download_button(
                label="📥 Download Mapping",
                data=json_str,
                file_name=f"mapping_config_{st.session_state.import_type}.json",
                mime="application/json",
                help="Download current mapping configuration as JSON"
            )
        else:
            st.button("📥 Download Mapping", disabled=True, help="No mappings to export")

    with col2:
        # Upload mapping from JSON
        uploaded_mapping = st.file_uploader(
            "Upload Mapping",
            type=['json'],
            help="Upload a previously saved mapping configuration",
            key="mapping_upload",
            label_visibility="collapsed"
        )

        # Process uploaded file only once
        if uploaded_mapping is not None and not st.session_state.mapping_file_processed:
            try:
                json_content = uploaded_mapping.read().decode('utf-8')
                success, messages = _import_mapping_from_json(json_content, csv_columns)

                # Display messages
                for message in messages:
                    if message.startswith("Success:"):
                        st.success(message[9:])
                    elif message.startswith("Warning:"):
                        st.warning(message[9:])
                    elif message.startswith("Error:"):
                        st.error(message[7:])

                if success:
                    # Mark as processed and rerun to update UI
                    st.session_state.mapping_file_processed = True
                    st.rerun()

            except Exception as e:
                st.error(f"Failed to read mapping file: {str(e)}")

        # Reset flag when file is removed
        if uploaded_mapping is None and st.session_state.mapping_file_processed:
            st.session_state.mapping_file_processed = False

    with col3:
        if st.button("🗑️ Clear All", help="Remove all field mappings"):
            st.session_state.field_mapping = {}
            st.session_state.final_tag_mappings = {}
            st.session_state.manual_tag_mappings = {}
            st.rerun()

    with col4:
        mapped_count = len([v for v in st.session_state.field_mapping.values() if v and v != ""])
        st.metric("Mapped", f"{mapped_count}/{len(all_fields)}")

        # Debug info (remove later)
        if 'debug_mapping' not in st.session_state:
            st.session_state.debug_mapping = False

        debug_enabled = st.checkbox("🔍 Debug mapping state",
                                   value=st.session_state.debug_mapping,
                                   key="debug_mapping_checkbox")

        if debug_enabled != st.session_state.debug_mapping:
            st.session_state.debug_mapping = debug_enabled

        if st.session_state.debug_mapping:
            st.write("**Current mappings:**", st.session_state.field_mapping)
            st.write("**Mapped count:**", [v for v in st.session_state.field_mapping.values() if v and v != ""])
            st.write("**Total fields:**", len(all_fields))

    # Render the field mapping section using refactored helper functions
    _render_field_mapping_section(required_fields, optional_fields, csv_columns)

    with st.expander("📋 Current Mapping", expanded=False):
        if st.session_state.field_mapping:
            mapping_df = pd.DataFrame([
                {"CSV Column": csv_col, "API Field": api_field}
                for csv_col, api_field in st.session_state.field_mapping.items()
                if api_field
            ])
            st.dataframe(mapping_df, use_container_width=True, hide_index=True)
        else:
            st.info("No mappings configured yet")

    # Check if ALL required fields are mapped
    mapped_required_fields = set(
        api_field for csv_col, api_field in st.session_state.field_mapping.items()
        if api_field in required_fields
    )
    required_mapped = len(mapped_required_fields) == len(required_fields)

    st.subheader("📊 Import Preview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows to Process", len(st.session_state.uploaded_data))
    with col2:
        st.metric("Fields Mapped", len([x for x in st.session_state.field_mapping.values() if x]))
    with col3:
        if required_mapped:
            st.metric("Status", "✅ Ready", delta="Required fields mapped")
        else:
            st.metric("Status", "⚠️ Missing Required", delta="Map required fields")

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
                st.warning(f"⏳ Very large file ({row_count:,} rows). Import may take several minutes. Please be patient and don't refresh the page.")
            elif row_count > 1000:
                st.info(f"📊 Large file ({row_count:,} rows). Import may take 1-2 minutes.")
            elif row_count > 500:
                st.info(f"📊 Medium file ({row_count:,} rows). Should complete in under a minute.")

            if st.button(f"🚀 Create {st.session_state.import_type.title()}", type="primary"):
                _execute_import_with_progress(st.session_state.import_type, row_count)
        else:
            st.error("⚠️ Please fix the validation errors above before importing.")

# Display import results
# noinspection PyUnreachableCode
if st.session_state.import_results:
    results = st.session_state.import_results
    st.subheader("📊 Import Results")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Successful", len(results['successful']))
    with col2:
        st.metric("❌ Failed", len(results['failed']))
    with col3:
        total = len(results['successful']) + len(results['failed'])
        success_rate = (len(results['successful']) / total * 100) if total > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")

    # Show successful imports
    if results['successful']:
        success_count = len(results['successful'])
        expanded = success_count <= 100  # Only expand by default for small results

        with st.expander("✅ Successful Imports", expanded=expanded):
            success_data = []

            # Limit display for large results sets
            if success_count > 1000:
                st.info(f"📊 Large import ({success_count:,} successful). Showing first 100 for performance.")
                items_to_show = results['successful'][:100]
            elif success_count > 500:
                st.info(f"📊 Medium import ({success_count:,} successful). Showing first 200.")
                items_to_show = results['successful'][:200]
            else:
                items_to_show = results['successful']

            for item in items_to_show:
                row_info = {"Row": item['row']}
                if results['import_type'] == 'companies':
                    row_info.update({
                        "Name": item['created'].get('name', 'N/A'),
                        "ID": item['created'].get('id', 'N/A')
                    })
                else:
                    row_info.update({
                        "First Name": item['created'].get('firstname', 'N/A'),
                        "Last Name": item['created'].get('lastname', 'N/A'),
                        "ID": item['created'].get('id', 'N/A')
                    })
                success_data.append(row_info)

            if success_data:
                st.dataframe(pd.DataFrame(success_data), use_container_width=True, hide_index=True)

                if len(items_to_show) < success_count:
                    st.caption(f"Showing {len(items_to_show)} of {success_count:,} successful imports")


    # Show failed imports with enhanced context
    if results['failed']:
        failed_count = len(results['failed'])
        expanded = failed_count <= 50  # Only expand by default for small failure sets

        with st.expander("❌ Failed Imports", expanded=expanded):
            st.warning(f"💡 **Tip**: Review the data in these rows and fix the issues before re-importing.")

            # Limit display for large failure sets
            if failed_count > 100:
                st.info(f"📊 Large failure set ({failed_count:,} failed). Showing first 50 for performance.")
                items_to_show = results['failed'][:50]
            else:
                items_to_show = results['failed']

            failure_data = []
            for item in items_to_show:
                error_msg = item['error']
                suggestions = []

                # Add contextual suggestions based on error type
                if 'Missing required field' in error_msg:
                    suggestions.append("Check column mapping for required fields")
                elif 'email' in error_msg.lower():
                    suggestions.append("Verify email format (e.g., user@domain.com)")
                elif 'phone' in error_msg.lower():
                    suggestions.append("Include country code (e.g., +49 30 12345678)")
                elif 'duplicate' in error_msg.lower():
                    suggestions.append("This record may already exist in the CRM")
                elif '400' in error_msg or 'Bad Request' in error_msg:
                    suggestions.append("Check data format and required fields")
                elif '401' in error_msg or 'Unauthorized' in error_msg:
                    suggestions.append("Verify API key is correct")
                elif '403' in error_msg or 'Forbidden' in error_msg:
                    suggestions.append("Check API permissions")

                # Show sample data from the failed row
                sample_data = []
                if 'data' in item and item['data']:
                    # Show first few fields as context
                    for k, v in list(item['data'].items())[:3]:
                        sample_data.append(f"{k}: {v}")

                failure_data.append({
                    "Row": item['row'],
                    "Error": error_msg,
                    "Sample Data": " | ".join(sample_data) if sample_data else "N/A",
                    "Suggestion": " | ".join(suggestions) if suggestions else "Review data format"
                })

            if failure_data:
                st.dataframe(pd.DataFrame(failure_data), use_container_width=True, hide_index=True)

                if len(items_to_show) < failed_count:
                    st.caption(f"Showing {len(items_to_show)} of {failed_count:,} failed imports")

                # Common error patterns summary
                error_types = {}
                for item in results['failed']:
                    error = item['error']
                    if 'Missing required field' in error:
                        error_types['Missing Required Fields'] = error_types.get('Missing Required Fields', 0) + 1
                    elif any(code in error for code in ['400', '401', '403', '500']):
                        error_types['API Errors'] = error_types.get('API Errors', 0) + 1
                    else:
                        error_types['Data Format Issues'] = error_types.get('Data Format Issues', 0) + 1

                if error_types:
                    st.subheader("📊 Error Summary")
                    cols = st.columns(len(error_types))
                    for i, (error_type, count) in enumerate(error_types.items()):
                        cols[i].metric(error_type, count)

    if st.button("🔄 Clear Results"):
        st.session_state.import_results = None
        st.rerun()

st.markdown("---")
st.markdown("💡 **Tip:** Check the mapping carefully before importing to avoid errors")
