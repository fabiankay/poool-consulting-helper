"""
Update operations for CRM system.

Handles bulk updates, matching, preview functions for companies and persons.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from ..poool_api_client import PooolAPIClient
from .field_definitions import get_client_fields, get_supplier_fields


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

    for api_field, csv_column in field_mapping.items():
        if not csv_column or csv_column not in row_data:
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


def prepare_supplier_update_data(supplier_data: Dict) -> Dict:
    """
    Prepare supplier data with proper type conversions for API submission.

    Args:
        supplier_data: Dict of supplier field names to values

    Returns:
        Dict with properly typed values ready for API
    """
    prepared = {}

    for field, value in supplier_data.items():
        if value is None or (isinstance(value, str) and not value.strip()):
            continue

        str_value = str(value).strip()

        # Handle integer fields
        if field in ["payment_time_day_num", "discount_day_num"]:
            if str_value.isdigit():
                prepared[field] = int(str_value)
        # Handle float fields
        elif field == "discount_percentage":
            try:
                prepared[field] = float(str_value.replace(',', '.'))
            except ValueError:
                pass
        # String fields
        elif str_value:
            prepared[field] = str_value

    return prepared


def match_company_by_identifier(client: PooolAPIClient, identifier_field: str, identifier_value: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Find a company by identifier field and value.
    Returns: (company_id, error_message)
    """
    try:
        if not identifier_value or not str(identifier_value).strip():
            return None, "Leerer Identifikator-Wert"

        identifier_value = str(identifier_value).strip()

        # Direct ID lookup
        if identifier_field.lower() == 'id':
            try:
                company_id = int(identifier_value)
                # Verify company exists
                company_data, error = client.get_company_by_id(company_id)
                if error:
                    return None, f"Firmen-ID {company_id} nicht gefunden"
                return company_id, None
            except ValueError:
                return None, f"Ungültiger ID-Wert: {identifier_value}"

        # Search by other fields
        results, error = client.search_companies_by_field(identifier_field, identifier_value)

        if error:
            return None, error

        if not results:
            return None, f"Keine Firma gefunden mit {identifier_field}='{identifier_value}'"

        # Look for exact match
        for company in results:
            company_value = company.get(identifier_field)
            if company_value and str(company_value).lower() == identifier_value.lower():
                return company.get('id'), None

        # If no exact match, return first result with warning
        return results[0].get('id'), f"Keine exakte Übereinstimmung, verwende nächste: {results[0].get('name', 'Unbekannt')}"

    except Exception as e:
        return None, f"Fehler beim Abgleichen der Firma: {str(e)}"


def match_person_by_identifier(client: PooolAPIClient, identifier_field: str, identifier_value: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Find a person by identifier field and value.
    Returns: (person_id, error_message)
    """
    try:
        if not identifier_value or not str(identifier_value).strip():
            return None, "Leerer Identifikator-Wert"

        identifier_value = str(identifier_value).strip()

        # Direct ID lookup
        if identifier_field.lower() == 'id':
            try:
                person_id = int(identifier_value)
                # Verify person exists
                person_data, error = client.get_person_by_id(person_id)
                if error:
                    return None, f"Personen-ID {person_id} nicht gefunden"
                return person_id, None
            except ValueError:
                return None, f"Ungültiger ID-Wert: {identifier_value}"

        # Search by other fields (name, email, etc.)
        results, error = client.search_persons_by_field(identifier_field, identifier_value)

        if error:
            return None, error

        if not results:
            return None, f"Keine Person gefunden mit {identifier_field}='{identifier_value}'"

        # Look for exact match
        for person in results:
            person_value = person.get(identifier_field)
            if person_value and str(person_value).lower() == identifier_value.lower():
                return person.get('id'), None

        # If no exact match, return first result with warning
        first_person = results[0]
        name = f"{first_person.get('firstname', '')} {first_person.get('lastname', '')}".strip() or 'Unbekannt'
        return first_person.get('id'), f"Keine exakte Übereinstimmung, verwende nächste: {name}"

    except Exception as e:
        return None, f"Fehler beim Abgleichen der Person: {str(e)}"


def process_single_update(client: PooolAPIClient, index: int, row_data: Dict, field_mapping: Dict,
                         identifier_field: str, update_type: str, dry_run: bool = False, country_cache: Optional[Dict[str, int]] = None) -> Dict:
    """
    Process a single row update for companies or persons.
    Returns: Dict with success status and details
    """
    from .company_operations import prepare_company_data
    from .person_operations import prepare_person_data

    try:
        # Clean NaN values
        clean_data = {k: v for k, v in row_data.items() if pd.notna(v)}

        if update_type == 'companies':
            # Get identifier value
            identifier_col = field_mapping.get(identifier_field)
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
                # Pass both cleaned and original data (original needed for is_client/is_supplier empty handling)
                prepared_company_data = prepare_company_data(clean_data,
                    {k: v for k, v in field_mapping.items() if k in company_fields}, client, country_cache, original_row_data=row_data)
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
                    prepared_supplier_data = prepare_supplier_update_data(supplier_fields)
                    updated_data, error = client.update_supplier(company_id, prepared_supplier_data)
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
            identifier_col = field_mapping.get(identifier_field)
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
    from . import create_api_client

    client = create_api_client(api_key, environment, custom_url)

    successful = []
    failed = []

    # Initialize country cache for address country lookups
    country_cache, error = client.get_all_countries()
    if error:
        print(f"Warning: Could not fetch countries: {error}. Country lookups will be disabled.")
        country_cache = {}

    # Pre-convert DataFrame to dict for better performance
    records = df.to_dict('records')

    for index, row_data in enumerate(records, 1):
        result = process_single_update(client, index, row_data, field_mapping, identifier_field, 'companies', dry_run, country_cache)

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
    from . import create_api_client

    client = create_api_client(api_key, environment, custom_url)

    preview_results = []

    # Get identifier column from mapping
    identifier_col = field_mapping.get(identifier_field)
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
    from . import create_api_client

    client = create_api_client(api_key, environment, custom_url)

    successful = []
    failed = []

    # Pre-convert DataFrame to dict for better performance
    records = df.to_dict('records')

    for index, row_data in enumerate(records, 1):
        result = process_single_update(client, index, row_data, field_mapping, identifier_field, 'persons', dry_run, None)

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
    from . import create_api_client

    client = create_api_client(api_key, environment, custom_url)

    preview_results = []

    # Get identifier column from mapping
    identifier_col = field_mapping.get(identifier_field)
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
