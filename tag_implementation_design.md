# 🏷️ Poool CRM Tag Implementation Design

## 🎯 Implementation Overview

Based on the comprehensive tag API discovery, we have full CRUD capabilities. This allows us to implement complete tag automation with name-based mapping and auto-creation.

## 📊 Tag API Structure (Confirmed)

```json
{
  "title": "VIP Client",           // Tag name/label
  "color": "#FF5733",              // Display color
  "color_background": "#FFF",      // Background color
  "is_active": true,               // Active status
  "available_company": true,       // Company support ✅
  "available_person": true,        // Person support ✅
  "pos": 10                       // Sort order
}
```

**Assignment Structure in Companies/Persons:**
```json
{
  "name": "Acme Corp",
  "tags": [
    {"id": 12},
    {"id": 25}
  ]
}
```

## 🎨 CSV Mapping Strategies

### **Primary Strategy: Comma-Separated**
**Most user-friendly and flexible**

```csv
Company Name,Tags,Is Client
Acme Corp,"VIP, Enterprise, Marketing",true
Tech Solutions,"Supplier, IT Services",false
Global Manufacturing,"Client, Large Enterprise",true
```

**Benefits:**
- ✅ Intuitive for users
- ✅ Unlimited tags per entity
- ✅ Handles spaces and special characters
- ✅ Common CSV pattern

**Parsing Logic:**
```python
def parse_comma_separated_tags(tag_string: str) -> List[str]:
    if not tag_string or pd.isna(tag_string):
        return []

    # Split by comma and clean
    tags = [tag.strip().strip('"') for tag in str(tag_string).split(',')]
    return [tag for tag in tags if tag]  # Remove empty strings
```

### **Secondary Strategy: Multiple Tag Columns**
**For users who prefer structured columns**

```csv
Company Name,Tag1,Tag2,Tag3,Is Client
Acme Corp,VIP,Enterprise,Marketing,true
Tech Solutions,Supplier,IT Services,,false
```

**Detection Pattern:**
- Columns named: `Tag1`, `Tag2`, `Tag_Primary`, `Secondary_Tag`, etc.
- Auto-detect columns matching `tag*`, `*tag*` patterns

### **Tertiary Strategy: One-Hot Encoding**
**For advanced users with known tag sets**

```csv
Company Name,Tag_VIP,Tag_Enterprise,Tag_Supplier,Is Client
Acme Corp,1,1,0,true
Tech Solutions,0,0,1,false
```

**Detection Logic:**
- Columns starting with `Tag_`, `tag_`
- Boolean/numeric values (1/0, true/false, yes/no)

## 🔧 Implementation Architecture

### **1. Tag Management Functions**

```python
# Core tag operations
def get_all_tags(api_key: str, environment: str) -> Dict[str, int]:
    """Returns {tag_name: tag_id} mapping"""

def create_tag_if_missing(api_key: str, tag_name: str, environment: str) -> int:
    """Creates tag and returns ID, or returns existing ID"""

def get_tag_id_by_name(tag_name: str, tag_cache: Dict[str, int]) -> Optional[int]:
    """Case-insensitive tag name lookup"""

def parse_csv_tags(tag_input: str, format_type: str) -> List[str]:
    """Parse tags from CSV based on detected format"""
```

### **2. Tag Detection & Mapping**

```python
def detect_tag_columns(df: pd.DataFrame) -> Dict[str, str]:
    """Auto-detect tag columns and their format"""

    tag_mappings = {}

    # Strategy 1: Comma-separated detection
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['tag', 'label', 'category']):
            sample = df[col].dropna().head(3)
            if any(',' in str(val) for val in sample):
                tag_mappings[col] = 'comma_separated'

    # Strategy 2: Multiple tag columns
    tag_pattern_cols = [col for col in df.columns
                       if re.match(r'tag\w*\d*|secondary.*tag|primary.*tag', col.lower())]
    for col in tag_pattern_cols:
        tag_mappings[col] = 'single_tag'

    # Strategy 3: One-hot encoding
    one_hot_cols = [col for col in df.columns
                   if col.lower().startswith(('tag_', 'label_'))]
    for col in one_hot_cols:
        if df[col].dtype in ['bool', 'int64'] or df[col].isin([0, 1, True, False]).all():
            tag_mappings[col] = 'one_hot'

    return tag_mappings
```

