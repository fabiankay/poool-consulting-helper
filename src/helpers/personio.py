import pandas as pd
import requests
import json
from datetime import datetime, timedelta

def get_access_token(client_id, client_secret):
    """Obtain access token from Personio API"""
    url = "https://api.personio.de/v2/auth/token"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in', 3600)  # Default to 1 hour
        
        # Calculate expiration time
        expires_at = datetime.now() + timedelta(seconds=expires_in - 60)  # Subtract 60s for safety
        
        return access_token, expires_at, None
    except requests.exceptions.RequestException as e:
        return None, None, f"API request failed: {str(e)}"
    except json.JSONDecodeError:
        return None, None, "Invalid JSON response from API"
    except Exception as e:
        return None, None, f"Unexpected error: {str(e)}"


def get_employees(access_token):
    """Retrieve employees from Personio API"""
    url = "https://api.personio.de/v1/company/employees"
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        employees_data = response.json()
        return employees_data, None
    except requests.exceptions.RequestException as e:
        return None, f"API request failed: {str(e)}"
    except json.JSONDecodeError:
        return None, "Invalid JSON response from API"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def process_employees_data(employees_data):
    """Convert employees data to pandas DataFrame with improved complex attribute handling"""
    try:
        if 'data' not in employees_data:
            return None, None, "No 'data' field found in API response"
                
        employees = employees_data['data']
        if not employees:
            return pd.DataFrame(), {}, None
                
        # Extract employee information and build column mapping
        processed_employees = []
        column_mapping = {}
                
        for employee in employees:
            emp_data = {}
                        
            # Basic employee info
            emp_data['ID (id)'] = employee.get('id')
            column_mapping['id'] = 'ID (id)'
                        
            # Extract attributes
            attributes = employee.get('attributes', {})
            for key, value in attributes.items():
                column_name, processed_value = process_attribute(key, value)
                column_mapping[key] = column_name
                emp_data[column_name] = processed_value
                        
            processed_employees.append(emp_data)
                
        df = pd.DataFrame(processed_employees)
        return df, column_mapping, None
        
    except Exception as e:
        return None, None, f"Error processing employee data: {str(e)}"


def process_attribute(key, value):
    """Process individual attribute with simplified handling"""
    
    # Simple values
    if not isinstance(value, dict):
        column_name = f"{key} ({key})"
        return column_name, value
    
    # Get column name from label or key
    label = value.get('label', key)
    column_name = f"{label} ({key})"
    
    # Extract the actual value
    actual_value = value.get('value', value)
    
    # Process based on value type
    if isinstance(actual_value, list):
        return column_name, process_list_value(actual_value)
    elif isinstance(actual_value, dict):
        return column_name, process_object_value(actual_value)
    else:
        return column_name, actual_value


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
