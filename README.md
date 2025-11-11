# Poool Consulting Helper

Streamlit-based internal tools for CRM data management, HR integrations, cost calculation, and analytics.

## Features

### 📥 CRM Import
Bulk import companies and persons to Poool CRM via API
- CSV/Excel file upload with flexible column mapping
- Smart field auto-detection with German labels
- Organized field mapping with categorized tabs (Stammdaten, Adresse, Kontakt, etc.)
- Tag management and organization
- JSON-based mapping configuration (export/import for reuse)
- Duplicate detection
- Multi-environment support (production/staging/sandbox)

### 🔄 CRM Update
Bulk update existing companies in Poool CRM
- Match records by ID, name, or customer number
- Update core, client, and supplier fields organized in tabs
- German-labeled fields for better usability
- Preview matches before updating
- Dry run mode for safe testing
- Multi-endpoint support (companies/clients/suppliers)

### 👤 Person Update
Bulk update existing persons in Poool CRM
- Match records by ID, email, or name
- Update contact information and personal details
- Tabbed interface with German labels (Stammdaten, Details, Firma)
- Preview and dry run support
- Batch processing with error reporting

### 🧑‍💻 Personio Integration
Access HR data from Personio API
- Fetch employees, absences, and attendances
- Optional date range filtering
- Export to CSV/Excel
- Automatic pagination handling
- OAuth2 authentication with token management

### 💰 Cost Calculator (Stundensatzkalkulation)
Systematic calculation of cost and sales hourly rates for consulting and service businesses
- **Employee Groups**: Define and manage multiple employee groups with individual salaries
- **Overhead Costs**: Track office rent, IT, insurance, marketing, and other overhead expenses
- **Calculation Parameters**: Configure profit margin, risk buffer, and discount rates
- **Detailed Calculations**: Step-by-step display of calculation logic
  - Productive hours = (Working days - Vacation - Sick days) × Hours/day × Productivity%
  - Cost rate = (Salary + Social security + Bonuses) / Productive hours
  - Full cost rate = Cost rate × (1 + Overhead%)
  - Sales rate = Full cost × (1 + Profit%) × (1 + Risk%) × (1 - Discount%)
- **Export Options**: Download as Excel, JSON, or CSV
- **Visualizations**: Cost distribution charts and group comparisons
- **Plausibility Checks**: Automatic warnings for negative margins or unfavorable rates
- **Session Persistence**: Save and reuse calculations within your session

### 🔍 Clustering Analytics
Client segmentation based on financial data using K-Means clustering
- **Database Integration**: Connect to Prism PostgreSQL analytics database
- **K-Means Clustering**: Configure number of clusters (2-10) for client segmentation
- **Feature-Based Segmentation**: Cluster clients based on:
  - Invoice amounts and quantities
  - Credit note amounts and quantities
  - Project counts
  - Total revenue
- **Automatic Tag Management**: Create and assign cluster tags in Poool CRM automatically
- **Visualization**: View clustering results with statistics per cluster
- **CRM Integration**: Seamlessly update client tags in Poool CRM using existing credentials

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure credentials:**
   - Create `.streamlit/secrets.toml` for sensitive credentials (optional)
   - Or enter credentials directly in the UI

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the tools:**
   - Navigate to `http://localhost:8501`
   - Choose your tool from the sidebar
   - Configure API credentials and environment

## Technology Stack

### Core Framework
- **Streamlit 1.42.0**: Web application framework
- **Python 3.9+**: Programming language

### Data Processing
- **Pandas 2.2.3**: Data manipulation and analysis
- **Pydantic 2.10.6**: Data validation and settings management
- **SQLAlchemy 2.0.37**: Database ORM for Prism integration

### Visualization & Export
- **Altair 5.5.0**: Declarative statistical visualizations
- **XlsxWriter 3.2.0**: Excel file generation

### APIs & HTTP
- **Requests 2.32.3**: HTTP library for API calls
- **Poool CRM API**: Custom API client implementation
- **Personio API**: HR system integration

### Machine Learning
- **scikit-learn 1.6.1**: K-Means clustering for client segmentation

### Database
- **PostgreSQL**: Prism analytics database via psycopg2-binary 2.9.10

## Architecture

```
poool-consulting-helper/
├── app.py                              # Main application entry point
├── docs/                               # Documentation
│   └── api_docs.json                   # Poool CRM API documentation
├── sites/                              # UI pages
│   ├── home.py                         # Dashboard and navigation
│   ├── crm.py                          # CRM import tool
│   ├── crm_update.py                   # CRM company update tool
│   ├── person_update.py                # CRM person update tool
│   ├── personio.py                     # Personio integration
│   ├── cost_calculator.py              # Cost/hourly rate calculator
│   └── clustering.py                   # Client clustering analytics
├── src/
│   ├── components/                     # Reusable UI components
│   │   ├── crm_ui.py                   # Shared CRM UI components
│   │   ├── entity_update_page.py       # Generic update page component
│   │   ├── field_mapping_builder.py    # Reusable field mapping UI builder
│   │   ├── session_state_manager.py    # Global state management
│   │   ├── sidebar.py                  # App sidebar
│   │   ├── cost_calculator_ui.py       # Cost calculator UI components
│   │   └── credential_manager.py       # Centralized credential management
│   └── helpers/                        # Business logic and API clients
│       ├── crm/                        # CRM operation modules
│       │   ├── __init__.py             # Module exports
│       │   ├── field_definitions.py    # Field definitions and labels
│       │   ├── company_operations.py   # Company-specific operations
│       │   ├── person_operations.py    # Person-specific operations
│       │   ├── update_operations.py    # Update and matching logic
│       │   ├── tag_operations.py       # Tag management
│       │   ├── validation.py           # Data validation
│       │   └── import_operations.py    # Generic import logic
│       ├── poool_api_client.py         # Poool CRM API client
│       ├── personio.py                 # Personio helpers
│       ├── personio_api_client.py      # Personio API client
│       ├── cost_calculator.py          # Cost calculation logic with Pydantic models
│       ├── cost_calculator_export.py   # Export functions (Excel, JSON, CSV)
│       └── mapping_utils.py            # Mapping utilities
├── .streamlit/
│   ├── config.toml                     # Streamlit configuration
│   └── secrets.toml                    # Optional: Store credentials (gitignored)
└── static/                             # Static assets
```

