"""
CRM UI Components

Reusable components for CRM operations (import, update, field mapping).
"""

# UI components
from .ui import (
    render_wip_warning,
    render_environment_selector,
    render_api_configuration,
    render_file_uploader,
    render_results_display,
    get_csv_columns,
    render_mapping_summary,
    render_preview_matches,
    render_update_execution,
    render_update_results,
)

# Entity update page
from .entity_update import (
    EntityUpdateConfig,
    render_entity_update_page,
    create_company_update_config,
    create_person_update_config,
)

# Field mapping
from .field_mapping import (
    FieldMappingBuilder,
    create_simple_field_mapper,
)

# Preview widgets
from .preview import (
    render_data_preview,
    render_boolean_field_preview,
    render_relationship_preview,
    render_match_preview,
    render_validation_messages,
    render_column_mapping_table,
)

__all__ = [
    # UI components
    'render_wip_warning',
    'render_environment_selector',
    'render_api_configuration',
    'render_file_uploader',
    'render_results_display',
    'get_csv_columns',
    'render_mapping_summary',
    'render_preview_matches',
    'render_update_execution',
    'render_update_results',

    # Entity update
    'EntityUpdateConfig',
    'render_entity_update_page',
    'create_company_update_config',
    'create_person_update_config',

    # Field mapping
    'FieldMappingBuilder',
    'create_simple_field_mapper',

    # Preview
    'render_data_preview',
    'render_boolean_field_preview',
    'render_relationship_preview',
    'render_match_preview',
    'render_validation_messages',
    'render_column_mapping_table',
]
