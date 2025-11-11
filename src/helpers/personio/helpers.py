"""
Personio helper functions using the PersonioAPIClient class.

Provides functions for fetching and processing employee, absence, and attendance data
from the Personio HR API.
"""

import pandas as pd
from .api_client import PersonioAPIClient


def create_personio_client(client_id: str, client_secret: str) -> PersonioAPIClient:
    """
    Create and authenticate a Personio API client.

    Args:
        client_id: Personio API Client ID
        client_secret: Personio API Client Secret

    Returns:
        Authenticated PersonioAPIClient instance, or None if authentication fails
    """
    client = PersonioAPIClient(client_id, client_secret)
    _, _, error = client.authenticate()

    if error:
        return None

    return client


def get_employees(client: PersonioAPIClient):
    """
    Retrieve all employees from Personio API with automatic pagination.

    Args:
        client: Authenticated PersonioAPIClient instance

    Returns:
        Tuple of (employees_data, error)
    """
    return client.get_employees()


def get_absences(client: PersonioAPIClient, start_date=None, end_date=None):
    """
    Retrieve all absences from Personio API with automatic pagination.

    Args:
        client: Authenticated PersonioAPIClient instance
        start_date: Optional start date (YYYY-MM-DD format)
        end_date: Optional end date (YYYY-MM-DD format)

    Returns:
        Tuple of (absences_data, error)
    """
    return client.get_absences(start_date, end_date)


def get_attendances(client: PersonioAPIClient, start_date=None, end_date=None):
    """
    Retrieve all attendances from Personio API with automatic pagination.

    Args:
        client: Authenticated PersonioAPIClient instance
        start_date: Optional start date (YYYY-MM-DD format)
        end_date: Optional end date (YYYY-MM-DD format)

    Returns:
        Tuple of (attendances_data, error)
    """
    return client.get_attendances(start_date, end_date)


def process_employees_data(employees_data):
    """Convert employees data to pandas DataFrame with improved complex attribute handling"""
    try:
        if 'data' not in employees_data:
            return None, None, "Kein 'data'-Feld in API-Antwort gefunden"

        employees = employees_data['data']
        if not employees:
            return pd.DataFrame(), {}, None

        # Extract employee information and build column mapping
        processed_employees = []
        column_mapping = {}

        for employee in employees:
            emp_data = {}

            # Extract attributes
            attributes = employee.get('attributes', {})
            for key, value in attributes.items():
                column_name, processed_value, json_path = process_attribute(key, value)
                column_mapping[json_path] = column_name
                emp_data[column_name] = processed_value

            processed_employees.append(emp_data)

        df = pd.DataFrame(processed_employees)
        return df, column_mapping, None

    except Exception as e:
        return None, None, f"Fehler beim Verarbeiten der Mitarbeiterdaten: {str(e)}"


def process_absences_data(absences_data):
    """Convert absences data to pandas DataFrame with column mapping

    Args:
        absences_data: Raw JSON response from absences API

    Returns:
        Tuple of (df, column_mapping, error)
    """
    try:
        if 'data' not in absences_data:
            return None, None, "Kein 'data'-Feld in API-Antwort gefunden"

        absences = absences_data['data']
        if not absences:
            return pd.DataFrame(), {}, None

        # Extract absence information and build column mapping
        processed_absences = []
        column_mapping = {}

        for absence in absences:
            absence_record = {}

            # Extract attributes
            attributes = absence.get('attributes', {})
            for key, value in attributes.items():
                column_name, processed_value, json_path = process_attribute(key, value)
                column_mapping[json_path] = column_name
                absence_record[column_name] = processed_value

            processed_absences.append(absence_record)

        df = pd.DataFrame(processed_absences)
        return df, column_mapping, None

    except Exception as e:
        return None, None, f"Fehler beim Verarbeiten der Abwesenheitsdaten: {str(e)}"


def process_attendances_data(attendances_data):
    """Convert attendances data to pandas DataFrame with column mapping

    Args:
        attendances_data: Raw JSON response from attendances API

    Returns:
        Tuple of (df, column_mapping, error)
    """
    try:
        if 'data' not in attendances_data:
            return None, None, "Kein 'data'-Feld in API-Antwort gefunden"

        attendances = attendances_data['data']
        if not attendances:
            return pd.DataFrame(), {}, None

        # Extract attendance information and build column mapping
        processed_attendances = []
        column_mapping = {}

        for attendance in attendances:
            attendance_record = {}

            # Extract attributes
            attributes = attendance.get('attributes', {})
            for key, value in attributes.items():
                column_name, processed_value, json_path = process_attribute(key, value)
                column_mapping[json_path] = column_name
                attendance_record[column_name] = processed_value

            processed_attendances.append(attendance_record)

        df = pd.DataFrame(processed_attendances)
        return df, column_mapping, None

    except Exception as e:
        return None, None, f"Fehler beim Verarbeiten der Anwesenheitsdaten: {str(e)}"


