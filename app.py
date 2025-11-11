import streamlit as st

from src.components.common import sidebar
from src.components.credentials import (
    get_credential_manager,
    CredentialType,
    CredentialScope
)
from src.helpers.prism import validate_login

sidebar.show_sidebar()

# Initialize credential manager with API registrations
def init_credentials():
    """Register all APIs with the credential manager at app startup."""
    manager = get_credential_manager()

    # Register Prism database (if not already registered)
    if not manager.get_api_config("prism"):
        manager.register_api(
            name="prism",
            display_name="Prism Analytics Database",
            credential_type=CredentialType.DATABASE,
            scope=CredentialScope.PAGE_LOCAL,
            validator_func=lambda username, password, **kwargs: validate_login(
                username, password, "particles.poool.cc", "pa_prism"
            ),
            credential_fields=['username', 'password']
        )

# Call credential initialization
init_credentials()

# define navigation
home = st.Page("sites/home.py", title="Übersicht", icon="🏠", default=True)

# CRM pages
crm_import = st.Page("sites/crm.py", title="CRM Import", icon="📥")
crm_update = st.Page("sites/crm_update.py", title="CRM Aktualisierung", icon="🔄")
person_update = st.Page("sites/person_update.py", title="Personen Aktualisierung", icon="👤")

# Tools pages
cost_calculator = st.Page("sites/cost_calculator.py", title="Stundensatzkalkulation", icon="📊")
personio = st.Page("sites/personio.py", title="Personio", icon="🧑‍💻")

# Analytics pages
clustering = st.Page("sites/clustering.py", title="Clustering", icon="🔍")

pg = st.navigation({
    "Allgemein": [home],
    "CRM Operationen": [crm_import, crm_update, person_update],
    "Tools": [cost_calculator, personio],
    "Analytics": [clustering]
})

pg.run()