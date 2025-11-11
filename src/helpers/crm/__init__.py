"""
CRM helper functions using the PooolAPIClient class.

Provides functions for importing companies and persons, handling field mappings,
validation, and tag management for the Poool CRM system.
"""

from typing import Tuple
from ..poool_api_client import PooolAPIClient

# Core API client functions (kept in __init__.py as they're used everywhere)
def create_api_client(api_key: str, environment: str = "production", custom_url: str = None) -> PooolAPIClient:
    """Create and return a configured API client."""
    return PooolAPIClient(api_key, environment, custom_url)


def test_api_connection(api_key: str, environment: str = "production", custom_url: str = None) -> Tuple[bool, str]:
    """Test API connection using the API client."""
    client = create_api_client(api_key, environment, custom_url)
    return client.test_connection()


# Import all public functions from submodules
from .field_definitions import (
    get_required_company_fields,
    get_optional_company_fields,
    get_required_person_fields,
    get_optional_person_fields,
    get_client_fields,
    get_supplier_fields,
    get_company_field_labels,
    get_person_field_labels,
    get_company_field_tabs,
    get_person_field_tabs,
)

from .company_operations import (
    lookup_or_create_country_id,
    prepare_company_data,
    bulk_import_companies,
)

from .person_operations import (
    prepare_person_data,
    prepare_person_data_with_company_lookup,
    bulk_import_persons,
)

from .tag_operations import (
    parse_comma_separated_tags,
    get_tag_ids_for_names,
    detect_tag_columns,
    process_entity_tags,
)

from .validation import (
    validate_import_data,
)

from .import_operations import (
    process_single_import,
    bulk_import_generic,
)

from .update_operations import (
    separate_update_fields_by_endpoint,
    prepare_supplier_update_data,
    match_company_by_identifier,
    match_person_by_identifier,
    process_single_update,
    bulk_update_companies,
    preview_company_matches,
    bulk_update_persons,
    preview_person_matches,
)

# Define public API
__all__ = [
    # Core functions
    'create_api_client',
    'test_api_connection',

    # Field definitions
    'get_required_company_fields',
    'get_optional_company_fields',
    'get_required_person_fields',
    'get_optional_person_fields',
    'get_client_fields',
    'get_supplier_fields',
    'get_company_field_labels',
    'get_person_field_labels',
    'get_company_field_tabs',
    'get_person_field_tabs',

    # Company operations
    'lookup_or_create_country_id',
    'prepare_company_data',
    'bulk_import_companies',

    # Person operations
    'prepare_person_data',
    'prepare_person_data_with_company_lookup',
    'bulk_import_persons',

    # Tag operations
    'parse_comma_separated_tags',
    'get_tag_ids_for_names',
    'detect_tag_columns',
    'process_entity_tags',

    # Validation
    'validate_import_data',

    # Import operations
    'process_single_import',
    'bulk_import_generic',

    # Update operations
    'separate_update_fields_by_endpoint',
    'prepare_supplier_update_data',
    'match_company_by_identifier',
    'match_person_by_identifier',
    'process_single_update',
    'bulk_update_companies',
    'preview_company_matches',
    'bulk_update_persons',
    'preview_person_matches',
]