### Design Patterns
- **Separation of Concerns**: UI (components) separated from business logic (helpers)
- **Component Reusability**: Shared UI components eliminate code duplication
- **Configuration-Driven**: Generic entity update pages configured for different entities
- **Modular Architecture**: CRM operations split into focused submodules
- **Pydantic Validation**: Automatic validation for cost calculator inputs
- **Session State Management**: Consistent state handling across pages

## Common Workflows

### CRM Import
1. Select environment and test API connection
2. Upload CSV/Excel file with company or person data
3. Map CSV columns to API fields using categorized tabs (or import saved mapping)
4. Configure tags and relationship flags (client/supplier)
5. Review preview and execute import
6. Download mapping as JSON for reuse

### CRM Update
1. Select environment and verify API connection
2. Upload CSV/Excel with data to update
3. Choose identifier field (ID, name, customer_number)
4. Map fields to update using categorized tabs with German labels
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

### Cost Calculator
1. Navigate to "Stundensatzkalkulation" in the sidebar
2. **Eingabe** (Tab 1): Enter base parameters
   - Set year and working days
   - Add employee groups with salary, benefits, vacation, sick days, productivity
   - Enter overhead costs (office, IT, insurance, marketing, other)
   - Configure calculation parameters (profit margin, risk buffer, discount)
   - Click "Berechnen"
3. **Berechnung** (Tab 2): Review detailed calculations
   - See step-by-step calculations per employee group
   - Review formulas and intermediate results
4. **Übersicht & Export** (Tab 3): Analyze results
   - View summary table with all hourly rates
   - Check plausibility warnings
   - Review visualizations (cost distribution, group comparison)
   - Export as Excel, JSON, or CSV

### Client Clustering
1. Navigate to "Clustering" in the sidebar
2. Configure Prism database connection
3. Test connection to verify credentials
4. Set clustering parameters (number of clusters)
5. Click "Clustering durchführen" to run analysis
6. Review results and cluster statistics
7. Optionally create and assign cluster tags in Poool CRM

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

### Prism Database (Clustering)
- PostgreSQL connection required
- Credentials can be stored in `.streamlit/secrets.toml` or entered in UI
- Used for fetching client financial data for clustering analysis

## Setup Instructions

### Credential Management
This application supports centralized credential management through `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml (add to .gitignore!)

[poool_crm]
api_key = "your-poool-api-key"
environment = "staging"  # or "production"

[personio]
client_id = "your-personio-client-id"
client_secret = "your-personio-client-secret"

[prism]
host = "your-prism-host"
database = "your-database-name"
user = "your-username"
password = "your-password"
port = 5432
```

Alternatively, enter credentials directly in the UI. The application will use secrets.toml as defaults if available.

## Best Practices

- ✅ Start with **staging** or **dry run mode** before production updates
- ✅ Use **preview matches** to verify which records will be affected
- ✅ Download and save **mapping JSONs** for recurring imports
- ✅ Check **duplicate detection** warnings during imports
- ✅ Review **failed records** to identify data issues
- ✅ Use **German labels** in field mapping for better usability
- ✅ Store sensitive credentials in `.streamlit/secrets.toml` (never commit this file)
- ✅ Run **cost calculations** before finalizing project quotes
- ✅ Review **plausibility warnings** in cost calculator results
- ✅ Test **clustering** with different parameters to find optimal segmentation

## Development

### Project Structure
- **Sites**: Streamlit pages for different tools
- **Components**: Reusable UI elements (environment selector, API config, field mapping, etc.)
- **Helpers**: Business logic, API clients, and utilities organized by domain
- **Session State**: Global state management for shared settings

### Adding New Features
1. Create UI page in `sites/` directory
2. Add reusable components to `src/components/`
3. Implement business logic in appropriate `src/helpers/` module
4. Update `app.py` navigation if needed
5. Document in this README

## Changelog

### Version 1.0 (2025-11-08)
**Cost Calculator Release**
- ✅ Initial implementation of Stundensatzkalkulation
- ✅ 3 tabs (Eingabe, Berechnung, Übersicht)
- ✅ Pydantic validation for all inputs
- ✅ Excel, JSON, and CSV export
- ✅ Altair visualizations
- ✅ Plausibility checks
- ✅ Session state management

### Recent Updates
**CRM Field Mapping Enhancement**
- ✅ Reorganized import and update pages with categorized tabs
- ✅ Added German labels for all CRM fields
- ✅ Implemented 2-column layout for better space utilization
- ✅ Removed 187 lines of legacy code
- ✅ Fixed critical bug with undefined tag_tab_idx variable

**Clustering Analytics**
- ✅ K-Means clustering for client segmentation
- ✅ Prism database integration
- ✅ Automatic CRM tag creation and assignment
- ✅ Visualization of clustering results

**Architecture Improvements**
- ✅ Refactored CRM helpers into modular subpackages
- ✅ Created reusable FieldMappingBuilder component
- ✅ Implemented generic EntityUpdatePage component
- ✅ Centralized credential management system

## Contact

**Maintainer**: [fabian.kainz@poool.cc](mailto:fabian.kainz@poool.cc)

For feature requests, bug reports, or questions, please contact the maintainer.
