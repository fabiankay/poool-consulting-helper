"""
Generic import operations for CRM system.

Handles single and bulk import processing for companies and persons.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from ..poool_api_client import PooolAPIClient


def process_single_import(client: PooolAPIClient, index: int, row_data: Dict, field_mapping: Dict, import_type: str, country_cache: Optional[Dict[str, int]] = None) -> Dict:
    """Process a single row import for companies or persons."""
    from .company_operations import prepare_company_data
    from .person_operations import prepare_person_data_with_company_lookup

    try:
        # Clean NaN values efficiently
        clean_data = {k: v for k, v in row_data.items() if pd.notna(v)}

        # Prepare data based on import type
        if import_type == 'companies':
            prepared_data = prepare_company_data(clean_data, field_mapping, client, country_cache)

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

    # Initialize country cache for address country lookups
    country_cache = {}
    if import_type == 'companies':
        # Fetch all countries once at the start of import
        country_cache, error = client.get_all_countries()
        if error:
            print(f"Warning: Could not fetch countries: {error}. Country lookups will be disabled.")
            country_cache = {}

    # Pre-convert DataFrame to dict for better performance
    records = df.to_dict('records')

    for index, row_data in enumerate(records, 1):
        result = process_single_import(client, index, row_data, field_mapping, import_type, country_cache)

        if result['success']:
            successful.append(result['result'])
        else:
            failed.append({
                'row': index,
                'data': {k: v for k, v in row_data.items() if pd.notna(v)},
                'error': result['error']
            })

    return successful, failed
