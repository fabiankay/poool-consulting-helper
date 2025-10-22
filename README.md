# Poool Consulting Helper

Streamlit application for managing Poool CRM data imports and Personio employee checks.

## Features

- **CRM Import Tool**: Bulk import companies and persons to Poool CRM via API
  - CSV/Excel file upload with flexible column mapping
  - JSON-based mapping configuration (export/import)
  - Tag detection and assignment
  - Multi-environment support (production/staging/custom)

- **Personio Integration**: Employee verification and data management

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. Navigate to the tool you need and configure your API credentials

## Architecture

```
├── app.py                  # Main application entry point
├── sites/
│   ├── crm.py             # CRM import tool UI
│   ├── personio.py        # Personio integration
│   └── home.py            # Home page
└── src/helpers/
    ├── crm.py             # CRM business logic
    ├── poool_api_client.py # Poool API client
    └── personio.py        # Personio API helpers
```

## CRM Import Workflow

1. Select environment and test API connection
2. Upload CSV/Excel file with company or person data
3. Map CSV columns to API fields (or import saved mapping)
4. Configure tags and relationships
5. Review preview and execute import

## API Configuration

The application supports multiple Poool environments:
- **Production**: `app.poool.cc`
- **Staging**: `staging-app.poool.rocks`
- **Custom**: Your sandbox URL
