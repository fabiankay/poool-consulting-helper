"""
Field Mapping Builder Component

Reusable component for rendering field mapping UI across import and update pages.
Eliminates code duplication by providing a consistent interface for field mapping.
"""

import streamlit as st
from typing import Dict, List, Optional, Callable, Tuple


class FieldMappingBuilder:
    """
    Builder class for creating field mapping UI components.

    Supports both callback-based and direct state update patterns,
    with optional tabs for organizing fields by category.
    """

    def __init__(self,
                 csv_columns: List[str],
                 field_mapping_key: str = 'field_mapping',
                 field_examples: Optional[Dict[str, str]] = None,
                 field_labels: Optional[Dict[str, str]] = None,
                 on_change_callback: Optional[Callable] = None):
        """
        Initialize the field mapping builder.

        Args:
            csv_columns: List of available CSV columns (should include empty string at start)
            field_mapping_key: Session state key for field mapping dict
            field_examples: Dictionary of field examples/help text {field_name: help_text}
            field_labels: Dictionary of human-readable labels {api_field: display_label}
            on_change_callback: Optional callback function for field changes
        """
        self.csv_columns = csv_columns
        self.field_mapping_key = field_mapping_key
        self.field_examples = field_examples or {}
        self.field_labels = field_labels or {}
        self.on_change_callback = on_change_callback

    def get_field_label(self, field: str) -> str:
        """Get the display label for a field, falling back to the field name."""
        return self.field_labels.get(field, field)

    def get_current_mapping(self, field: str) -> str:
        """Get the current CSV column mapped to an API field."""
        field_mapping = st.session_state.get(self.field_mapping_key, {})
        return field_mapping.get(field, '')

    def update_mapping(self, field: str, selected_column: str) -> None:
        """Update the field mapping in session state."""
        if self.field_mapping_key not in st.session_state:
            st.session_state[self.field_mapping_key] = {}

        if selected_column and selected_column.strip() and selected_column != '':
            st.session_state[self.field_mapping_key][field] = selected_column
        else:
            # Remove mapping if empty selection
            if field in st.session_state[self.field_mapping_key]:
                del st.session_state[self.field_mapping_key][field]

    def render_field_selectbox(self,
                               field: str,
                               label: Optional[str] = None,
                               key_prefix: str = 'field',
                               use_callback: bool = False) -> Optional[str]:
        """
        Render a selectbox for a single field mapping.

        Args:
            field: API field name
            label: Display label (overrides field_labels if provided)
            key_prefix: Prefix for widget key (for uniqueness)
            use_callback: Whether to use on_change callback (True) or direct update (False)

        Returns:
            Selected column name (only if use_callback=False)
        """
        # Use provided label, or fall back to field_labels dict, or field name
        label = label or self.get_field_label(field)
        current_mapping = self.get_current_mapping(field)
        help_text = self.field_examples.get(field, f"CSV-Spalte für '{label}' zuordnen")

        # Calculate index safely
        try:
            default_index = self.csv_columns.index(current_mapping) if current_mapping and current_mapping in self.csv_columns else 0
        except (ValueError, IndexError):
            default_index = 0

        widget_key = f"{key_prefix}_{field}"

        if use_callback and self.on_change_callback:
            # Callback-based pattern (used in sites/crm.py)
            st.selectbox(
                label,
                options=self.csv_columns,
                index=default_index,
                key=widget_key,
                help=help_text,
                on_change=self.on_change_callback,
                args=(field, widget_key)
            )
            return None
        else:
            # Direct update pattern (used in update pages)
            selected = st.selectbox(
                label,
                options=self.csv_columns,
                index=default_index,
                key=widget_key,
                help=help_text
            )

            # Update mapping directly
            self.update_mapping(field, selected)
            return selected

    def render_field_group(self,
                          fields: List[str],
                          title: Optional[str] = None,
                          key_prefix: str = 'field',
                          use_callback: bool = False) -> None:
        """
        Render a group of field selectboxes.

        Args:
            fields: List of API field names to render
            title: Optional title/header for the group
            key_prefix: Prefix for widget keys
            use_callback: Whether to use callbacks
        """
        if title:
            st.markdown(f"**{title}**")

        for field in fields:
            self.render_field_selectbox(field, key_prefix=key_prefix, use_callback=use_callback)

    def render_tabbed_fields_from_dict(self,
                                      tab_config_dict: Dict[str, List[str]],
                                      use_callback: bool = False,
                                      num_columns: int = 2) -> None:
        """
        Render fields organized in tabs from a dictionary configuration.

        Args:
            tab_config_dict: Dictionary mapping tab name to list of fields
            use_callback: Whether to use callbacks
            num_columns: Number of columns for field layout within each tab (default 2)

        Example:
            tab_config_dict = {
                "Stammdaten": ['name', 'email'],
                "Adresse": ['street', 'city']
            }
        """
        tab_names = list(tab_config_dict.keys())
        tabs = st.tabs(tab_names)

        for idx, tab_name in enumerate(tab_names):
            fields = tab_config_dict[tab_name]

            with tabs[idx]:
                # Use column layout within tab for better space utilization
                if num_columns > 1 and len(fields) > 1:
                    # Split fields into columns
                    cols = st.columns(num_columns)
                    for field_idx, field in enumerate(fields):
                        col_idx = field_idx % num_columns
                        with cols[col_idx]:
                            key_prefix = f"{tab_name.lower().replace(' ', '_')}_{col_idx}"
                            self.render_field_selectbox(field, key_prefix=key_prefix, use_callback=use_callback)
                else:
                    # Single column layout
                    key_prefix = tab_name.lower().replace(" ", "_")
                    for field in fields:
                        self.render_field_selectbox(field, key_prefix=key_prefix, use_callback=use_callback)

    def render_columns_layout(self,
                             field_groups: List[Tuple[str, List[str]]],
                             use_callback: bool = False) -> None:
        """
        Render fields in a column layout.

        Args:
            field_groups: List of (title, fields_list) tuples for each column
            use_callback: Whether to use callbacks

        Example:
            field_groups = [
                ("Required Fields", ['firstname', 'lastname']),
                ("Optional Fields", ['phone', 'email'])
            ]
        """
        cols = st.columns(len(field_groups))

        for idx, (title, fields) in enumerate(field_groups):
            with cols[idx]:
                self.render_field_group(fields, title=title, key_prefix=f"col{idx}", use_callback=use_callback)

    def get_mapping_summary(self) -> Dict[str, str]:
        """Get the current field mapping as a dictionary."""
        return st.session_state.get(self.field_mapping_key, {}).copy()

    def get_mapped_fields_count(self) -> int:
        """Get the number of currently mapped fields."""
        return len([v for v in st.session_state.get(self.field_mapping_key, {}).values() if v])

    def validate_required_fields(self, required_fields: List[str]) -> Tuple[bool, List[str]]:
        """
        Validate that required fields are mapped.

        Args:
            required_fields: List of field names that must be mapped

        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        mapping = st.session_state.get(self.field_mapping_key, {})
        missing = []

        for field in required_fields:
            if field not in mapping or not mapping[field]:
                missing.append(field)

        return len(missing) == 0, missing


def create_simple_field_mapper(csv_columns: List[str],
                               fields: List[str],
                               field_mapping_key: str = 'field_mapping',
                               field_examples: Optional[Dict[str, str]] = None,
                               title: Optional[str] = None) -> FieldMappingBuilder:
    """
    Convenience function to create and render a simple field mapping UI.

    Args:
        csv_columns: List of CSV columns
        fields: List of API fields to map
        field_mapping_key: Session state key
        field_examples: Optional help text for fields
        title: Optional section title

    Returns:
        FieldMappingBuilder instance for further customization
    """
    builder = FieldMappingBuilder(csv_columns, field_mapping_key, field_examples)
    builder.render_field_group(fields, title=title)
    return builder
