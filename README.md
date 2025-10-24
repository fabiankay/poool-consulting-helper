# Poool Consulting Helper

Streamlit-based internal tools for CRM data management and HR integrations.

## Features

### 📥 CRM Import
Bulk import companies and persons to Poool CRM via API
- CSV/Excel file upload with flexible column mapping
- Smart field auto-detection
- Tag management and organization
- JSON-based mapping configuration (export/import for reuse)
- Duplicate detection
- Multi-environment support (production/staging/sandbox)

### 🔄 CRM Update
Bulk update existing companies in Poool CRM
- Match records by ID, name, or customer number
- Update core, client, and supplier fields
- Preview matches before updating
- Dry run mode for safe testing
- Multi-endpoint support (companies/clients/suppliers)

### 👤 Person Update
Bulk update existing persons in Poool CRM
- Match records by ID, email, or name
- Update contact information and personal details
- Preview and dry run support
- Batch processing with error reporting

### 🧑‍💻 Personio Integration
Access HR data from Personio API
- Fetch employees, absences, and attendances
- Optional date range filtering
- Export to CSV/Excel
- Automatic pagination handling
- OAuth2 authentication with token management

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run app.py
   ```

3. **Access the tools:**
   - Navigate to `http://localhost:8501`
   - Choose your tool from the sidebar
   - Configure API credentials and environment

## Architecture

```
poool-consulting-helper/
├── app.py                          # Main application entry point
├── sites/                          # UI pages
│   ├── home.py                     # Dashboard and navigation
│   ├── crm.py                      # CRM import tool
│   ├── crm_update.py              # CRM company update tool
│   ├── person_update.py           # CRM person update tool
│   └── personio.py                # Personio integration
├── src/
│   ├── components/                 # Reusable UI components
│   │   ├── crm_ui.py              # Shared CRM UI components
│   │   ├── session_state.py       # Global state management
│   │   └── sidebar.py             # App sidebar
│   └── helpers/                    # Business logic and API clients
│       ├── crm.py                 # CRM operations
│       ├── poool_api_client.py    # Poool API client
│       ├── personio.py            # Personio helpers
│       ├── personio_api_client.py # Personio API client
│       └── mapping_utils.py       # Mapping utilities
└── .streamlit/
    └── config.toml                # Streamlit configuration
```

## Common Workflows

### CRM Import
1. Select environment and test API connection
2. Upload CSV/Excel file with company or person data
3. Map CSV columns to API fields (or import saved mapping)
4. Configure tags and relationship flags (client/supplier)
5. Review preview and execute import
6. Download mapping as JSON for reuse

### CRM Update
1. Select environment and verify API connection
2. Upload CSV/Excel with data to update
3. Choose identifier field (ID, name, customer_number)
4. Map fields to update
5. Preview matches to verify
6. Run in dry run mode first (optional)
7. Execute actual update

### Personio Data Export
1. Enter Personio API credentials (Client ID/Secret)
2. Authenticate to get access token
3. Switch to desired tab (Employees/Absences/Attendances)
4. Optionally set date range filters
5. Fetch data
6. Download as CSV or Excel

## API Configuration

### Poool CRM Environments
- **Production**: `app.poool.cc` - Live data (use with caution)
- **Staging**: `staging-app.poool.rocks` - Safe testing environment
- **Custom**: Your sandbox URL

API credentials and environment selection persist across all CRM pages.

### Personio API
- Uses OAuth2 client credentials flow
- Requires Client ID and Client Secret
- Token automatically managed with expiration tracking
- Supports v1 API endpoints for employees, time-offs, and attendances

## Best Practices

- ✅ Start with **staging** or **dry run mode** before production updates
- ✅ Use **preview matches** to verify which records will be affected
- ✅ Download and save **mapping JSONs** for recurring imports
- ✅ Check **duplicate detection** warnings during imports
- ✅ Review **failed records** to identify data issues

## Development

### Project Structure
- **Sites**: Streamlit pages for different tools
- **Components**: Reusable UI elements (environment selector, API config, etc.)
- **Helpers**: Business logic, API clients, and utilities
- **Session State**: Global state management for shared settings

## Contact

**Maintainer**: [fabian.kainz@poool.cc](mailto:fabian.kainz@poool.cc)

For feature requests, bug reports, or questions, please contact the maintainer.
