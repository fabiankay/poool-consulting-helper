import streamlit as st

from src.components import sidebar

sidebar.show_sidebar()

# define navigation
home = st.Page("sites/home.py", title="Home", icon="🏠", default=True)
personio = st.Page("sites/personio.py", title="Personio", icon="🧑‍💻")

# CRM pages
crm_import = st.Page("sites/crm.py", title="CRM Import", icon="📥")
crm_update = st.Page("sites/crm_update.py", title="CRM Update", icon="🔄")
person_update = st.Page("sites/person_update.py", title="Person Update", icon="👤")

# signature = st.Page("sites/signature_reader.py", title="Signature Reader", icon="✏️")
# clustering = st.Page("sites/clustering.py", title="Clustering", icon="🔍")

pg = st.navigation({
    "Basics": [home],
    "CRM Operations": [crm_import, crm_update, person_update],
    "Helpers": [personio]
})

pg.run()