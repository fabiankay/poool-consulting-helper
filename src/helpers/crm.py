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


# Update-related functions
def get_client_fields() -> List[str]:
    """Return list of fields that belong to the client endpoint."""
    return [
        'customer_number', 'payment_time_day_num', 'dunning_blocked', 'dunning_document_blocked',
        'reference_number_required', 'datev_account', 'leitweg_id', 'datev_is_client_collection',
        'send_bill_to_email_to', 'send_bill_to_email_cc', 'send_bill_to_email_bcc',
        'send_by_email', 'send_by_mail', 'number', 'number_unique'
    ]


def get_supplier_fields() -> List[str]:
    """Return list of fields that belong to the supplier endpoint."""
    return [
        'customer_number', 'discount_day_num', 'discount_percentage',
        'comment_supplier', 'comment_internal', 'datev_account',
        'number'
    ]


def separate_update_fields_by_endpoint(row_data: Dict, field_mapping: Dict) -> Tuple[Dict, Dict, Dict]:
    """
    Separate update data into company, client, and supplier fields.
    Returns: (company_fields, client_fields, supplier_fields)
    """
    client_field_names = set(get_client_fields())
    supplier_field_names = set(get_supplier_fields())

    company_data = {}
    client_data = {}
    supplier_data = {}

    for csv_column, api_field in field_mapping.items():
        if not api_field or csv_column not in row_data:
            continue

        value = row_data[csv_column]
        if value is None or (isinstance(value, str) and not value.strip()):
            continue

        # Route to appropriate endpoint
        if api_field in client_field_names:
            client_data[api_field] = value
        elif api_field in supplier_field_names:
            supplier_data[api_field] = value
        else:
            # Company endpoint (includes addresses, contacts, tags, etc.)
            company_data[api_field] = value

    return company_data, client_data, supplier_data


