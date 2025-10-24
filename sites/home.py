import streamlit as st

st.set_page_config(
    page_title="Poool Consulting Helper",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Poool Consulting Helper")
st.markdown("Internal tools for CRM data management and HR integrations")

st.markdown("---")

# CRM Operations
st.subheader("📊 CRM Operations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📥 CRM Import**")
    st.markdown("""
    - Import companies and persons from CSV/Excel
    - Field mapping with auto-detection
    - Tag management
    - JSON configurations
    """)
    if st.button("Open →", key="btn_import", use_container_width=True):
        st.switch_page("sites/crm.py")

with col2:
    st.markdown("**🔄 CRM Update**")
    st.markdown("""
    - Bulk update existing companies
    - Match by ID, name, or customer number
    - Preview and dry run mode
    - Multi-endpoint support
    """)
    if st.button("Open →", key="btn_update", use_container_width=True):
        st.switch_page("sites/crm_update.py")

with col3:
    st.markdown("**👤 Person Update**")
    st.markdown("""
    - Bulk update existing persons
    - Match by ID, email, or name
    - Preview and dry run mode
    - Contact info updates
    """)
    if st.button("Open →", key="btn_person", use_container_width=True):
        st.switch_page("sites/person_update.py")

st.markdown("---")

# Helpers
st.subheader("🛠️ Helpers")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**🧑‍💻 Personio**")
    st.markdown("""
    - Fetch employees, absences, attendances
    - Export to CSV/Excel
    - Date range filtering
    """)
    if st.button("Open →", key="btn_personio", use_container_width=True):
        st.switch_page("sites/personio.py")

st.markdown("---")

# Quick Guide
st.subheader("📝 Quick Start")

st.markdown("""
**1. Choose Environment**
- Production: Live data
- Staging: Test environment
- Custom: Sandbox URL

**2. API Setup**
- Enter API key
- Test connection

**3. Common Tasks**
- Import new data → CRM Import
- Update existing data → CRM/Person Update
- Export HR data → Personio

**Tips:**
- Start with staging environment
- Use dry run mode before updates
- Save JSON mappings for reuse
""")

st.markdown("---")
st.markdown("Contact: [fabian.kainz@poool.cc](mailto:fabian.kainz@poool.cc)")
