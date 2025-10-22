"""
CRM helper functions using the PooolAPIClient class.

Provides functions for importing companies and persons, handling field mappings,
validation, and tag management for the Poool CRM system.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from .poool_api_client import PooolAPIClient


def create_api_client(api_key: str, environment: str = "production", custom_url: str = None) -> PooolAPIClient:
    """Create and return a configured API client."""
    return PooolAPIClient(api_key, environment, custom_url)


def test_api_connection(api_key: str, environment: str = "production", custom_url: str = None) -> Tuple[bool, str]:
    """Test API connection using the API client."""
    client = create_api_client(api_key, environment, custom_url)
    return client.test_connection()


def get_required_company_fields() -> List[str]:
    """Return list of fields that are typically required for company creation."""
    return ["name"]


def get_optional_company_fields() -> List[str]:
    """Return list of optional fields for company creation."""
    return [
        # Core company info
        "name_legal", "name_token", "uid", "commercial_register", "jurisdiction",
        "management", "data_privacy_number",

        # Person fields (for company contacts)
        "salutation", "title", "firstname", "middlename", "lastname", "nickname",
        "position", "function", "department", "maiden_name", "birthday", "gender",

        # Additional info
        "note", "is_operator",

        # Relationship flags
        "is_client", "is_supplier",

        # Client-specific fields
        "customer_number", "payment_time_day_num", "comment_client",
        "send_bill_to_email_to", "reference_number_required", "dunning_blocked",

        # Supplier-specific fields
        "comment_supplier", "discount_day_num", "discount_percentage",

        # German/EU specific fields
        "datev_account", "leitweg_id", "datev_is_client_collection",

        # Tags
        "tags",

        # Generic additional info
        "additional_information_a", "additional_information_b", "additional_information_c",

        # Complex fields (create nested objects)
        "address_street", "address_house_number", "address_zip", "address_city",
        "contact_phone", "contact_email", "contact_website"
    ]


def get_required_person_fields() -> List[str]:
    """Return list of fields that are typically required for person creation."""
    return ["firstname", "lastname"]


def get_optional_person_fields() -> List[str]:
    """Return list of optional fields for person creation."""
    return [
        "company", "company_id", "company_subsidiary_id", "email", "phone",
        "salutation", "title", "middlename", "middle_name", "nickname",
        "position", "function", "department", "maiden_name",
        "additional_information_a", "additional_information_b", "additional_information_c",
        "tags", "contacts"
    ]


def prepare_company_data(row_data: Dict, field_mapping: Dict) -> Dict:
    """Prepare company data for API submission using field mapping."""
    company_data = {}
    complex_fields = {}

    # Process all fields in a single loop
    for csv_column, api_field in field_mapping.items():
        if not api_field or csv_column not in row_data:
            continue

        value = row_data[csv_column]
        if value is None:
            continue

        str_value = str(value).strip()

        # Handle different field types
        if api_field in ["is_client", "is_supplier"]:
            company_data[api_field] = bool(str_value)
        elif api_field in ["reference_number_required", "dunning_blocked", "datev_is_client_collection"]:
            if str_value.lower() in ['true', '1', 'yes']:
                company_data[api_field] = "1"
            elif str_value.lower() in ['false', '0', 'no']:
                company_data[api_field] = "0"
            elif str_value:
                company_data[api_field] = "1"
        elif api_field in ["payment_time_day_num", "discount_day_num"]:
            if str_value.isdigit():
                company_data[api_field] = int(str_value)
        elif api_field == "discount_percentage":
            try:
                company_data[api_field] = float(str_value.replace(',', '.'))
            except ValueError:
                pass
        elif api_field.startswith(("address_", "contact_")):
            if str_value:
                complex_fields[api_field] = str_value
        elif str_value:
            company_data[api_field] = str_value

    # Process complex fields if any exist
    if complex_fields:
        _add_complex_fields_to_company(company_data, complex_fields)

    return company_data


def _add_complex_fields_to_company(company_data: Dict, complex_fields: Dict) -> None:
    """Add addresses and contacts arrays to company data."""
    addresses = []
    contacts = []

    # Extract address data
    address_data = {
        "street_name": complex_fields.get("address_street"),
        "street_number": complex_fields.get("address_house_number"),
        "zip": complex_fields.get("address_zip"),
        "location": complex_fields.get("address_city")
    }

    # Create address if any address fields exist
    if any(address_data.values()):
        address = {"is_preferred": True, "pos": 1, "country_id": 1}
        address.update({k: v for k, v in address_data.items() if v})
        addresses.append(address)

    # Create contacts
    contact_configs = [
        ("contact_phone", 1, "Phone", True),
        ("contact_email", 2, "Email", True),
        ("contact_website", 6, "Website", False)
    ]

    contact_pos = 1
    for field_key, contact_type_id, title, is_preferred in contact_configs:
        if field_key in complex_fields:
            contacts.append({
                "contact_type_id": contact_type_id,
                "value": complex_fields[field_key],
                "title": title,
                "is_preferred": is_preferred,
                "pos": contact_pos
            })
            contact_pos += 1

    # Add arrays to company data if they have content
    if addresses:
        company_data["addresses"] = addresses
    if contacts:
        company_data["contacts"] = contacts


def prepare_person_data(row_data: Dict, field_mapping: Dict) -> Dict:
    """Prepare person data for API submission using field mapping."""
    person_data = {}
    contacts_data = {}

    # Process each mapped field
    for csv_column, api_field in field_mapping.items():
        if api_field and csv_column in row_data:
            value = row_data[csv_column]

            if value is not None and str(value).strip():
                clean_value = str(value).strip()

                # Handle contact information (email, phone)
                if api_field in ['email', 'phone']:
                    if api_field == 'email':
                        contacts_data['email'] = {
                            "contact_type_id": 1,
                            "value": clean_value
                        }
                    elif api_field == 'phone':
                        contacts_data['phone'] = {
                            "contact_type_id": 2,
                            "value": clean_value
                        }
                else:
                    person_data[api_field] = clean_value

    # Add contacts array if we have contact information
    if contacts_data:
        person_data["contacts"] = list(contacts_data.values())

    return person_data


def prepare_person_data_with_company_lookup(client: PooolAPIClient, row_data: Dict, field_mapping: Dict) -> Tuple[Dict, List[str]]:
    """Prepare person data with company lookup functionality."""
    warnings = []

    # Start with basic person data preparation
    person_data = prepare_person_data(row_data, field_mapping)

    # Handle company identification if company name is provided
    if 'company' in person_data:
        company_name = person_data['company']

        # Look up company_id
        company_id, error = client.lookup_company_by_name(company_name)

        if company_id:
            person_data['company_id'] = company_id
            del person_data['company']

            if error:  # Partial match warning
                warnings.append(f"Warning: {error}")
        else:
            if error:
                warnings.append(f"Warning: Company lookup failed for '{company_name}': {error}")
            else:
                warnings.append(f"Warning: Empty company name provided")
            del person_data['company']

    return person_data, warnings


def validate_import_data(df, field_mapping: Dict, import_type: str) -> Tuple[bool, List[str]]:
    """Validate DataFrame and field mapping before import."""
    all_messages = []

    # Basic validation
    if df.empty:
        all_messages.append("Upload file is empty")

    # Required field validation
    if import_type == 'companies':
        required_fields = ['name']
    else:
        required_fields = ['firstname', 'lastname']

    mapped_required = [field for field in field_mapping.values() if field in required_fields]
    missing_required = [field for field in required_fields if field not in mapped_required]

    if missing_required:
        if import_type == 'companies':
            all_messages.append("Required field 'name' must be mapped for companies")
        else:
            all_messages.append(f"Required fields must be mapped: {', '.join(missing_required)}")

    # Column existence validation
    missing_columns = [col for col in field_mapping.keys() if col not in df.columns]
    if missing_columns:
        all_messages.append(f"Mapped columns not found in file: {', '.join(missing_columns)}")

    # Data quality validation
    if import_type == 'companies':
        name_column = next((col for col, field in field_mapping.items() if field == 'name'), None)
        if name_column:
            empty_count = df[name_column].isna().sum() + (df[name_column] == '').sum()
            if empty_count > 0:
                all_messages.append(f"Warning: {empty_count} rows have empty company names and will be skipped")
    else:
        for required_field in ['firstname', 'lastname']:
            col = next((col for col, field in field_mapping.items() if field == required_field), None)
            if col:
                empty_count = df[col].isna().sum() + (df[col] == '').sum()
                if empty_count > 0:
                    all_messages.append(f"Warning: {empty_count} rows have empty {required_field}s and will be skipped")

    # Determine if validation passed
    has_errors = any(not msg.startswith("Warning:") for msg in all_messages)
    return not has_errors, all_messages


def process_single_import(client: PooolAPIClient, index: int, row_data: Dict, field_mapping: Dict, import_type: str) -> Dict:
    """Process a single row import for companies or persons."""
    try:
        # Clean NaN values efficiently
        clean_data = {k: v for k, v in row_data.items() if pd.notna(v)}

        # Prepare data based on import type
        if import_type == 'companies':
            prepared_data = prepare_company_data(clean_data, field_mapping)

            # Early validation
            if not prepared_data.get('name'):
                return {
                    'success': False,
                    'error': 'Missing required field: name'
                }

            created_item, error = client.create_company(prepared_data)
        else:
            # Use enhanced person preparation with company lookup
            prepared_data, lookup_warnings = prepare_person_data_with_company_lookup(client, clean_data, field_mapping)

            # Early validation
            if not prepared_data.get('firstname') or not prepared_data.get('lastname'):
                return {
                    'success': False,
                    'error': 'Missing required fields: firstname and/or lastname'
                }

            created_item, error = client.create_person(prepared_data)

        if error:
            return {
                'success': False,
                'error': error
            }
        else:
            return {
                'success': True,
                'result': {
                    'row': index,
                    'data': clean_data,
                    'created': created_item
                }
            }

    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def bulk_import_generic(client: PooolAPIClient, df, field_mapping: Dict, import_type: str, tag_mappings: Dict = None) -> Tuple[List[Dict], List[Dict]]:
    """Generic bulk import function for companies or persons."""
    successful = []
    failed = []

    # Pre-convert DataFrame to dict for better performance
    records = df.to_dict('records')

    for index, row_data in enumerate(records, 1):
        result = process_single_import(client, index, row_data, field_mapping, import_type)

        if result['success']:
            successful.append(result['result'])
        else:
            failed.append({
                'row': index,
                'data': {k: v for k, v in row_data.items() if pd.notna(v)},
                'error': result['error']
            })

    return successful, failed


def bulk_import_companies(api_key: str, df, field_mapping: Dict, environment: str = "production", custom_url: str = None, tag_mappings: Dict = None) -> Tuple[List[Dict], List[Dict]]:
    """Import multiple companies from DataFrame."""
    client = create_api_client(api_key, environment, custom_url)
    return bulk_import_generic(client, df, field_mapping, 'companies', tag_mappings)


def bulk_import_persons(api_key: str, df, field_mapping: Dict, environment: str = "production", custom_url: str = None, tag_mappings: Dict = None) -> Tuple[List[Dict], List[Dict]]:
    """Import multiple persons from DataFrame."""
    client = create_api_client(api_key, environment, custom_url)
    return bulk_import_generic(client, df, field_mapping, 'persons', tag_mappings)


# Tag-related functions using the API client
def parse_comma_separated_tags(tag_string: str) -> List[str]:
    """Parse comma-separated tag string into list of tag names."""
    if not tag_string or pd.isna(tag_string):
        return []

    tags = [tag.strip().strip('"').strip("'") for tag in str(tag_string).split(',')]
    return [tag for tag in tags if tag]


def get_tag_ids_for_names(client: PooolAPIClient, tag_names: List[str], tag_cache: Dict[str, int], auto_create: bool = True) -> Tuple[List[int], List[str], Optional[str]]:
    """Convert list of tag names to tag IDs, optionally creating missing tags."""
    tag_ids = []
    created_tags = []

    for tag_name in tag_names:
        tag_name_clean = tag_name.strip()
        if not tag_name_clean:
            continue

        # Check cache first (case-insensitive)
        tag_id = None
        for cached_name, cached_id in tag_cache.items():
            if cached_name.lower() == tag_name_clean.lower():
                tag_id = cached_id
                break

        if tag_id:
            tag_ids.append(tag_id)
        elif auto_create:
            # Create missing tag
            new_tag_id, error = client.create_tag_if_missing(tag_name_clean)
            if error:
                return [], [], f"Failed to create tag '{tag_name_clean}': {error}"

            if new_tag_id:
                tag_ids.append(new_tag_id)
                tag_cache[tag_name_clean] = new_tag_id
                tag_cache[tag_name_clean.lower()] = new_tag_id
                created_tags.append(tag_name_clean)
        else:
            continue

    return tag_ids, created_tags, None


def detect_tag_columns(df: pd.DataFrame) -> Dict[str, str]:
    """Auto-detect tag columns in DataFrame and determine their format."""
    import re

    tag_mappings = {}

    # Strategy 1: One-hot encoding (check first for specific patterns)
    one_hot_cols = [col for col in df.columns
                   if col.lower().startswith(('tag_', 'label_', 'category_')) and '_' in col.lower()]
    for col in one_hot_cols:
        sample = df[col].dropna()
        if len(sample) > 0:
            unique_vals = set(sample.astype(str).str.lower())
            boolean_vals = {'0', '1', 'true', 'false', 'yes', 'no', '0.0', '1.0'}
            if unique_vals.issubset(boolean_vals):
                tag_mappings[col] = 'one_hot'

    # Strategy 2: Comma-separated detection
    for col in df.columns:
        if col not in tag_mappings and any(keyword in col.lower() for keyword in ['tag', 'label', 'category']):
            sample = df[col].dropna().head(10)
            if len(sample) > 0 and any(',' in str(val) for val in sample):
                tag_mappings[col] = 'comma_separated'
                continue
            elif len(sample) > 0:
                tag_mappings[col] = 'single_tag'
                continue

    # Strategy 3: Multiple tag columns
    tag_pattern_cols = [col for col in df.columns
                       if re.match(r'tag\w*\d*|secondary.*tag|primary.*tag|main.*tag', col.lower())]
    for col in tag_pattern_cols:
        if col not in tag_mappings:
            tag_mappings[col] = 'single_tag'

    return tag_mappings


def process_entity_tags(client: PooolAPIClient, row_data: pd.Series, tag_mappings: Dict[str, str], tag_cache: Dict[str, int], auto_create: bool = True) -> Tuple[List[int], List[str], Optional[str]]:
    """Process all tag assignments for a single entity."""
    all_tag_names = set()

    # Process each mapped column
    for column, format_type in tag_mappings.items():
        if column not in row_data or pd.isna(row_data[column]):
            continue

        if format_type == 'comma_separated':
            tags = parse_comma_separated_tags(row_data[column])
            all_tag_names.update(tags)
        elif format_type == 'single_tag':
            tag = str(row_data[column]).strip()
            if tag and tag.lower() not in ['nan', 'none', '']:
                all_tag_names.add(tag)
        elif format_type == 'one_hot':
            value = str(row_data[column]).lower()
            if value in ['1', 'true', 'yes', '1.0']:
                tag_name = column.lower()
                for prefix in ['tag_', 'label_', 'category_']:
                    if tag_name.startswith(prefix):
                        tag_name = tag_name[len(prefix):]
                        break
                tag_name = tag_name.replace('_', ' ').title()
                all_tag_names.add(tag_name)

    # Convert tag names to IDs
    if all_tag_names:
        return get_tag_ids_for_names(client, list(all_tag_names), tag_cache, auto_create)
    else:
        return [], [], None