def match_company_by_identifier(client: PooolAPIClient, identifier_field: str, identifier_value: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Find a company by identifier field and value.
    Returns: (company_id, error_message)
    """
    try:
        if not identifier_value or not str(identifier_value).strip():
            return None, "Empty identifier value"

        identifier_value = str(identifier_value).strip()

        # Direct ID lookup
        if identifier_field.lower() == 'id':
            try:
                company_id = int(identifier_value)
                # Verify company exists
                company_data, error = client.get_company_by_id(company_id)
                if error:
                    return None, f"Company ID {company_id} not found"
                return company_id, None
            except ValueError:
                return None, f"Invalid ID value: {identifier_value}"

        # Search by other fields
        results, error = client.search_companies_by_field(identifier_field, identifier_value)

        if error:
            return None, error

        if not results:
            return None, f"No company found with {identifier_field}='{identifier_value}'"

        # Look for exact match
        for company in results:
            company_value = company.get(identifier_field)
            if company_value and str(company_value).lower() == identifier_value.lower():
                return company.get('id'), None

        # If no exact match, return first result with warning
        return results[0].get('id'), f"No exact match, using closest: {results[0].get('name', 'Unknown')}"

    except Exception as e:
        return None, f"Error matching company: {str(e)}"


def match_person_by_identifier(client: PooolAPIClient, identifier_field: str, identifier_value: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Find a person by identifier field and value.
    Returns: (person_id, error_message)
    """
    try:
        if not identifier_value or not str(identifier_value).strip():
            return None, "Empty identifier value"

        identifier_value = str(identifier_value).strip()

        # Direct ID lookup
        if identifier_field.lower() == 'id':
            try:
                person_id = int(identifier_value)
                # Verify person exists
                person_data, error = client.get_person_by_id(person_id)
                if error:
                    return None, f"Person ID {person_id} not found"
                return person_id, None
            except ValueError:
                return None, f"Invalid ID value: {identifier_value}"

        # Search by other fields (name, email, etc.)
        results, error = client.search_persons_by_field(identifier_field, identifier_value)

        if error:
            return None, error

        if not results:
            return None, f"No person found with {identifier_field}='{identifier_value}'"

        # Look for exact match
        for person in results:
            person_value = person.get(identifier_field)
            if person_value and str(person_value).lower() == identifier_value.lower():
                return person.get('id'), None

        # If no exact match, return first result with warning
        first_person = results[0]
        name = f"{first_person.get('firstname', '')} {first_person.get('lastname', '')}".strip() or 'Unknown'
        return first_person.get('id'), f"No exact match, using closest: {name}"

    except Exception as e:
        return None, f"Error matching person: {str(e)}"


def process_single_update(client: PooolAPIClient, index: int, row_data: Dict, field_mapping: Dict,
                         identifier_field: str, update_type: str, dry_run: bool = False) -> Dict:
    """
    Process a single row update for companies or persons.
    Returns: Dict with success status and details
    """
    try:
        # Clean NaN values
        clean_data = {k: v for k, v in row_data.items() if pd.notna(v)}

        if update_type == 'companies':
            # Get identifier value
            identifier_col = next((col for col, field in field_mapping.items() if field == identifier_field), None)
            if not identifier_col or identifier_col not in clean_data:
                return {
                    'success': False,
                    'error': f'Identifier field "{identifier_field}" not found in row data'
                }

            identifier_value = clean_data[identifier_col]

            # Match existing company
            company_id, match_error = match_company_by_identifier(client, identifier_field, identifier_value)

            if not company_id:
                return {
                    'success': False,
                    'error': match_error or 'Could not match company'
                }

            # Separate fields by endpoint
            company_fields, client_fields, supplier_fields = separate_update_fields_by_endpoint(clean_data, field_mapping)

            # Prepare company data if any company fields exist
            if company_fields:
                prepared_company_data = prepare_company_data(clean_data,
                    {k: v for k, v in field_mapping.items() if v in company_fields})
            else:
                prepared_company_data = {}

            # Track results
            results = {'company_id': company_id, 'updates': [], 'dry_run': dry_run}
            errors = []

            if dry_run:
                # Dry run mode - simulate updates without API calls
                if prepared_company_data:
                    results['updates'].append('company')
                    results['company_fields'] = list(prepared_company_data.keys())
                if client_fields:
                    results['updates'].append('client')
                    results['client_fields'] = list(client_fields.keys())
                if supplier_fields:
                    results['updates'].append('supplier')
                    results['supplier_fields'] = list(supplier_fields.keys())
            else:
                # Actual update mode
                # Update company endpoint if needed
                if prepared_company_data:
                    updated_data, error = client.update_company(company_id, prepared_company_data)
                    if error:
                        errors.append(f"Company update failed: {error}")
                    else:
                        results['updates'].append('company')

                # Update client endpoint if needed
                if client_fields:
                    updated_data, error = client.update_client(company_id, client_fields)
                    if error:
                        errors.append(f"Client update failed: {error}")
                    else:
                        results['updates'].append('client')

                # Update supplier endpoint if needed
                if supplier_fields:
                    updated_data, error = client.update_supplier(company_id, supplier_fields)
                    if error:
                        errors.append(f"Supplier update failed: {error}")
                    else:
                        results['updates'].append('supplier')

            if errors:
                return {
                    'success': False,
                    'error': '; '.join(errors),
                    'partial_success': len(results['updates']) > 0,
                    'results': results
                }

            return {
                'success': True,
                'result': {
                    'row': index,
                    'company_id': company_id,
                    'endpoints_updated': results['updates'],
                    'identifier': identifier_value
                }
            }

        else:  # persons
            # Get identifier value
            identifier_col = next((col for col, field in field_mapping.items() if field == identifier_field), None)
            if not identifier_col or identifier_col not in clean_data:
                return {
                    'success': False,
                    'error': f'Identifier field "{identifier_field}" not found in row data'
                }

            identifier_value = clean_data[identifier_col]

            # Match existing person
            person_id, match_error = match_person_by_identifier(client, identifier_field, identifier_value)

            if not person_id:
                return {
                    'success': False,
                    'error': match_error or 'Could not match person'
                }

            # Prepare person data
            person_data = prepare_person_data(clean_data, field_mapping)

            if not person_data:
                return {
                    'success': False,
                    'error': 'No valid person data to update'
                }

            if dry_run:
                # Dry run mode - simulate update without API call
                return {
                    'success': True,
                    'result': {
                        'row': index,
                        'person_id': person_id,
                        'identifier': identifier_value,
                        'fields_to_update': list(person_data.keys()),
                        'dry_run': True
                    }
                }
            else:
                # Actual update mode
                updated_data, error = client.update_person(person_id, person_data)

                if error:
                    return {
                        'success': False,
                        'error': f'Person update failed: {error}'
                    }

                return {
                    'success': True,
                    'result': {
                        'row': index,
                        'person_id': person_id,
                        'identifier': identifier_value,
                        'fields_updated': list(person_data.keys())
                    }
                }

    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def bulk_update_companies(api_key: str, df, field_mapping: Dict, identifier_field: str,
                         environment: str = "production", custom_url: str = None,
                         dry_run: bool = False) -> Tuple[List[Dict], List[Dict]]:
    """Bulk update companies from DataFrame."""
    client = create_api_client(api_key, environment, custom_url)

    successful = []
    failed = []

    # Pre-convert DataFrame to dict for better performance
    records = df.to_dict('records')

    for index, row_data in enumerate(records, 1):
        result = process_single_update(client, index, row_data, field_mapping, identifier_field, 'companies', dry_run)

        if result['success']:
            successful.append(result['result'])
        else:
            failed.append({
                'row': index,
                'data': {k: v for k, v in row_data.items() if pd.notna(v)},
                'error': result['error'],
                'partial_success': result.get('partial_success', False)
            })

    return successful, failed


def preview_company_matches(api_key: str, df, field_mapping: Dict, identifier_field: str,
                            environment: str = "production", custom_url: str = None,
                            preview_limit: int = 20) -> List[Dict]:
    """
    Preview how records will be matched without updating.

    Args:
        api_key: API key
        df: DataFrame with records
        field_mapping: CSV column to API field mapping
        identifier_field: Field to use for matching
        environment: API environment
        custom_url: Custom URL if environment is custom
        preview_limit: Number of records to preview (default 20)

    Returns:
        List of match preview results
    """
    client = create_api_client(api_key, environment, custom_url)

    preview_results = []

    # Get identifier column from mapping
    identifier_col = next((col for col, field in field_mapping.items() if field == identifier_field), None)
    if not identifier_col:
        return [{
            'error': f'Identifier field "{identifier_field}" not found in field mapping'
        }]

    # Preview first N records
    records = df.head(preview_limit).to_dict('records')

    for index, row_data in enumerate(records, 1):
        # Clean data
        clean_data = {k: v for k, v in row_data.items() if pd.notna(v)}

        if identifier_col not in clean_data:
            preview_results.append({
                'row': index,
                'identifier_value': 'N/A',
                'status': '❌ Missing',
                'company_id': None,
                'company_name': None,
                'message': f'Identifier column "{identifier_col}" not found in row'
            })
            continue

        identifier_value = clean_data[identifier_col]

        # Try to match
        company_id, error = match_company_by_identifier(client, identifier_field, identifier_value)

        if company_id:
            # Get company name
            company_data, get_error = client.get_company_by_id(company_id)
            company_name = company_data.get('name', 'Unknown') if company_data else 'Unknown'

            # Check if it was a fuzzy match
            if error:
                status = '⚠️ Fuzzy Match'
                message = error
            else:
                status = '✅ Found'
                message = 'Exact match'

            preview_results.append({
                'row': index,
                'identifier_value': str(identifier_value),
                'status': status,
                'company_id': company_id,
                'company_name': company_name,
                'message': message
            })
        else:
            preview_results.append({
                'row': index,
                'identifier_value': str(identifier_value),
                'status': '❌ Not Found',
                'company_id': None,
                'company_name': None,
                'message': error or 'No match found'
            })

    return preview_results


def bulk_update_persons(api_key: str, df, field_mapping: Dict, identifier_field: str,
                       environment: str = "production", custom_url: str = None,
                       dry_run: bool = False) -> Tuple[List[Dict], List[Dict]]:
    """Bulk update persons from DataFrame."""
    client = create_api_client(api_key, environment, custom_url)

    successful = []
    failed = []

    # Pre-convert DataFrame to dict for better performance
    records = df.to_dict('records')

    for index, row_data in enumerate(records, 1):
        result = process_single_update(client, index, row_data, field_mapping, identifier_field, 'persons', dry_run)

        if result['success']:
            successful.append(result['result'])
        else:
            failed.append({
                'row': index,
                'data': {k: v for k, v in row_data.items() if pd.notna(v)},
                'error': result['error']
            })

    return successful, failed


def preview_person_matches(api_key: str, df, field_mapping: Dict, identifier_field: str,
                          environment: str = "production", custom_url: str = None,
                          preview_limit: int = 20) -> List[Dict]:
    """
    Preview how person records will be matched without updating.

    Args:
        api_key: API key
        df: DataFrame with records
        field_mapping: CSV column to API field mapping
        identifier_field: Field to use for matching (e.g., 'id', 'email', 'firstname')
        environment: API environment
        custom_url: Custom URL if environment is custom
        preview_limit: Number of records to preview (default 20)

    Returns:
        List of match preview results
    """
    client = create_api_client(api_key, environment, custom_url)

    preview_results = []

    # Get identifier column from mapping
    identifier_col = next((col for col, field in field_mapping.items() if field == identifier_field), None)
    if not identifier_col:
        return [{
            'error': f'Identifier field "{identifier_field}" not found in field mapping'
        }]

    # Preview first N records
    records = df.head(preview_limit).to_dict('records')

    for index, row_data in enumerate(records, 1):
        # Clean data
        clean_data = {k: v for k, v in row_data.items() if pd.notna(v)}

        if identifier_col not in clean_data:
            preview_results.append({
                'row': index,
                'identifier_value': 'N/A',
                'status': '❌ Missing',
                'person_id': None,
                'person_name': None,
                'message': f'Identifier column "{identifier_col}" not found in row'
            })
            continue

        identifier_value = clean_data[identifier_col]

        # Try to match
        person_id, error = match_person_by_identifier(client, identifier_field, identifier_value)

        if person_id:
            # Get person name
            person_data, get_error = client.get_person_by_id(person_id)
            if person_data:
                person_name = f"{person_data.get('firstname', '')} {person_data.get('lastname', '')}".strip() or 'Unknown'
            else:
                person_name = 'Unknown'

            # Check if it was a fuzzy match
            if error:
                status = '⚠️ Fuzzy Match'
                message = error
            else:
                status = '✅ Found'
                message = 'Exact match'

            preview_results.append({
                'row': index,
                'identifier_value': str(identifier_value),
                'status': status,
                'person_id': person_id,
                'person_name': person_name,
                'message': message
            })
        else:
            preview_results.append({
                'row': index,
                'identifier_value': str(identifier_value),
                'status': '❌ Not Found',
                'person_id': None,
                'person_name': None,
                'message': error or 'No match found'
            })

    return preview_results
