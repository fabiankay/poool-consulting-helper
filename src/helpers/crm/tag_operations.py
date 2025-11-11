"""
Tag-related operations for CRM system.

Handles tag detection, processing, ID lookup, and tag assignment.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
import re
from ..poool_api_client import PooolAPIClient


def parse_comma_separated_tags(tag_string: str) -> List[str]:
    """Parse comma-separated tag string into list of tag names."""
    if not tag_string or pd.isna(tag_string):
        return []

    tags = [tag.strip().strip('"').strip("'") for tag in str(tag_string).split(',')]
    return [tag for tag in tags if tag]


def get_tag_ids_for_names(client: PooolAPIClient, tag_names: List[str], tag_cache: Dict[str, int], auto_create: bool = True) -> Tuple[List[int], List[str], Optional[str]]:
    """Convert list of tag names to tag IDs, optionally creating missing tags."""
    tag_ids = []
    created_tags = []

    for tag_name in tag_names:
        tag_name_clean = tag_name.strip()
        if not tag_name_clean:
            continue

        # Check cache first (case-insensitive)
        tag_id = None
        for cached_name, cached_id in tag_cache.items():
            if cached_name.lower() == tag_name_clean.lower():
                tag_id = cached_id
                break

        if tag_id:
            tag_ids.append(tag_id)
        elif auto_create:
            # Create missing tag
            new_tag_id, error = client.create_tag_if_missing(tag_name_clean)
            if error:
                return [], [], f"Fehler beim Erstellen des Tags '{tag_name_clean}': {error}"

            if new_tag_id:
                tag_ids.append(new_tag_id)
                tag_cache[tag_name_clean] = new_tag_id
                tag_cache[tag_name_clean.lower()] = new_tag_id
                created_tags.append(tag_name_clean)
        else:
            continue

    return tag_ids, created_tags, None


def detect_tag_columns(df: pd.DataFrame) -> Dict[str, str]:
    """Auto-detect tag columns in DataFrame and determine their format."""
    tag_mappings = {}

    # Strategy 1: One-hot encoding (check first for specific patterns)
    one_hot_cols = [col for col in df.columns
                   if col.lower().startswith(('tag_', 'label_', 'category_')) and '_' in col.lower()]
    for col in one_hot_cols:
        sample = df[col].dropna()
        if len(sample) > 0:
            unique_vals = set(sample.astype(str).str.lower())
            boolean_vals = {'0', '1', 'true', 'false', 'yes', 'no', '0.0', '1.0'}
            if unique_vals.issubset(boolean_vals):
                tag_mappings[col] = 'one_hot'

    # Strategy 2: Comma-separated detection
    for col in df.columns:
        if col not in tag_mappings and any(keyword in col.lower() for keyword in ['tag', 'label', 'category']):
            sample = df[col].dropna().head(10)
            if len(sample) > 0 and any(',' in str(val) for val in sample):
                tag_mappings[col] = 'comma_separated'
                continue
            elif len(sample) > 0:
                tag_mappings[col] = 'single_tag'
                continue

    # Strategy 3: Multiple tag columns
    tag_pattern_cols = [col for col in df.columns
                       if re.match(r'tag\w*\d*|secondary.*tag|primary.*tag|main.*tag', col.lower())]
    for col in tag_pattern_cols:
        if col not in tag_mappings:
            tag_mappings[col] = 'single_tag'

    return tag_mappings


def process_entity_tags(client: PooolAPIClient, row_data: pd.Series, tag_mappings: Dict[str, str], tag_cache: Dict[str, int], auto_create: bool = True) -> Tuple[List[int], List[str], Optional[str]]:
    """Process all tag assignments for a single entity."""
    all_tag_names = set()

    # Process each mapped column
    for column, format_type in tag_mappings.items():
        if column not in row_data or pd.isna(row_data[column]):
            continue

        if format_type == 'comma_separated':
            tags = parse_comma_separated_tags(row_data[column])
            all_tag_names.update(tags)
        elif format_type == 'single_tag':
            tag = str(row_data[column]).strip()
            if tag and tag.lower() not in ['nan', 'none', '']:
                all_tag_names.add(tag)
        elif format_type == 'one_hot':
            value = str(row_data[column]).lower()
            if value in ['1', 'true', 'yes', '1.0']:
                tag_name = column.lower()
                for prefix in ['tag_', 'label_', 'category_']:
                    if tag_name.startswith(prefix):
                        tag_name = tag_name[len(prefix):]
                        break
                tag_name = tag_name.replace('_', ' ').title()
                all_tag_names.add(tag_name)

    # Convert tag names to IDs
    if all_tag_names:
        return get_tag_ids_for_names(client, list(all_tag_names), tag_cache, auto_create)
    else:
        return [], [], None
