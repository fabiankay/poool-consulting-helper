"""
Generic Entity Update Page Component

Configuration-driven component for rendering update workflows for different entity types.
Eliminates 95% code duplication between company and person update pages.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple, Optional, Callable, Any
from ..common.session_state_manager import init_session_state
from .ui import (
    render_environment_selector,
    render_api_configuration,
    render_file_uploader,
    render_mapping_summary,
    render_preview_matches,
    render_update_execution,
    render_update_results,
    render_wip_warning
)


class EntityUpdateConfig:
    """
    Configuration class for entity update page.

    Defines all entity-specific settings and functions for the generic update workflow.
    """

    def __init__(self,
                 entity_type: str,
                 entity_name: str,
                 entity_icon: str,
                 identifier_options: List[str],
                 default_identifier: str,
                 field_groups: List[Tuple[str, str, List[str]]],
                 get_all_fields_func: Callable[[], List[str]],
                 bulk_update_func: Callable,
                 preview_matches_func: Callable,
                 field_labels: Optional[Dict[str, str]] = None):
        """
        Initialize entity update configuration.

        Args:
            entity_type: Internal identifier ("company", "person")
            entity_name: Display name ("Firma", "Person")
            entity_icon: Emoji icon for the entity
            identifier_options: List of field options for matching (e.g., ['id', 'email', 'name'])
            default_identifier: Default identifier field
            field_groups: List of (tab_name, tab_title, field_list) for field mapping UI
            get_all_fields_func: Function that returns all available fields
            bulk_update_func: Function for bulk updates
            preview_matches_func: Function for preview matches
            field_labels: Optional dictionary mapping API fields to human-readable German labels
        """
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.entity_icon = entity_icon
        self.identifier_options = identifier_options
        self.default_identifier = default_identifier
        self.field_groups = field_groups
        self.get_all_fields_func = get_all_fields_func
        self.bulk_update_func = bulk_update_func
        self.preview_matches_func = preview_matches_func
        self.field_labels = field_labels or {}


def render_entity_update_page(config: EntityUpdateConfig,
                              page_title: str,
                              page_icon: str = "🔄") -> None:
    """
    Render a complete entity update page with consistent workflow.

    Args:
        config: EntityUpdateConfig instance with entity-specific settings
        page_title: Page title to display
        page_icon: Page icon for st.set_page_config
    """
    # Page configuration
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide"
    )

    st.title(f"{page_icon} {page_title}")
    st.markdown(f"Bestehende {config.entity_name}en im Poool CRM über die API aktualisieren")

    render_wip_warning()

    # Environment Toggle
    st.markdown("---")
    environment, custom_url = render_environment_selector()
    st.markdown("---")

    # Initialize session state
    init_session_state('update_page', overrides={'identifier_field': config.default_identifier})

    # API Configuration and File Upload
    col1, col2 = st.columns([1, 2])

    with col1:
        api_key, is_connected = render_api_configuration(
            lambda key, env, url: __import__('src.helpers.crm', fromlist=['test_api_connection']).test_api_connection(key, env, url)
        )

    with col2:
        df = render_file_uploader("update")

    # Main update workflow
    if st.session_state.uploaded_data is not None and st.session_state.crm_api_key:
        st.markdown("---")
        st.subheader("🎯 Aktualisierungskonfiguration")

        df = st.session_state.uploaded_data
        csv_columns = [''] + list(df.columns)

        # Identifier Selection
        st.markdown("### 1️⃣ Identifikationsfeld auswählen")
        st.markdown("Wählen Sie, welches Feld zum Abgleich bestehender Datensätze verwendet werden soll:")

        col1, col2 = st.columns(2)

        with col1:
            identifier_field = st.selectbox(
                "Datensätze abgleichen nach:",
                options=config.identifier_options,
                help=f"Feld zum Identifizieren bestehender {config.entity_name}en im CRM"
            )
            st.session_state.identifier_field = identifier_field

        with col2:
            st.info(f"📌 Identifikator: **{identifier_field}**\n\nStellen Sie sicher, dass Sie dieses Feld im nächsten Schritt zuordnen!")

        # Field Mapping
        st.markdown("### 2️⃣ Felder zum Aktualisieren zuordnen")
        st.markdown("Ordnen Sie CSV-Spalten den API-Feldern zu. Nur zugeordnete Felder werden aktualisiert.")

        # Get all available fields
        all_fields = config.get_all_fields_func()

        # Render field mapping in tabs
        _render_field_mapping_tabs(config.field_groups, all_fields, csv_columns, config.field_labels)

        # Show current mapping summary
        render_mapping_summary(st.session_state.field_mapping)

        # Preview Matches
        render_preview_matches(
            df,
            st.session_state.field_mapping,
            st.session_state.identifier_field,
            config.preview_matches_func,
            entity_type=config.entity_type
        )

        # Execute Update
        render_update_execution(
            df,
            st.session_state.field_mapping,
            st.session_state.identifier_field,
            config.bulk_update_func,
            entity_type=config.entity_type,
            entity_icon=config.entity_icon
        )

    # Show Results
    render_update_results(st.session_state.get('update_results'))


def _render_field_mapping_tabs(field_groups: List[Tuple[str, str, List[str]]],
                               all_fields: List[str],
                               csv_columns: List[str],
                               field_labels: Optional[Dict[str, str]] = None) -> None:
    """
    Render field mapping selectboxes organized in tabs with 2-column layout.

    Args:
        field_groups: List of (tab_name, tab_title, field_list) tuples
        all_fields: List of all available fields (for validation)
        csv_columns: List of CSV columns to choose from
        field_labels: Optional dictionary mapping API fields to human-readable labels
    """
    from .field_mapping import FieldMappingBuilder

    # Create builder with labels
    builder = FieldMappingBuilder(
        csv_columns=csv_columns,
        field_mapping_key='field_mapping',
        field_labels=field_labels or {}
    )

    tab_names = [group[0] for group in field_groups]
    tabs = st.tabs(tab_names)

    for idx, (tab_name, tab_title, fields) in enumerate(field_groups):
        with tabs[idx]:
            if tab_title:
                st.markdown(f"**{tab_title}**")

            # Filter fields that exist
            valid_fields = [f for f in fields if f in all_fields]

            # Use 2-column layout for better space utilization
            if len(valid_fields) > 1:
                cols = st.columns(2)
                for field_idx, field in enumerate(valid_fields):
                    col_idx = field_idx % 2
                    with cols[col_idx]:
                        key_prefix = f"update_{tab_name.lower().replace(' ', '_')}_{col_idx}"
                        builder.render_field_selectbox(field, key_prefix=key_prefix, use_callback=False)
            else:
                # Single column for single field
                for field in valid_fields:
                    key_prefix = f"update_{tab_name.lower().replace(' ', '_')}"
                    builder.render_field_selectbox(field, key_prefix=key_prefix, use_callback=False)


# Helper function to create company update configuration
def create_company_update_config() -> EntityUpdateConfig:
    """
    Create configuration for company update page.

    Returns:
        EntityUpdateConfig for companies
    """
    from src.helpers.crm import (
        get_required_company_fields,
        get_optional_company_fields,
        bulk_update_companies,
        preview_company_matches,
        get_company_field_tabs,
        get_company_field_labels
    )

    all_fields = get_required_company_fields() + get_optional_company_fields()
    field_tabs = get_company_field_tabs()
    field_labels = get_company_field_labels()

    # Convert dict-based tabs to tuple-based format: (tab_name, tab_title, fields)
    field_groups = [
        (tab_name, tab_name, fields) for tab_name, fields in field_tabs.items()
    ]

    return EntityUpdateConfig(
        entity_type="company",
        entity_name="Firma",
        entity_icon="🔄",
        identifier_options=['id', 'name', 'customer_number'],
        default_identifier='id',
        field_groups=field_groups,
        get_all_fields_func=lambda: all_fields,
        bulk_update_func=bulk_update_companies,
        preview_matches_func=preview_company_matches,
        field_labels=field_labels
    )


# Helper function to create person update configuration
def create_person_update_config() -> EntityUpdateConfig:
    """
    Create configuration for person update page.

    Returns:
        EntityUpdateConfig for persons
    """
    from src.helpers.crm import (
        get_required_person_fields,
        get_optional_person_fields,
        bulk_update_persons,
        preview_person_matches,
        get_person_field_tabs,
        get_person_field_labels
    )

    all_fields = get_required_person_fields() + get_optional_person_fields()
    field_tabs = get_person_field_tabs()
    field_labels = get_person_field_labels()

    # Convert dict-based tabs to tuple-based format: (tab_name, tab_title, fields)
    field_groups = [
        (tab_name, tab_name, fields) for tab_name, fields in field_tabs.items()
    ]

    return EntityUpdateConfig(
        entity_type="person",
        entity_name="Person",
        entity_icon="👤",
        identifier_options=['id', 'email', 'firstname', 'lastname'],
        default_identifier='id',
        field_groups=field_groups,
        get_all_fields_func=lambda: all_fields,
        bulk_update_func=bulk_update_persons,
        preview_matches_func=preview_person_matches,
        field_labels=field_labels
    )
