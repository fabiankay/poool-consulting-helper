"""
Export Utilities

Common functions for exporting data in various formats (CSV, Excel, JSON)
and creating download buttons with consistent naming and formatting.
"""

import pandas as pd
import json
import streamlit as st
from io import BytesIO
from datetime import datetime
from typing import Dict, Any, Optional


def generate_filename(base_name: str, extension: str, include_timestamp: bool = True) -> str:
    """
    Generate a filename with optional timestamp.

    Args:
        base_name: Base name for the file (e.g., "personio_employees")
        extension: File extension without dot (e.g., "csv", "xlsx", "json")
        include_timestamp: Whether to include timestamp in filename

    Returns:
        Formatted filename string
    """
    if include_timestamp:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{base_name}_{timestamp}.{extension}"
    return f"{base_name}.{extension}"


def dataframe_to_csv(df: pd.DataFrame, index: bool = False) -> str:
    """
    Convert DataFrame to CSV string.

    Args:
        df: DataFrame to convert
        index: Whether to include index in CSV

    Returns:
        CSV string
    """
    return df.to_csv(index=index)


def dataframe_to_excel(df: pd.DataFrame,
                       sheet_name: str = 'Data',
                       index: bool = False) -> bytes:
    """
    Convert DataFrame to Excel file in memory.

    Args:
        df: DataFrame to convert
        sheet_name: Name of the Excel sheet
        index: Whether to include index

    Returns:
        Excel file as bytes
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=index, sheet_name=sheet_name)
    output.seek(0)
    return output.getvalue()


def dict_to_json(data: Dict[str, Any],
                 pretty: bool = True,
                 ensure_ascii: bool = False) -> str:
    """
    Convert dictionary to JSON string.

    Args:
        data: Dictionary to convert
        pretty: Whether to format with indentation
        ensure_ascii: Whether to escape non-ASCII characters

    Returns:
        JSON string
    """
    indent = 2 if pretty else None
    return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)


def create_csv_download_button(df: pd.DataFrame,
                               button_label: str,
                               base_filename: str,
                               key: Optional[str] = None,
                               include_timestamp: bool = True,
                               include_index: bool = False,
                               help_text: Optional[str] = None) -> None:
    """
    Create a download button for CSV export.

    Args:
        df: DataFrame to export
        button_label: Label for the download button
        base_filename: Base name for the file (without extension)
        key: Unique key for the button
        include_timestamp: Whether to include timestamp in filename
        include_index: Whether to include DataFrame index in CSV
        help_text: Optional help text for the button
    """
    csv_data = dataframe_to_csv(df, index=include_index)
    filename = generate_filename(base_filename, 'csv', include_timestamp)

    st.download_button(
        label=button_label,
        data=csv_data,
        file_name=filename,
        mime='text/csv',
        key=key,
        help=help_text
    )


def create_excel_download_button(df: pd.DataFrame,
                                 button_label: str,
                                 base_filename: str,
                                 sheet_name: str = 'Data',
                                 key: Optional[str] = None,
                                 include_timestamp: bool = True,
                                 include_index: bool = False,
                                 help_text: Optional[str] = None) -> None:
    """
    Create a download button for Excel export.

    Args:
        df: DataFrame to export
        button_label: Label for the download button
        base_filename: Base name for the file (without extension)
        sheet_name: Name of the Excel sheet
        key: Unique key for the button
        include_timestamp: Whether to include timestamp in filename
        include_index: Whether to include DataFrame index
        help_text: Optional help text for the button
    """
    excel_data = dataframe_to_excel(df, sheet_name=sheet_name, index=include_index)
    filename = generate_filename(base_filename, 'xlsx', include_timestamp)

    st.download_button(
        label=button_label,
        data=excel_data,
        file_name=filename,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key=key,
        help=help_text
    )


def create_json_download_button(data: Dict[str, Any],
                                button_label: str,
                                base_filename: str,
                                key: Optional[str] = None,
                                include_timestamp: bool = True,
                                pretty: bool = True,
                                help_text: Optional[str] = None) -> None:
    """
    Create a download button for JSON export.

    Args:
        data: Dictionary to export as JSON
        button_label: Label for the download button
        base_filename: Base name for the file (without extension)
        key: Unique key for the button
        include_timestamp: Whether to include timestamp in filename
        pretty: Whether to format JSON with indentation
        help_text: Optional help text for the button
    """
    json_data = dict_to_json(data, pretty=pretty)
    filename = generate_filename(base_filename, 'json', include_timestamp)

    st.download_button(
        label=button_label,
        data=json_data,
        file_name=filename,
        mime='application/json',
        key=key,
        help=help_text
    )


def render_download_options(df: pd.DataFrame,
                           base_filename: str,
                           formats: list = ['csv', 'excel'],
                           csv_label: str = "📄 Als CSV herunterladen",
                           excel_label: str = "📊 Als Excel herunterladen",
                           sheet_name: str = 'Data',
                           include_timestamp: bool = True) -> None:
    """
    Render download buttons for multiple formats in columns.

    Args:
        df: DataFrame to export
        base_filename: Base name for files (without extension)
        formats: List of formats to include ('csv', 'excel')
        csv_label: Label for CSV download button
        excel_label: Label for Excel download button
        sheet_name: Sheet name for Excel export
        include_timestamp: Whether to include timestamp in filenames
    """
    cols = st.columns(len(formats))

    for idx, fmt in enumerate(formats):
        with cols[idx]:
            if fmt == 'csv':
                create_csv_download_button(
                    df=df,
                    button_label=csv_label,
                    base_filename=base_filename,
                    key=f"{base_filename}_csv",
                    include_timestamp=include_timestamp
                )
            elif fmt == 'excel':
                create_excel_download_button(
                    df=df,
                    button_label=excel_label,
                    base_filename=base_filename,
                    sheet_name=sheet_name,
                    key=f"{base_filename}_excel",
                    include_timestamp=include_timestamp
                )
