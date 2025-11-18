"""
Validation functions for CRM imports.

Handles data validation before import operations.
"""

from typing import Dict, List, Tuple


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

    # field_mapping structure is {api_field: csv_column}
    mapped_required = [api_field for api_field in field_mapping.keys() if api_field in required_fields]
    missing_required = [field for field in required_fields if field not in mapped_required]

    if missing_required:
        if import_type == 'companies':
            all_messages.append("Required field 'name' must be mapped for companies")
        else:
            all_messages.append(f"Required fields must be mapped: {', '.join(missing_required)}")

    # Column existence validation
    missing_columns = [col for col in field_mapping.values() if col and col not in df.columns]
    if missing_columns:
        all_messages.append(f"Mapped columns not found in file: {', '.join(missing_columns)}")

    # Data quality validation
    if import_type == 'companies':
        name_column = field_mapping.get('name')
        if name_column:
            empty_count = df[name_column].isna().sum() + (df[name_column] == '').sum()
            if empty_count > 0:
                all_messages.append(f"Warning: {empty_count} rows have empty company names and will be skipped")
    else:
        for required_field in ['firstname', 'lastname']:
            col = field_mapping.get(required_field)
            if col:
                empty_count = df[col].isna().sum() + (df[col] == '').sum()
                if empty_count > 0:
                    all_messages.append(f"Warning: {empty_count} rows have empty {required_field}s and will be skipped")

    # Determine if validation passed
    has_errors = any(not msg.startswith("Warning:") for msg in all_messages)
    return not has_errors, all_messages
