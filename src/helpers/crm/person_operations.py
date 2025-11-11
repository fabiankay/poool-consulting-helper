"""
Person-related operations for CRM system.

Handles person data preparation, bulk imports, and company lookups.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from ..poool_api_client import PooolAPIClient


def prepare_person_data(row_data: Dict, field_mapping: Dict) -> Dict:
    """Prepare person data for API submission using field mapping."""
    person_data = {}
    contacts_data = {}

    # Process each mapped field
    for api_field, csv_column in field_mapping.items():
        if csv_column and csv_column in row_data:
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


def bulk_import_persons(api_key: str, df, field_mapping: Dict, environment: str = "production", custom_url: str = None, tag_mappings: Dict = None) -> Tuple[List[Dict], List[Dict]]:
    """Import multiple persons from DataFrame."""
    from . import create_api_client
    from .import_operations import bulk_import_generic

    client = create_api_client(api_key, environment, custom_url)
    return bulk_import_generic(client, df, field_mapping, 'persons', tag_mappings)