def process_attribute(key, value, path_prefix=""):
    """Process individual attribute with JSON path tracking"""

    # Build current path
    current_path = f"{path_prefix}.{key}" if path_prefix else key

    # Simple values
    if not isinstance(value, dict):
        column_name = f"{key} ({current_path})"
        return column_name, value, current_path

    # Get column name from label or key
    label = value.get('label', key)

    # Extract the actual value
    actual_value = value.get('value', value)

    # Build path based on structure
    if 'value' in value:
        # Has a value field, add it to path
        value_path = f"{current_path}.value"
    else:
        value_path = current_path

    column_name = f"{label} ({value_path})"

    # Process based on value type
    if isinstance(actual_value, list):
        return column_name, process_list_value(actual_value), value_path
    elif isinstance(actual_value, dict):
        # Check if it has type and attributes (nested object)
        if 'attributes' in actual_value:
            nested_path = f"{value_path}.attributes"
            return column_name, process_object_value(actual_value), nested_path
        else:
            return column_name, process_object_value(actual_value), value_path
    else:
        return column_name, actual_value, value_path


def process_list_value(value_list):
    """Process list values like cost_centers and absence_entitlements"""
    
    if not value_list:
        return "None"
    
    processed_items = []
    
    for item in value_list:
        if isinstance(item, dict):
            obj_type = item.get('type')
            attributes = item.get('attributes', {})
            
            if obj_type == 'TimeOffType':
                name = attributes.get('name', 'Unknown')
                entitlement = attributes.get('entitlement', 0)
                processed_items.append(f"{name} ({entitlement})")
            else:
                # Generic object handling
                name = extract_name_from_attributes(attributes) or f"{obj_type or 'Item'}"
                processed_items.append(str(name))
        else:
            processed_items.append(str(item))
    
    return "; ".join(processed_items)


def process_object_value(value):
    """Process object values with unified approach"""
    
    if not isinstance(value, dict):
        return value
    
    obj_type = value.get('type')
    attributes = value.get('attributes', {})
    
    # Handle different object types
    if obj_type in ['Employee', 'Department', 'Location', 'WorkSchedule', 'CostCenter']:
        name = extract_name_from_attributes(attributes)
        if name:
            return name
        return f"{obj_type} Object"
    
    # Handle objects with direct value field
    if 'value' in value:
        nested_value = value['value']
        if isinstance(nested_value, (dict, list)):
            if isinstance(nested_value, list):
                return process_list_value(nested_value)
            else:
                return process_object_value(nested_value)
        return nested_value
    
    # Handle objects with attributes but no type
    if attributes:
        name = extract_name_from_attributes(attributes)
        if name:
            return name
    
    # Handle objects with direct name field
    if 'name' in value:
        return value['name']
    
    # Fallback
    return f"Complex Object ({obj_type or 'Unknown'})"


def extract_name_from_attributes(attributes):
    """Extract name from attributes with consistent nested value handling"""
    
    if not attributes:
        return None
    
    def get_value(attr):
        """Extract value from potentially nested attribute structure"""
        if isinstance(attr, dict) and 'value' in attr:
            return attr['value']
        return attr
    
    # Try different name fields in order of preference
    name_fields = [
        'preferred_name', 'display_name', 'full_name', 'name',
        'first_name', 'last_name', 'code', 'address', 'employee_number', 'id'
    ]
    
    extracted_values = {}
    for field in name_fields:
        if field in attributes:
            extracted_values[field] = get_value(attributes[field])
    
    # Build name with preference order
    if extracted_values.get('preferred_name'):
        return str(extracted_values['preferred_name'])
    
    # Try to build full name from first + last
    first_name = extracted_values.get('first_name')
    last_name = extracted_values.get('last_name')
    if first_name and last_name:
        return f"{str(first_name).strip()} {str(last_name).strip()}".strip()
    
    # Try other name fields
    for field in ['display_name', 'full_name', 'name', 'code', 'address']:
        if extracted_values.get(field):
            return str(extracted_values[field])
    
    # Last resort: employee_number or id
    for field in ['employee_number', 'id']:
        if extracted_values.get(field):
            return str(extracted_values[field])
    
    return None