### **3. Tag Processing Pipeline**

```python
def process_entity_tags(row_data: pd.Series, tag_mappings: Dict, tag_cache: Dict[str, int],
                       api_key: str, environment: str) -> List[int]:
    """Process all tag assignments for a single entity"""

    all_tags = set()

    for column, format_type in tag_mappings.items():
        if column not in row_data or pd.isna(row_data[column]):
            continue

        if format_type == 'comma_separated':
            tags = parse_comma_separated_tags(row_data[column])
            all_tags.update(tags)

        elif format_type == 'single_tag':
            tag = str(row_data[column]).strip()
            if tag:
                all_tags.add(tag)

        elif format_type == 'one_hot':
            if row_data[column] in [1, True, 'true', 'yes', '1']:
                # Extract tag name from column (remove 'tag_' prefix)
                tag_name = column.lower().replace('tag_', '').replace('_', ' ').title()
                all_tags.add(tag_name)

    # Convert tag names to IDs
    tag_ids = []
    for tag_name in all_tags:
        if tag_name in tag_cache:
            tag_ids.append(tag_cache[tag_name])
        else:
            # Create new tag
            tag_id = create_tag_if_missing(api_key, tag_name, environment)
            tag_cache[tag_name] = tag_id  # Update cache
            tag_ids.append(tag_id)

    return tag_ids
```

## 🎨 UI Integration Plan

### **Tab Organization**
Add tags to **Basic Info tab** to keep interface simple:

```
📋 Basic Info Tab
├── Company Information (name, address, etc.)
├── 🏷️ Tag Management
│   ├── Auto-detected tag columns
│   ├── Tag format preview
│   └── Create missing tags option
└── Contact Information (phone, email, etc.)
```

### **Tag Mapping Interface**

```python
def show_tag_mapping_section():
    st.subheader("🏷️ Tag Assignment")

    # Auto-detection results
    if 'detected_tag_columns' in st.session_state:
        tag_mappings = st.session_state.detected_tag_columns

        if tag_mappings:
            st.success(f"✅ Auto-detected {len(tag_mappings)} tag columns")

            for col, format_type in tag_mappings.items():
                with st.expander(f"📋 {col} ({format_type.replace('_', ' ').title()})"):

                    # Show sample data
                    sample_data = st.session_state.uploaded_data[col].dropna().head(3)
                    st.code(f"Sample: {list(sample_data)}")

                    # Format-specific options
                    if format_type == 'comma_separated':
                        st.info("💡 Comma-separated tags will be split automatically")

                    elif format_type == 'one_hot':
                        tag_name = st.text_input(
                            f"Tag name for {col}:",
                            value=col.replace('tag_', '').replace('_', ' ').title(),
                            key=f"tag_name_{col}"
                        )

            # Tag creation options
            st.subheader("🆕 Tag Creation Settings")
            auto_create = st.checkbox(
                "Automatically create missing tags",
                value=True,
                help="Create new tags when they don't exist in the system"
            )

            if auto_create:
                default_color = st.color_picker("Default color for new tags", "#007BFF")

        else:
            st.warning("⚠️ No tag columns detected. You can manually map columns below.")

    # Manual mapping option
    with st.expander("🔧 Manual Tag Column Mapping"):
        available_columns = [col for col in st.session_state.uploaded_data.columns
                           if col not in ['id', 'name']]

        manual_tag_column = st.selectbox(
            "Select column containing tags:",
            [''] + available_columns
        )

        if manual_tag_column:
            format_type = st.radio(
                "Tag format:",
                ['comma_separated', 'single_tag'],
                format_func=lambda x: x.replace('_', ' ').title()
            )
```

