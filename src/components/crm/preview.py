"""
Preview Widgets Component

Reusable preview components for data visualization and validation.
Used across import and update workflows to show data samples and match previews.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Callable, Any


def render_data_preview(df: pd.DataFrame,
                       title: str = "Datenvorschau",
                       max_rows: int = 10,
                       large_dataset_threshold: int = 5000,
                       use_expander: bool = True) -> None:
    """
    Render a data preview with automatic size handling.

    Args:
        df: DataFrame to preview
        title: Title for the preview section
        max_rows: Maximum number of rows to display
        large_dataset_threshold: Row count threshold for "large dataset" warning
        use_expander: Whether to wrap in an expander
    """
    if df.empty:
        st.info("Keine Daten zum Anzeigen vorhanden")
        return

    total_rows = len(df)
    preview_df = df.head(max_rows)

    def _render_content():
        if total_rows > large_dataset_threshold:
            st.caption(f"📊 Großer Datensatz ({total_rows:,} Zeilen). Vorschau zeigt nur die ersten {max_rows} Zeilen.")
        else:
            st.caption(f"📊 {total_rows:,} Zeilen insgesamt")

        st.dataframe(preview_df, use_container_width=True)

    if use_expander:
        with st.expander(title, expanded=False):
            _render_content()
    else:
        st.markdown(f"**{title}**")
        _render_content()


def render_boolean_field_preview(df: pd.DataFrame,
                                 field_name: str,
                                 csv_column: Optional[str],
                                 title: str,
                                 icon: str = "✅",
                                 positive_label: str = "Aktiv",
                                 sample_rows: int = 3,
                                 name_column: Optional[str] = None) -> None:
    """
    Render a preview of boolean field values (e.g., is_client, is_supplier).

    Args:
        df: Source DataFrame
        field_name: API field name being previewed
        csv_column: CSV column mapped to this field
        title: Title for preview section
        icon: Icon to use for positive values
        positive_label: Label for positive (True) values
        sample_rows: Number of sample rows to show
        name_column: Column to use for entity names (defaults to first column)
    """
    if df.empty:
        return

    if not csv_column:
        st.info(f"💡 Ordnen Sie die '{field_name}'-Spalte zu, um die Vorschau zu sehen")
        return

    st.markdown(f"**{title}** 🔍")

    preview_data = []
    sample_data = df.head(sample_rows)
    count = 0

    # Determine name column
    if name_column and name_column in df.columns:
        entity_col = name_column
    else:
        entity_col = df.columns[0]

    for idx, row in sample_data.iterrows():
        entity_name = str(row.get(entity_col, f"Row {idx+1}"))

        # Check boolean value
        is_positive = False
        if csv_column in row:
            val = str(row[csv_column]).strip()
            if val and val.lower() not in ['false', '0', 'no', 'nein', '']:
                is_positive = True
                count += 1

        if is_positive:
            # Truncate long names
            display_name = entity_name[:25] + "..." if len(entity_name) > 25 else entity_name
            preview_data.append({
                "Name": display_name,
                "Status": f"{icon} {positive_label}"
            })

    if preview_data:
        preview_df = pd.DataFrame(preview_data)
        st.dataframe(preview_df, use_container_width=True, hide_index=True)
        st.info(f"📊 {count} Einträge in Beispieldaten gefunden")
    else:
        st.warning(f"Keine {positive_label.lower()}-Einträge in Beispieldaten erkannt")


def render_relationship_preview(df: pd.DataFrame,
                                field_mapping: Dict[str, str],
                                relationship_fields: List[tuple],
                                sample_rows: int = 3,
                                name_column: Optional[str] = None) -> None:
    """
    Render a preview showing multiple relationship fields side-by-side.

    Args:
        df: Source DataFrame
        field_mapping: Field mapping dictionary {api_field: csv_column}
        relationship_fields: List of (field_name, display_label, icon) tuples
        sample_rows: Number of sample rows to show
        name_column: Column to use for entity names

    Example:
        relationship_fields = [
            ('is_client', 'Kunde', '💼'),
            ('is_supplier', 'Lieferant', '🏭')
        ]
    """
    if df.empty:
        return

    # Check if any relationship field is mapped
    mapped_fields = [field for field, _, _ in relationship_fields if field_mapping.get(field)]

    if not mapped_fields:
        st.info("💡 Ordnen Sie Beziehungsspalten zu, um die Vorschau zu sehen")
        return

    st.markdown("**Beziehungsvorschau** 🔍")

    total_rows = len(df)
    if total_rows > 5000:
        st.caption(f"📊 Großer Datensatz ({total_rows:,} Zeilen). Vorschau zeigt nur die ersten {sample_rows} Zeilen.")

    preview_data = []
    sample_data = df.head(sample_rows)

    # Determine name column
    if name_column and name_column in df.columns:
        entity_col = name_column
    else:
        entity_col = df.columns[0]

    for idx, row in sample_data.iterrows():
        entity_name = str(row.get(entity_col, f"Row {idx+1}"))
        display_name = entity_name[:20] + "..." if len(entity_name) > 20 else entity_name

        row_data = {"Name": display_name}

        # Check each relationship field
        for field_name, display_label, icon in relationship_fields:
            csv_column = field_mapping.get(field_name)
            status = "❌"

            if csv_column and csv_column in row:
                val = str(row[csv_column]).strip()
                if val and val.lower() not in ['false', '0', 'no', 'nein', '']:
                    status = icon if icon else "✅"

            row_data[display_label] = status

        preview_data.append(row_data)

    if preview_data:
        preview_df = pd.DataFrame(preview_data)
        st.dataframe(preview_df, use_container_width=True, hide_index=True)


def render_match_preview(preview_results: Optional[Dict],
                        entity_type: str = "entity",
                        entity_icon: str = "📋") -> None:
    """
    Render match preview results for update operations.

    Args:
        preview_results: Preview results dictionary with 'matched', 'total', 'sample_matches'
        entity_type: Type of entity (e.g., "company", "person")
        entity_icon: Icon for the entity type
    """
    if not preview_results:
        return

    matched = preview_results.get('matched', 0)
    total = preview_results.get('total', 0)
    sample_matches = preview_results.get('sample_matches', [])

    st.markdown(f"### {entity_icon} Vorschau-Ergebnis")

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Gefunden", matched, help=f"Anzahl der gefundenen {entity_type}s im CRM")
    with col2:
        st.metric("Nicht gefunden", total - matched, help=f"Anzahl der nicht gefundenen {entity_type}s")
    with col3:
        match_rate = (matched / total * 100) if total > 0 else 0
        st.metric("Match-Rate", f"{match_rate:.1f}%")

    # Sample matches
    if sample_matches:
        with st.expander(f"🔍 Beispiel-Matches anzeigen (erste {len(sample_matches)})", expanded=False):
            for match in sample_matches:
                identifier = match.get('identifier', 'N/A')
                status = match.get('status', 'unknown')
                crm_id = match.get('crm_id')

                if status == 'found':
                    st.success(f"✅ **{identifier}** → CRM ID: {crm_id}")
                else:
                    error_msg = match.get('error', 'Nicht gefunden')
                    st.error(f"❌ **{identifier}** → {error_msg}")


def render_validation_messages(messages: List[str],
                               success_icon: str = "✅",
                               warning_icon: str = "⚠️",
                               error_icon: str = "❌") -> None:
    """
    Render validation messages with appropriate styling.

    Args:
        messages: List of message strings
        success_icon: Icon for success messages (starts with "Erfolg")
        warning_icon: Icon for warning messages (starts with "Warnung")
        error_icon: Icon for error messages (starts with "Fehler")
    """
    for message in messages:
        if message.startswith("Erfolg"):
            st.success(f"{success_icon} {message}")
        elif message.startswith("Warnung"):
            st.warning(f"{warning_icon} {message}")
        elif message.startswith("Fehler"):
            st.error(f"{error_icon} {message}")
        else:
            st.info(message)


def render_column_mapping_table(mapping: Dict[str, Any],
                                title: str = "Spalten-Zuordnung",
                                show_counts: bool = True) -> None:
    """
    Render a table showing column mappings with optional value counts.

    Args:
        mapping: Dictionary of mappings (can be nested for API mappings)
        title: Title for the mapping table
        show_counts: Whether to show value counts (requires DataFrame access)
    """
    if not mapping:
        st.info("Keine Zuordnungen vorhanden")
        return

    with st.expander(f"📋 {title}", expanded=False):
        # Convert mapping to displayable format
        if isinstance(list(mapping.values())[0], dict):
            # Nested mapping (e.g., Personio API mapping)
            for api_key, columns_dict in mapping.items():
                st.markdown(f"**{api_key}**")
                for col, api_field in columns_dict.items():
                    st.text(f"  {col} → {api_field}")
        else:
            # Simple mapping
            mapping_data = []
            for api_field, csv_column in mapping.items():
                mapping_data.append({
                    "API-Feld": api_field,
                    "CSV-Spalte": csv_column
                })

            if mapping_data:
                mapping_df = pd.DataFrame(mapping_data)
                st.dataframe(mapping_df, use_container_width=True, hide_index=True)
