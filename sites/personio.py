import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import io

from src.helpers.personio import (
    create_personio_client,
    get_employees, get_absences, get_attendances,
    process_employees_data, process_absences_data, process_attendances_data
)

# Page configuration
st.set_page_config(
    page_title="Personio API-Abfrage-Tool",
    page_icon="🧑‍💻",
    layout="wide"
)

st.title("🧑‍💻 Personio API-Abfrage-Tool")
st.markdown("Geben Sie Ihre Personio API-Zugangsdaten ein, um sich zu authentifizieren und Mitarbeiterdaten, Abwesenheiten und Anwesenheiten abzurufen.")

# Initialize session state
if 'personio_client' not in st.session_state:
    st.session_state.personio_client = None
if 'employees_df' not in st.session_state:
    st.session_state.employees_df = None
if 'employees_column_mapping' not in st.session_state:
    st.session_state.employees_column_mapping = {}
if 'absences_df' not in st.session_state:
    st.session_state.absences_df = None
if 'absences_column_mapping' not in st.session_state:
    st.session_state.absences_column_mapping = {}
if 'attendances_df' not in st.session_state:
    st.session_state.attendances_df = None
if 'attendances_column_mapping' not in st.session_state:
    st.session_state.attendances_column_mapping = {}


def is_client_valid():
    """Check if the current Personio client is still valid"""
    if not st.session_state.personio_client:
        return False
    return st.session_state.personio_client.is_token_valid()