### **Tag Preview Section**

```python
def show_tag_preview():
    """Show preview of tag assignments"""

    if 'tag_preview_data' in st.session_state:
        preview_data = st.session_state.tag_preview_data

        st.subheader("🔍 Tag Assignment Preview")

        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            total_entities = len(preview_data)
            st.metric("Entities with Tags", total_entities)
        with col2:
            total_tags = len(set().union(*[item['tags'] for item in preview_data]))
            st.metric("Unique Tags", total_tags)
        with col3:
            new_tags = len([tag for item in preview_data for tag in item['new_tags']])
            st.metric("New Tags to Create", new_tags)

        # Detailed preview
        with st.expander("📋 Detailed Tag Assignments", expanded=True):
            preview_df = pd.DataFrame([
                {
                    'Entity': item['name'],
                    'Tags': ', '.join(item['tags']),
                    'New Tags': ', '.join(item['new_tags']) or 'None'
                }
                for item in preview_data[:10]  # Show first 10
            ])

            st.dataframe(preview_df, use_container_width=True)

            if len(preview_data) > 10:
                st.caption(f"Showing first 10 of {len(preview_data)} entities")
```

## 🔄 Integration with Existing System

### **1. Add to Field Definitions**

```python
def get_optional_company_fields():
    return [
        # ... existing fields ...
        "tags",  # Add tag support
    ]

def get_optional_person_fields():
    return [
        # ... existing fields ...
        "tags",  # Add tag support
    ]
```

### **2. Update Data Preparation**

```python
def prepare_company_data(row: pd.Series, field_mapping: Dict, tag_mappings: Dict,
                        tag_cache: Dict, api_key: str, environment: str) -> Dict:
    """Enhanced with tag processing"""

    # ... existing field processing ...

    # Process tags
    if tag_mappings:
        tag_ids = process_entity_tags(row, tag_mappings, tag_cache, api_key, environment)
        if tag_ids:
            data['tags'] = [{'id': tag_id} for tag_id in tag_ids]

    return data
```

### **3. Auto-mapping Patterns**

```python
# Add to existing auto-mapping dictionary
AUTO_MAPPING_PATTERNS = {
    # ... existing patterns ...

    # Tag patterns
    'tags': ['tags', 'tag', 'labels', 'label', 'categories', 'category'],
    'tag_column_1': ['tag1', 'tag_1', 'primary_tag', 'main_tag'],
    'tag_column_2': ['tag2', 'tag_2', 'secondary_tag', 'additional_tag'],
}
```

## 🎯 Implementation Phases

### **Phase 1: Core Tag API Functions** ✅ Next
1. Implement tag listing and caching
2. Implement tag creation with validation
3. Add tag name-to-ID mapping
4. Test with real API

### **Phase 2: CSV Detection & Parsing**
1. Auto-detect tag columns and formats
2. Implement parsing for all three strategies
3. Add validation and error handling
4. Create comprehensive test cases

### **Phase 3: UI Integration**
1. Add tag section to Basic Info tab
2. Implement auto-detection display
3. Add manual mapping options
4. Create tag assignment preview

### **Phase 4: Data Pipeline Integration**
1. Update company/person data preparation
2. Integrate tag processing in bulk imports
3. Add progress tracking for tag operations
4. Implement error handling and rollback

## 📋 Success Criteria

✅ **Auto-detect 90%+ of common tag column formats**
✅ **Support unlimited tags per entity**
✅ **Create missing tags automatically with user consent**
✅ **Provide clear preview of tag assignments**
✅ **Handle edge cases gracefully (special characters, duplicates)**
✅ **Maintain performance for large imports (1000+ entities)**

---

This comprehensive design leverages the full API capabilities for seamless tag management!