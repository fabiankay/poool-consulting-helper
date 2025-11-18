"""
Company-related operations for CRM system.

Handles company data preparation, bulk imports, country lookups,
and complex field processing (addresses, contacts).
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from ..poool_api_client import PooolAPIClient


def lookup_or_create_country_id(client: PooolAPIClient, country_name: str, country_cache: Dict[str, int]) -> Optional[int]:
    """
    Look up country ID by name, or create country if it doesn't exist.

    Searches the country cache (case-insensitive) for the country name. If not found,
    creates a new country via API and adds it to the cache.

    Args:
        client: PooolAPIClient instance
        country_name: Name of the country to look up or create
        country_cache: Dict mapping lowercase country names to IDs (mutated if country is created)

    Returns:
        Country ID if found/created, None if error
    """
    if not country_name or not country_name.strip():
        return None

    # Normalize the country name for lookup
    normalized_name = country_name.strip().lower()

    # Check if country exists in cache
    if normalized_name in country_cache:
        return country_cache[normalized_name]

    # Country not found in cache, create it
    created_country, error = client.create_country(country_name)

    if error:
        # Log error but don't fail the import
        print(f"Warning: Could not create country '{country_name}': {error}")
        return None

    if created_country and 'id' in created_country:
        country_id = created_country['id']

        # Add all name variants to cache for future lookups
        if created_country.get('name_german'):
            country_cache[created_country['name_german'].lower()] = country_id
        if created_country.get('name_local'):
            country_cache[created_country['name_local'].lower()] = country_id
        if created_country.get('name_international'):
            country_cache[created_country['name_international'].lower()] = country_id
        if created_country.get('iso_3166_alpha2'):
            country_cache[created_country['iso_3166_alpha2'].lower()] = country_id
        if created_country.get('iso_3166_alpha3'):
            country_cache[created_country['iso_3166_alpha3'].lower()] = country_id

        # Also add the original name used for creation
        country_cache[normalized_name] = country_id

        return country_id

    return None


def _add_complex_fields_to_company(company_data: Dict, complex_fields: Dict, client: Optional[PooolAPIClient] = None, country_cache: Optional[Dict[str, int]] = None) -> None:
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
        # Use provided title or default to "Hauptanschrift"
        address_title = complex_fields.get("address_title", "Hauptanschrift")
        address = {"is_preferred": True, "pos": 1, "title": address_title}
        address.update({k: v for k, v in address_data.items() if v})

        # Handle country if provided
        if complex_fields.get("address_country"):
            if client and country_cache is not None:
                country_id = lookup_or_create_country_id(
                    client,
                    complex_fields["address_country"],
                    country_cache
                )
                if country_id:
                    address["country_id"] = country_id

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


def prepare_company_data(row_data: Dict, field_mapping: Dict, client: Optional[PooolAPIClient] = None, country_cache: Optional[Dict[str, int]] = None, original_row_data: Optional[Dict] = None) -> Dict:
    """Prepare company data for API submission using field mapping.

    Args:
        row_data: Cleaned row data (NaN values removed)
        field_mapping: Mapping of API fields to CSV columns
        client: Optional API client for lookups
        country_cache: Optional country cache for address processing
        original_row_data: Original uncleaned row data (needed for is_client/is_supplier empty value handling)
    """
    from .field_definitions import get_field_api_name_mapping

    company_data = {}
    complex_fields = {}
    field_name_mapping = get_field_api_name_mapping()

    # Use original_row_data for checking empty values, fallback to row_data if not provided
    check_data = original_row_data if original_row_data is not None else row_data

    # Handle is_client and is_supplier specially - they need explicit false for empty cells
    for boolean_field in ['is_client', 'is_supplier']:
        if boolean_field in field_mapping:
            csv_column = field_mapping[boolean_field]
            if csv_column and csv_column in check_data:
                import pandas as pd
                value = check_data[csv_column]
                # Check if value is NaN/None or empty string
                if pd.isna(value) or (isinstance(value, str) and not value.strip()):
                    company_data[boolean_field] = False
                    print(f"DEBUG: {boolean_field} set to False (empty cell in column '{csv_column}')")
                else:
                    # Any non-empty value = True
                    company_data[boolean_field] = True
                    print(f"DEBUG: {boolean_field} set to True (value: {value})")
            elif csv_column:
                # Column mapped but doesn't exist in data
                company_data[boolean_field] = False
                print(f"DEBUG: {boolean_field} set to False (column '{csv_column}' not found)")

    # Process all fields in a single loop
    for api_field, csv_column in field_mapping.items():
        # Skip is_client and is_supplier - already handled above
        if api_field in ["is_client", "is_supplier"]:
            continue

        if not csv_column or csv_column not in row_data:
            continue

        value = row_data[csv_column]
        if value is None:
            continue

        str_value = str(value).strip()

        # Map internal field name to actual API field name if needed
        actual_api_field = field_name_mapping.get(api_field, api_field)

        # Special handling for name_token - remove ALL spaces and append "abc" for testing
        if actual_api_field == 'name_token' and str_value:
            original_value = str_value
            str_value = str_value.replace(' ', '') + 'abc'
            print(f"DEBUG: name_token processed - original: '{value}', trimmed: '{original_value.replace(' ', '')}', final: '{str_value}'")

        # Debug logging for UID field
        if actual_api_field == 'uid' and str_value:
            print(f"DEBUG: Processing UID field - csv_column: {csv_column}, value: {value}, str_value: {str_value}")

        # Handle different field types (is_client/is_supplier already handled above)
        if actual_api_field in ["reference_number_required", "dunning_blocked", "datev_is_client_collection"]:
            if str_value.lower() in ['true', '1', 'yes']:
                company_data[actual_api_field] = "1"
            elif str_value.lower() in ['false', '0', 'no']:
                company_data[actual_api_field] = "0"
            elif str_value:
                company_data[actual_api_field] = "1"
        elif actual_api_field in ["payment_time_day_num", "discount_day_num"]:
            if str_value.isdigit():
                company_data[actual_api_field] = int(str_value)
        elif actual_api_field == "discount_percentage":
            try:
                company_data[actual_api_field] = float(str_value.replace(',', '.'))
            except ValueError:
                pass
        elif actual_api_field.startswith(("address_", "contact_")):
            if str_value:
                complex_fields[actual_api_field] = str_value
        elif str_value:
            company_data[actual_api_field] = str_value
            # Debug logging for UID field storage
            if actual_api_field == 'uid':
                print(f"DEBUG: UID stored in company_data: {company_data[actual_api_field]}")

    # Process complex fields if any exist
    if complex_fields:
        _add_complex_fields_to_company(company_data, complex_fields, client, country_cache)

    # Final debug check for UID
    if 'uid' in company_data:
        print(f"DEBUG: Final company_data contains UID: {company_data.get('uid')}")
    elif 'uid' in field_mapping:
        print(f"DEBUG: UID was mapped but NOT in final company_data. field_mapping['uid'] = {field_mapping.get('uid')}")

    return company_data


def bulk_import_companies(api_key: str, df, field_mapping: Dict, environment: str = "production", custom_url: str = None, tag_mappings: Dict = None) -> Tuple[List[Dict], List[Dict]]:
    """Import multiple companies from DataFrame."""
    from . import create_api_client
    from .import_operations import bulk_import_generic

    client = create_api_client(api_key, environment, custom_url)
    return bulk_import_generic(client, df, field_mapping, 'companies', tag_mappings)
