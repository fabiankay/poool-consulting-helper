import streamlit as st

st.set_page_config(
    page_title="Poool Consulting Helper",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Poool Consulting Helper")
st.markdown("Hilfreiche Tools für CRM-Datenverwaltung, Personio-Integrationen und Stundensatzkalkulation")

st.markdown("---")

# CRM Operationen
st.subheader("📊 CRM Helper")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📥 CRM Import**")
    st.markdown("""
    - Firmen und Personen aus CSV/Excel importieren
    - Kunden-/Lieferanten-Auswahl
    - Tag-Verwaltung
    - JSON-Konfigurationen
    """)
    if st.button("Öffnen →", key="btn_import", use_container_width=True):
        st.switch_page("sites/crm.py")

with col2:
    st.markdown("**🔄 CRM Aktualisierung**")
    st.markdown("""
    - Massenaktualisierung bestehender Firmen
    - Abgleich nach ID, Name oder Kundennummer
    - Vorschau- und Test-Modus
    - Multi-Endpunkt-Unterstützung
    """)
    if st.button("Öffnen →", key="btn_update", use_container_width=True):
        st.switch_page("sites/crm_update.py")

with col3:
    st.markdown("**👤 Personen Aktualisierung**")
    st.markdown("""
    - Massenaktualisierung bestehender Personen
    - Abgleich nach ID, E-Mail oder Name
    - Vorschau- und Test-Modus
    - Kontaktdaten-Aktualisierung
    """)
    if st.button("Öffnen →", key="btn_person", use_container_width=True):
        st.switch_page("sites/person_update.py")

st.markdown("---")

# Hilfswerkzeuge
st.subheader("🛠️ Hilfswerkzeuge")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**📊 Stundensatzkalkulation**")
    st.markdown("""
    - Kosten- und Verkaufsstundensätze berechnen
    - Mitarbeitergruppen mit Produktivität
    - Gemeinkostenverteilung
    - Excel-, JSON-, CSV-Export
    """)
    if st.button("Öffnen →", key="btn_stundensatz", use_container_width=True):
        st.switch_page("sites/cost_calculator.py")

with col2:
    st.markdown("**🧑‍💻 Personio**")
    st.markdown("""
    - Mitarbeiter abrufen
    - Abwesenheiten, Anwesenheiten abrufen
    - Export nach CSV/Excel
    - Datumsbereichsfilterung
    """)
    if st.button("Öffnen →", key="btn_personio", use_container_width=True):
        st.switch_page("sites/personio.py")

st.markdown("---")

# Analytics
st.subheader("📈 Analytics")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("**🔍 Clustering**")
    st.markdown("""
    - Client-Segmentierung auf Basis von Finanzdaten
    - K-Means Clustering-Algorithmus
    - Prism-Datenbank Integration
    - Automatische Tag-Erstellung in Poool CRM
    """)
    if st.button("Öffnen →", key="btn_clustering", use_container_width=True):
        st.switch_page("sites/clustering.py")

with col2:
    # Placeholder for future analytics tools
    pass

st.markdown("---")
st.markdown("Fragen, Ideen oder Feedback: [fabian.kainz@poool.cc](mailto:fabian.kainz@poool.cc)")
