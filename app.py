import streamlit as st

from src.components import sidebar

sidebar.show_sidebar()

# define navigation
home = st.Page("sites/home.py", title="Home", icon="🏠", default=True)
personio = st.Page("sites/personio.py", title="Personio", icon="🧑‍💻")
contacts = st.Page("sites/crm.py", title="Kontakte", icon="🐨")
# signature = st.Page("sites/signature_reader.py", title="Signature Reader", icon="✏️")
# clustering = st.Page("sites/clustering.py", title="Clustering", icon="🔍")

pg = st.navigation({
    "Basics": [home],
    "Helpers": [personio, contacts]
})

pg.run()