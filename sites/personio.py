import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="Personio API Query Tool",
    page_icon="🧑‍💻",
    layout="wide"
)

st.title("👥 Personio API Query Tool")
st.markdown("Enter your Personio API credentials to authenticate and retrieve employee data.")

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'token_expires_at' not in st.session_state:
    st.session_state.token_expires_at = None
if 'column_mapping' not in st.session_state:
    st.session_state.column_mapping = {}
if 'employees_df' not in st.session_state:
    st.session_state.employees_df = None

def is_token_valid():
    """Check if the current token is still valid"""
    if not st.session_state.access_token or not st.session_state.token_expires_at:
        return False
    return datetime.now() < st.session_state.token_expires_at

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
    """Convert employees data to pandas DataFrame"""
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
                if isinstance(value, dict):
                    # Get label and create column name
                    label = value.get('label', key)
                    column_name = f"{label} ({key})"
                    column_mapping[key] = column_name
                    
                    # Get the actual value
                    if 'value' in value:
                        emp_data[column_name] = value['value']
                    else:
                        emp_data[column_name] = value
                else:
                    # Fallback for simple values
                    column_name = f"{key} ({key})"
                    column_mapping[key] = column_name
                    emp_data[column_name] = value
            
            processed_employees.append(emp_data)
        
        df = pd.DataFrame(processed_employees)
        return df, column_mapping, None
    except Exception as e:
        return None, None, f"Error processing employee data: {str(e)}"

def create_excel_download(df):
    """Create Excel file in memory for download"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Employees')
    output.seek(0)
    return output.getvalue()

# Main app layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔑 API Credentials")
    
    # Input fields for credentials
    client_id = st.text_input(
        "Client ID",
        type="default",
        help="Your Personio API Client ID"
    )
    
    client_secret = st.text_input(
        "Client Secret",
        type="password",
        help="Your Personio API Client Secret"
    )
    
    # Authentication button
    if st.button("🔓 Authenticate", type="primary"):
        if not client_id or not client_secret:
            st.error("Please enter both Client ID and Client Secret")
        else:
            with st.spinner("Authenticating..."):
                token, expires_at, error = get_access_token(client_id, client_secret)
                
                if error:
                    st.error(f"Authentication failed: {error}")
                else:
                    st.session_state.access_token = token
                    st.session_state.token_expires_at = expires_at
                    st.success("✅ Authentication successful!")
                    st.rerun()
    
    # Token status
    if st.session_state.access_token:
        if is_token_valid():
            st.success("🟢 Token is valid")
            time_left = st.session_state.token_expires_at - datetime.now()
            minutes_left = int(time_left.total_seconds() / 60)
            st.info(f"Token expires in {minutes_left} minutes")
        else:
            st.error("🔴 Token has expired")
            st.session_state.access_token = None
            st.session_state.token_expires_at = None

with col2:
    st.subheader("👥 Employee Data")
    
    if st.session_state.access_token and is_token_valid():
        if st.button("📥 Fetch Employees", type="secondary"):
            with st.spinner("Fetching employee data..."):
                employees_data, error = get_employees(st.session_state.access_token)
                
                if error:
                    st.error(f"Failed to fetch employees: {error}")
                else:
                    df, column_mapping, process_error = process_employees_data(employees_data)
                    
                    if process_error:
                        st.error(f"Failed to process employee data: {process_error}")
                    else:
                        st.session_state.employees_df = df
                        st.session_state.column_mapping = column_mapping
                        st.success(f"✅ Successfully fetched {len(df)} employees!")
                        st.rerun()
    else:
        st.info("Please authenticate first to fetch employee data")

# Display employee data
if st.session_state.employees_df is not None:
    st.subheader("📊 Employee DataFrame")
    
    # Display basic info about the dataset
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Employees", len(st.session_state.employees_df))
    with col2:
        st.metric("Total Columns", len(st.session_state.employees_df.columns))
    with col3:
        st.metric("Data Size", f"{st.session_state.employees_df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # Display the DataFrame
    st.dataframe(
        st.session_state.employees_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Download options
    st.subheader("💾 Download Options")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = st.session_state.employees_df.to_csv(index=False)
        st.download_button(
            label="📄 Download as CSV",
            data=csv,
            file_name=f"personio_employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_data = create_excel_download(st.session_state.employees_df)
        st.download_button(
            label="📊 Download as Excel",
            data=excel_data,
            file_name=f"personio_employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Data preview options
    with st.expander("🔍 Data Preview Options"):
        if st.checkbox("Show column information"):
            st.write("**Column Names and Data Types:**")
            col_info = pd.DataFrame({
                'Column': st.session_state.employees_df.columns,
                'Data Type': st.session_state.employees_df.dtypes.values,
                'Non-Null Count': st.session_state.employees_df.count().values,
                'Null Count': st.session_state.employees_df.isnull().sum().values
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)
        
        if st.checkbox("Show sample data"):
            sample_size = st.slider("Number of sample rows", 1, min(20, len(st.session_state.employees_df)), 5)
            st.write(f"**Sample of {sample_size} rows:**")
            st.dataframe(st.session_state.employees_df.head(sample_size), use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Keep your API credentials secure and don't share them with others.")