def create_excel_download(df):
    """Create Excel file in memory for download"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output.getvalue()


# API Credentials Section (Shared across all tabs)
st.markdown("---")
st.subheader("🔑 API-Authentifizierung")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    client_id = st.text_input(
        "Client-ID",
        type="default",
        help="Ihre Personio API Client-ID"
    )

with col2:
    client_secret = st.text_input(
        "Client-Secret",
        type="password",
        help="Ihr Personio API Client-Secret"
    )

with col3:
    st.write("")  # Spacing
    st.write("")  # Spacing
    if st.button("🔓 Authentifizieren", type="primary", use_container_width=True):
        if not client_id or not client_secret:
            st.error("Bitte geben Sie sowohl Client-ID als auch Client-Secret ein")
        else:
            with st.spinner("Authentifiziere..."):
                client = create_personio_client(client_id, client_secret)

                if not client:
                    st.error("Authentifizierung fehlgeschlagen: Ungültige Zugangsdaten oder API-Fehler")
                else:
                    st.session_state.personio_client = client
                    st.success("✅ Authentifizierung erfolgreich!")
                    st.rerun()

# Client status
if st.session_state.personio_client:
    if is_client_valid():
        time_left = st.session_state.personio_client.token_expires_at - datetime.now()
        minutes_left = int(time_left.total_seconds() / 60)
        st.success(f"🟢 Token ist gültig (läuft in {minutes_left} Minuten ab)")
    else:
        st.error("🔴 Token has expired - please re-authenticate")
        st.session_state.personio_client = None

st.markdown("---")

# Main Tabs
if st.session_state.personio_client and is_client_valid():
    tab1, tab2, tab3 = st.tabs(["👥 Mitarbeiter", "🏖️ Abwesenheiten", "⏰ Anwesenheiten"])

    # ========== TAB 1: EMPLOYEES ==========
    with tab1:
        st.markdown("### Mitarbeiterdaten")

        if st.button("📥 Mitarbeiter abrufen", type="secondary", key="fetch_employees"):
            with st.spinner("Hole Mitarbeiterdaten..."):
                employees_data, error = get_employees(st.session_state.personio_client)

                if error:
                    st.error(f"Fehler beim Abrufen der Mitarbeiter: {error}")
                else:
                    df, column_mapping, process_error = process_employees_data(employees_data)

                    if process_error:
                        st.error(f"Fehler beim Verarbeiten der Mitarbeiterdaten: {process_error}")
                    else:
                        st.session_state.employees_df = df
                        st.session_state.employees_column_mapping = column_mapping
                        st.rerun()

        if st.session_state.employees_df is not None:
            # Column mapping info
            with st.expander("📋 Spaltenzuordnung", expanded=False):
                st.write("Diese Tabelle zeigt die Zuordnung von API-Feldern zu DataFrame-Spalten:")
                mapping_df = pd.DataFrame.from_dict(
                    st.session_state.employees_column_mapping,
                    orient='index',
                    columns=['DataFrame-Spalte']
                ).reset_index().rename(columns={'index': 'API-Feld'})

                # Count not null and not empty values per column in mapping
                not_null_not_empty = []
                null_or_empty = []

                for _, row in mapping_df.iterrows():
                    col_name = row['DataFrame-Spalte']
                    if col_name in st.session_state.employees_df.columns:
                        col_data = st.session_state.employees_df[col_name]
                        not_null_not_empty.append(
                            ((col_data.notnull()) & (col_data.astype(str).str.strip() != '')).sum()
                        )
                        null_or_empty.append(
                            ((col_data.isnull()) | (col_data.astype(str).str.strip() == '')).sum()
                        )
                    else:
                        not_null_not_empty.append(0)
                        null_or_empty.append(0)

                mapping_df['Nicht-leer Anzahl'] = not_null_not_empty
                mapping_df['Leer Anzahl'] = null_or_empty
                st.dataframe(mapping_df, use_container_width=True, hide_index=True)

            # Display metrics
            st.markdown("#### 📊 Datenübersicht")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mitarbeiter gesamt", len(st.session_state.employees_df))
            with col2:
                st.metric("Attribute gesamt", len(st.session_state.employees_df.columns))
            with col3:
                st.metric("Datengröße", f"{st.session_state.employees_df.memory_usage(deep=True).sum() / 1024:.1f} KB")

            # Display the DataFrame
            st.dataframe(
                st.session_state.employees_df,
                use_container_width=True,
                hide_index=True
            )

            # Download options
            st.markdown("#### 💾 Download-Optionen")
            col1, col2 = st.columns(2)

            with col1:
                csv = st.session_state.employees_df.to_csv(index=False)
                st.download_button(
                    label="📄 Als CSV herunterladen",
                    data=csv,
                    file_name=f"personio_employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

            with col2:
                excel_data = create_excel_download(st.session_state.employees_df)
                st.download_button(
                    label="📊 Als Excel herunterladen",
                    data=excel_data,
                    file_name=f"personio_employees_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    # ========== TAB 2: ABSENCES ==========
    with tab2:
        st.markdown("### Abwesenheitsdaten")

        # Date range filters
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Startdatum (Optional)",
                value=None,
                help="Abwesenheiten ab diesem Datum filtern"
            )
        with col2:
            end_date = st.date_input(
                "Enddatum (Optional)",
                value=None,
                help="Abwesenheiten bis zu diesem Datum filtern"
            )

        # Format dates for API
        start_date_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d') if end_date else None

        if st.button("📥 Abwesenheiten abrufen", type="secondary", key="fetch_absences"):
            with st.spinner("Hole Abwesenheitsdaten..."):
                absences_data, error = get_absences(
                    st.session_state.personio_client,
                    start_date=start_date_str,
                    end_date=end_date_str
                )

                if error:
                    st.error(f"Fehler beim Abrufen der Abwesenheiten: {error}")
                else:
                    df, column_mapping, process_error = process_absences_data(absences_data)

                    if process_error:
                        st.error(f"Fehler beim Verarbeiten der Abwesenheitsdaten: {process_error}")
                    else:
                        st.session_state.absences_df = df
                        st.session_state.absences_column_mapping = column_mapping
                        st.rerun()

        if st.session_state.absences_df is not None:
            # Column mapping info
            with st.expander("📋 Spaltenzuordnung", expanded=False):
                st.write("Diese Tabelle zeigt die Zuordnung von API-Feldern zu DataFrame-Spalten:")
                mapping_df = pd.DataFrame.from_dict(
                    st.session_state.absences_column_mapping,
                    orient='index',
                    columns=['DataFrame-Spalte']
                ).reset_index().rename(columns={'index': 'API-Feld'})

                # Count not null and not empty values per column in mapping
                not_null_not_empty = []
                null_or_empty = []

                for _, row in mapping_df.iterrows():
                    col_name = row['DataFrame-Spalte']
                    if col_name in st.session_state.absences_df.columns:
                        col_data = st.session_state.absences_df[col_name]
                        not_null_not_empty.append(
                            ((col_data.notnull()) & (col_data.astype(str).str.strip() != '')).sum()
                        )
                        null_or_empty.append(
                            ((col_data.isnull()) | (col_data.astype(str).str.strip() == '')).sum()
                        )
                    else:
                        not_null_not_empty.append(0)
                        null_or_empty.append(0)

                mapping_df['Nicht-leer Anzahl'] = not_null_not_empty
                mapping_df['Leer Anzahl'] = null_or_empty
                st.dataframe(mapping_df, use_container_width=True, hide_index=True)

            # Display metrics
            st.markdown("#### 📊 Datenübersicht")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Abwesenheiten gesamt", len(st.session_state.absences_df))
            with col2:
                st.metric("Attribute gesamt", len(st.session_state.absences_df.columns))
            with col3:
                st.metric("Datengröße", f"{st.session_state.absences_df.memory_usage(deep=True).sum() / 1024:.1f} KB")

            # Display the DataFrame
            st.dataframe(
                st.session_state.absences_df,
                use_container_width=True,
                hide_index=True
            )

            # Download options
            st.markdown("#### 💾 Download-Optionen")
            col1, col2 = st.columns(2)

            with col1:
                csv = st.session_state.absences_df.to_csv(index=False)
                st.download_button(
                    label="📄 Als CSV herunterladen",
                    data=csv,
                    file_name=f"personio_absences_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_absences_csv"
                )

            with col2:
                excel_data = create_excel_download(st.session_state.absences_df)
                st.download_button(
                    label="📊 Als Excel herunterladen",
                    data=excel_data,
                    file_name=f"personio_absences_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_absences_excel"
                )

    # ========== TAB 3: ATTENDANCES ==========
    with tab3:
        st.markdown("### Anwesenheitsdaten")

        # Date range filters
        col1, col2 = st.columns(2)
        with col1:
            att_start_date = st.date_input(
                "Startdatum (Optional)",
                value=None,
                help="Anwesenheiten ab diesem Datum filtern",
                key="att_start_date"
            )
        with col2:
            att_end_date = st.date_input(
                "Enddatum (Optional)",
                value=None,
                help="Anwesenheiten bis zu diesem Datum filtern",
                key="att_end_date"
            )

        # Format dates for API
        att_start_date_str = att_start_date.strftime('%Y-%m-%d') if att_start_date else None
        att_end_date_str = att_end_date.strftime('%Y-%m-%d') if att_end_date else None

        if st.button("📥 Anwesenheiten abrufen", type="secondary", key="fetch_attendances"):
            with st.spinner("Hole Anwesenheitsdaten..."):
                attendances_data, error = get_attendances(
                    st.session_state.personio_client,
                    start_date=att_start_date_str,
                    end_date=att_end_date_str
                )

                if error:
                    st.error(f"Fehler beim Abrufen der Anwesenheiten: {error}")
                else:
                    df, column_mapping, process_error = process_attendances_data(attendances_data)

                    if process_error:
                        st.error(f"Fehler beim Verarbeiten der Anwesenheitsdaten: {process_error}")
                    else:
                        st.session_state.attendances_df = df
                        st.session_state.attendances_column_mapping = column_mapping
                        st.rerun()

        if st.session_state.attendances_df is not None:
            # Column mapping info
            with st.expander("📋 Spaltenzuordnung", expanded=False):
                st.write("Diese Tabelle zeigt die Zuordnung von API-Feldern zu DataFrame-Spalten:")
                mapping_df = pd.DataFrame.from_dict(
                    st.session_state.attendances_column_mapping,
                    orient='index',
                    columns=['DataFrame-Spalte']
                ).reset_index().rename(columns={'index': 'API-Feld'})

                # Count not null and not empty values per column in mapping
                not_null_not_empty = []
                null_or_empty = []

                for _, row in mapping_df.iterrows():
                    col_name = row['DataFrame-Spalte']
                    if col_name in st.session_state.attendances_df.columns:
                        col_data = st.session_state.attendances_df[col_name]
                        not_null_not_empty.append(
                            ((col_data.notnull()) & (col_data.astype(str).str.strip() != '')).sum()
                        )
                        null_or_empty.append(
                            ((col_data.isnull()) | (col_data.astype(str).str.strip() == '')).sum()
                        )
                    else:
                        not_null_not_empty.append(0)
                        null_or_empty.append(0)

                mapping_df['Nicht-leer Anzahl'] = not_null_not_empty
                mapping_df['Leer Anzahl'] = null_or_empty
                st.dataframe(mapping_df, use_container_width=True, hide_index=True)

            # Display metrics
            st.markdown("#### 📊 Datenübersicht")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anwesenheiten gesamt", len(st.session_state.attendances_df))
            with col2:
                st.metric("Attribute gesamt", len(st.session_state.attendances_df.columns))
            with col3:
                st.metric("Datengröße", f"{st.session_state.attendances_df.memory_usage(deep=True).sum() / 1024:.1f} KB")

            # Display the DataFrame
            st.dataframe(
                st.session_state.attendances_df,
                use_container_width=True,
                hide_index=True
            )

            # Download options
            st.markdown("#### 💾 Download-Optionen")
            col1, col2 = st.columns(2)

            with col1:
                csv = st.session_state.attendances_df.to_csv(index=False)
                st.download_button(
                    label="📄 Als CSV herunterladen",
                    data=csv,
                    file_name=f"personio_attendances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_attendances_csv"
                )

            with col2:
                excel_data = create_excel_download(st.session_state.attendances_df)
                st.download_button(
                    label="📊 Als Excel herunterladen",
                    data=excel_data,
                    file_name=f"personio_attendances_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_attendances_excel"
                )

else:
    st.info("🔐 Bitte authentifizieren Sie sich mit Ihren Personio API-Zugangsdaten, um auf Mitarbeiter-, Abwesenheits- und Anwesenheitsdaten zuzugreifen.")

# Footer
st.markdown("---")
st.markdown("💡 **Tipp:** Bewahren Sie API-Zugangsdaten sicher auf und teilen Sie diese nicht mit anderen.")
