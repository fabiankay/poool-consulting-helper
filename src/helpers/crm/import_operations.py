"""
Generic import operations for CRM system.

Handles single and bulk import processing for companies and persons.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from ..poool_api_client import PooolAPIClient


def process_single_import(client: PooolAPIClient, index: int, row_data: Dict, field_mapping: Dict, import_type: str, country_cache: Optional[Dict[str, int]] = None, tag_mappings: Optional[Dict] = None, tag_cache: Optional[Dict[str, int]] = None, client_number_range_id: Optional[int] = None, supplier_number_range_id: Optional[int] = None) -> Dict:
    """Process a single row import for companies or persons."""
    from .company_operations import prepare_company_data
    from .person_operations import prepare_person_data_with_company_lookup
    from .update_operations import separate_update_fields_by_endpoint, prepare_supplier_update_data
    from .tag_operations import process_entity_tags
    from .field_definitions import get_client_fields, get_supplier_fields

    try:
        # Clean NaN values efficiently
        clean_data = {k: v for k, v in row_data.items() if pd.notna(v)}

        # Prepare data based on import type
        if import_type == 'companies':
            # Separate fields by endpoint (company vs client vs supplier)
            company_fields, client_fields, supplier_fields = separate_update_fields_by_endpoint(clean_data, field_mapping)

            # Prepare company data with company-level fields only
            # Use internal field names for comparison (not API field names from client_fields/supplier_fields)
            client_field_names = set(get_client_fields())
            supplier_field_names = set(get_supplier_fields())
            company_field_mapping = {k: v for k, v in field_mapping.items() if k not in client_field_names and k not in supplier_field_names}
            prepared_data = prepare_company_data(clean_data, company_field_mapping, client, country_cache, original_row_data=row_data)

            # Process tags if tag_mappings provided
            if tag_mappings and tag_cache is not None:
                tag_ids, created_tags, tag_error = process_entity_tags(
                    client,
                    pd.Series(row_data),  # Convert dict to Series for tag processing
                    tag_mappings,
                    tag_cache,
                    auto_create=True
                )
                if tag_error:
                    print(f"Warning: Tag processing failed for row {index}: {tag_error}")
                elif tag_ids:
                    prepared_data['tags'] = tag_ids
                    if created_tags:
                        print(f"Created new tags for row {index}: {', '.join(created_tags)}")

            # Early validation
            if not prepared_data.get('name'):
                return {
                    'success': False,
                    'error': 'Missing required field: name'
                }

            # Store activation flags before removing from company data
            should_activate_client = prepared_data.pop('is_client', False)
            should_activate_supplier = prepared_data.pop('is_supplier', False)

            # Create the company first (without is_client/is_supplier - these are set by POST /clients and /suppliers)
            created_item, error = client.create_company(prepared_data)

            if error:
                return {
                    'success': False,
                    'error': f'Company creation failed: {error}'
                }

            # Get created company ID
            company_id = created_item.get('id')
            if not company_id:
                return {
                    'success': False,
                    'error': 'Company created but no ID returned'
                }

            # Track activation results
            activation_results = []
            activation_errors = []

            # Activate as client if needed (use create_client with POST /clients)
            if should_activate_client:
                client_data_to_send = client_fields.copy() if client_fields else {}
                client_result, client_error = client.create_client(company_id, client_data_to_send, client_number_range_id)
                if client_error:
                    activation_errors.append(f"Client creation failed: {client_error}")
                else:
                    activation_results.append('client')

            # Activate as supplier if needed (use create_supplier with POST /suppliers)
            if should_activate_supplier:
                supplier_data_to_send = prepare_supplier_update_data(supplier_fields) if supplier_fields else {}
                supplier_result, supplier_error = client.create_supplier(company_id, supplier_data_to_send, supplier_number_range_id)
                if supplier_error:
                    activation_errors.append(f"Supplier creation failed: {supplier_error}")
                else:
                    activation_results.append('supplier')

            # Return result with activation info
            result = {
                'success': True,
                'result': {
                    'row': index,
                    'data': clean_data,
                    'created': created_item
                }
            }

            if activation_results:
                result['result']['activated'] = activation_results

            if activation_errors:
                result['result']['activation_warnings'] = activation_errors

            return result

        else:
            # Use enhanced person preparation with company lookup
            prepared_data, lookup_warnings = prepare_person_data_with_company_lookup(client, clean_data, field_mapping)

            # Process tags if tag_mappings provided
            if tag_mappings and tag_cache is not None:
                tag_ids, created_tags, tag_error = process_entity_tags(
                    client,
                    pd.Series(row_data),
                    tag_mappings,
                    tag_cache,
                    auto_create=True
                )
                if tag_error:
                    print(f"Warning: Tag processing failed for row {index}: {tag_error}")
                elif tag_ids:
                    prepared_data['tags'] = tag_ids
                    if created_tags:
                        print(f"Created new tags for row {index}: {', '.join(created_tags)}")

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

    # Initialize country cache for address country lookups
    country_cache = {}
    if import_type == 'companies':
        # Fetch all countries once at the start of import
        country_cache, error = client.get_all_countries()
        if error:
            print(f"Warning: Could not fetch countries: {error}. Country lookups will be disabled.")
            country_cache = {}

    # Initialize tag cache for tag lookups
    tag_cache = {}
    if tag_mappings:
        # Fetch all tags once at the start of import
        tag_cache, error = client.get_all_tags()
        if error:
            print(f"Warning: Could not fetch tags: {error}. Tag processing will be disabled.")
            tag_cache = {}
        else:
            print(f"Loaded {len(tag_cache)} tags for import processing")

    # Fetch default number_range_ids for client/supplier activation
    client_number_range_id = None
    supplier_number_range_id = None
    if import_type == 'companies':
        client_number_range_id, error = client.get_default_number_range_id("client")
        if error:
            print(f"Warning: Could not fetch client number range: {error}")
        supplier_number_range_id, error = client.get_default_number_range_id("supplier")
        if error:
            print(f"Warning: Could not fetch supplier number range: {error}")

    # Pre-convert DataFrame to dict for better performance
    records = df.to_dict('records')

    for index, row_data in enumerate(records, 1):
        result = process_single_import(client, index, row_data, field_mapping, import_type, country_cache, tag_mappings, tag_cache, client_number_range_id, supplier_number_range_id)

        if result['success']:
            successful.append(result['result'])
        else:
            failed.append({
                'row': index,
                'data': {k: v for k, v in row_data.items() if pd.notna(v)},
                'error': result['error']
            })

    return successful, failed
