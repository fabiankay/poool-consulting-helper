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
    """Process individual attribute with improved handling for complex structures"""
    
    # Case 1: Simple value (string, number, boolean, None)
    if not isinstance(value, dict):
        column_name = f"{key} ({key})"
        return column_name, value
    
    # Case 2: Dictionary with label and value structure
    if 'label' in value:
        label = value.get('label', key)
        column_name = f"{label} ({key})"
        
        # Extract the actual value
        actual_value = value.get('value', {})
        
        # Handle nested value structures
        if isinstance(actual_value, dict):
            return column_name, process_nested_value(actual_value)
        elif isinstance(actual_value, list):
            return column_name, process_list_value(actual_value)
        else:
            return column_name, actual_value
    
    # Case 3: Direct nested object or list (no label wrapper)
    else:
        column_name = f"{key} ({key})"
        if isinstance(value, list):
            return column_name, process_list_value(value)
        else:
            return column_name, process_nested_value(value)


def process_list_value(value_list):
    """Process list values like cost_centers and absence_entitlements"""
    
    if not value_list or len(value_list) == 0:
        return "None"
    
    processed_items = []
    
    for item in value_list:
        if isinstance(item, dict):
            # Handle typed objects in lists
            obj_type = item.get('type')
            attributes = item.get('attributes', {})
            
            if obj_type == 'TimeOffType':
                # For absence entitlements
                name = attributes.get('name', 'Unknown')
                entitlement = attributes.get('entitlement', 0)
                category = attributes.get('category', '')
                processed_items.append(f"{name} ({entitlement})")
            
            elif obj_type == 'CostCenter':
                # For cost centers
                name = attributes.get('name') or attributes.get('code') or attributes.get('id')
                if name:
                    processed_items.append(str(name))
                else:
                    processed_items.append('Cost Center')
            
            elif obj_type == 'Department':
                # For department lists
                name = attributes.get('name') or attributes.get('code') or attributes.get('id')
                if name:
                    processed_items.append(str(name))
                else:
                    processed_items.append('Department')
            
            elif obj_type == 'Location':
                # For location lists
                name = attributes.get('name') or attributes.get('address') or attributes.get('code')
                if name:
                    processed_items.append(str(name))
                else:
                    processed_items.append('Location')
            
            elif attributes:
                # Generic handling for objects with attributes
                name = (attributes.get('name') or 
                       attributes.get('code') or 
                       attributes.get('id') or 
                       f"{obj_type or 'Item'}")
                processed_items.append(str(name))
            
            else:
                # Fallback for objects without clear structure
                processed_items.append(f"{obj_type or 'Item'}")
        
        else:
            # Handle simple values in lists
            processed_items.append(str(item))
    
    # Return as comma-separated string for DataFrame compatibility
    return "; ".join(processed_items)


def process_nested_value(value):
    """Process nested value objects based on their type"""
    
    if not isinstance(value, dict):
        return value
    
    # Handle typed objects
    obj_type = value.get('type')
    
    if obj_type == 'WorkSchedule':
        # For work schedules, extract relevant schedule information
        attributes = value.get('attributes', {})
        if attributes:
            # Try to get name first, fallback to other identifiers
            return (attributes.get('name') or 
                   attributes.get('code') or 
                   attributes.get('id') or 
                   'WorkSchedule Object')
        return 'WorkSchedule Object'
    
    elif obj_type == 'Employee':
        # For employee references (like supervisors), get preferred name or fallback
        attributes = value.get('attributes', {})
        if attributes:
            # Handle nested attribute structure where each field has label/value
            def extract_nested_value(attr_dict):
                if isinstance(attr_dict, dict) and 'value' in attr_dict:
                    return attr_dict['value']
                return attr_dict
            
            # Extract values from nested structure
            preferred_name = extract_nested_value(attributes.get('preferred_name'))
            first_name = extract_nested_value(attributes.get('first_name', ''))
            last_name = extract_nested_value(attributes.get('last_name', ''))
            display_name = extract_nested_value(attributes.get('display_name'))
            full_name = extract_nested_value(attributes.get('full_name'))
            name = extract_nested_value(attributes.get('name'))
            employee_number = extract_nested_value(attributes.get('employee_number'))
            emp_id = extract_nested_value(attributes.get('id'))
            
            # Build full name from first/last if available
            if first_name and last_name:
                first_name = str(first_name).strip()
                last_name = str(last_name).strip()
                full_name_concat = f"{first_name} {last_name}".strip()
            else:
                full_name_concat = None
            
            return (preferred_name or 
                   full_name_concat or
                   display_name or
                   full_name or
                   name or 
                   (str(employee_number) if employee_number else None) or
                   (str(emp_id) if emp_id else None) or 
                   'Employee Reference')
        return 'Employee Reference'
    
    elif obj_type == 'Department':
        # For departments, get name or code
        attributes = value.get('attributes', {})
        if attributes:
            return (attributes.get('name') or 
                   attributes.get('code') or 
                   attributes.get('id') or 
                   'Department Object')
        return 'Department Object'
    
    elif obj_type == 'Location':
        # For locations, get name or address
        attributes = value.get('attributes', {})
        if attributes:
            return (attributes.get('name') or 
                   attributes.get('address') or 
                   attributes.get('code') or 
                   'Location Object')
        return 'Location Object'
    
    # Handle objects with attributes but no type
    elif 'attributes' in value:
        attributes = value.get('attributes', {})
        # Try common name fields (this covers supervisor cases without explicit type)
        first_name = str(attributes.get('first_name', '')).strip()
        last_name = str(attributes.get('last_name', '')).strip()
        full_name_concat = f"{first_name} {last_name}".strip()
        
        name_result = (attributes.get('preferred_name') or 
                      (full_name_concat if full_name_concat else None) or
                      attributes.get('display_name') or 
                      attributes.get('full_name') or
                      attributes.get('name') or 
                      str(attributes.get('employee_number', '')) or
                      str(attributes.get('code', '')) or 
                      str(attributes.get('id', '')))
        
        return name_result or 'Complex Object'
    
    # Handle objects with 'value' field that contains simple data
    elif 'value' in value and not isinstance(value.get('value'), (dict, list)):
        # This handles cases like supervisor returning a name object
        return value.get('value')
    
    # Handle direct value objects with complex nested structures
    elif 'value' in value:
        nested_value = value.get('value')
        if isinstance(nested_value, dict):
            return process_nested_value(nested_value)
        elif isinstance(nested_value, list):
            return process_list_value(nested_value)
        return nested_value
    
    # Handle objects with name field directly
    elif 'name' in value:
        return value.get('name')
    
    # Fallback: convert complex object to string representation
    else:
        # For debugging, you might want to see the structure
        if len(str(value)) < 100:  # Only for reasonably small objects
            return str(value)
        else:
            return f"Complex Object ({obj_type or 'Unknown Type'})"
