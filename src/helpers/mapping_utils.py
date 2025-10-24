"""
Utilities for field mapping and JSON import/export.

Provides helper functions for managing field mappings, tag mappings,
and configuration import/export in JSON format.
"""

import json
import streamlit as st
from typing import Dict, List, Tuple


def get_current_mapping_for_field(field: str, field_mapping: Dict[str, str]) -> str:
    """
    Get the currently mapped CSV column for a given API field.

    Args:
        field: API field name to look up
        field_mapping: Dictionary mapping CSV columns to API fields

    Returns:
        CSV column name if mapped, empty string otherwise
    """
    for csv_col, api_field in field_mapping.items():
        if api_field == field:
            return csv_col
    return ''


def export_mapping_to_json(field_mapping: Dict[str, str],
                           final_tag_mappings: Dict[str, str] = None,
                           manual_tag_mappings: Dict[str, List[str]] = None) -> str:
    """
    Export field mapping configuration to JSON format.

    Args:
        field_mapping: Dictionary mapping CSV columns to API fields
        final_tag_mappings: Optional dictionary of tag column mappings
        manual_tag_mappings: Optional dictionary of manual tag assignments

    Returns:
        JSON string of mapping configuration
    """
    mapping_config = {
        "field_mapping": field_mapping,
        "final_tag_mappings": final_tag_mappings or {},
        "manual_tag_mappings": manual_tag_mappings or {}
    }

    return json.dumps(mapping_config, indent=2)


def import_mapping_from_json(json_content: str, csv_columns: List[str]) -> Tuple[Dict, List[str]]:
    """
    Import mapping configuration from JSON with validation.

    Args:
        json_content: JSON string containing mapping configuration
        csv_columns: List of available CSV column names

    Returns:
        Tuple of (imported_config, messages) where:
        - imported_config contains 'field_mapping', 'final_tag_mappings', 'manual_tag_mappings'
        - messages is a list of success/warning/error messages
    """
    messages = []
    imported_config = {
        'field_mapping': {},
        'final_tag_mappings': {},
        'manual_tag_mappings': {}
    }

    try:
        mapping_config = json.loads(json_content)

        # Validate JSON structure
        if not isinstance(mapping_config, dict):
            return imported_config, ["Error: JSON must be an object/dictionary"]

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

            imported_config['field_mapping'] = matched_mappings

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

            imported_config['final_tag_mappings'] = matched_tag_mappings

            if matched_tag_mappings:
                messages.append(f"Success: Imported {len(matched_tag_mappings)} tag mappings")

            if missing_tag_columns:
                messages.append(f"Warning: {len(missing_tag_columns)} tag columns from JSON not found in CSV")

        # Import manual tag mappings
        if 'manual_tag_mappings' in mapping_config:
            imported_config['manual_tag_mappings'] = mapping_config['manual_tag_mappings']
            messages.append(f"Success: Imported manual tag mappings")

        return imported_config, messages

    except json.JSONDecodeError as e:
        return imported_config, [f"Error: Invalid JSON format - {str(e)}"]
    except Exception as e:
        return imported_config, [f"Error: Failed to import mapping - {str(e)}"]
