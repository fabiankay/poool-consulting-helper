import streamlit as st

from src.components import sidebar

sidebar.show_sidebar()

# define navigation
home = st.Page("sites/home.py", title="Übersicht", icon="🏠", default=True)

# CRM pages
crm_import = st.Page("sites/crm.py", title="CRM Import", icon="📥")
crm_update = st.Page("sites/crm_update.py", title="CRM Aktualisierung", icon="🔄")
person_update = st.Page("sites/person_update.py", title="Personen Aktualisierung", icon="👤")

# Tools pages
stundensatz = st.Page("sites/cost_calculator.py", title="Stundensatzkalkulation", icon="📊")
personio = st.Page("sites/personio.py", title="Personio", icon="🧑‍💻")

# Analytics pages
clustering = st.Page("sites/clustering.py", title="Clustering", icon="🔍")

pg = st.navigation({
    "Allgemein": [home],
    "CRM Operationen": [crm_import, crm_update, person_update],
    "Tools": [stundensatz, personio]
})

pg.run()