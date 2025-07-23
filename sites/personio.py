import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import io

from src.helpers.personio import get_access_token, get_employees, process_employees_data

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
                        # st.success(f"✅ Successfully fetched {len(df)} employees!")
                        st.rerun()

        if st.session_state.employees_df is not None:
            # Show a summary of the employee data and column mapping - column name, mapping, not null or empty count, null or empty count and data types
            with st.expander("📋 Column Mapping", expanded=False):
                st.write("This table shows the mapping of API fields to DataFrame columns:")
                mapping_df = pd.DataFrame.from_dict(
                    st.session_state.column_mapping, 
                    orient='index', 
                    columns=['DataFrame Column']
                ).reset_index().rename(columns={'index': 'API Field'})
                
                # Count not null and not empty values per column
                not_null_not_empty = st.session_state.employees_df.apply(
                    lambda col: col.notnull() & (col.astype(str).str.strip() != ''), axis=0
                ).sum().values
                # Count null or empty values per column
                null_or_empty = st.session_state.employees_df.apply(
                    lambda col: col.isnull() | (col.astype(str).str.strip() == ''), axis=0
                ).sum().values

                mapping_df['Not Null & Not Empty Count'] = not_null_not_empty
                mapping_df['Null or Empty Count'] = null_or_empty
                st.dataframe(mapping_df, use_container_width=True, hide_index=True)


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
        st.metric("Total Attributes", len(st.session_state.employees_df.columns))
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

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Keep API credentials secure and don't share them with others.")