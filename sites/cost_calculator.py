"""
Hourly Rate Calculation Page

Hourly rate calculation tool for consulting/service businesses.
Calculates cost-based and sales-based hourly rates with overhead allocation.
"""

import streamlit as st
from typing import List, Dict
from datetime import datetime, date
import pandas as pd

from src.helpers.cost_calculator import (
    HourlyRateCalculator,
    EmployeeGroup,
    OverheadCosts,
    PricingParameters,
    export_to_excel,
    export_to_json
)
from src.components.cost_calculator import (
    render_basic_parameters,
    render_employee_groups_form,
    render_overhead_costs_form,
    render_pricing_parameters_form,
    render_calculation_steps,
    render_results_table,
    render_plausibility_checks,
    create_cost_distribution_chart,
    create_group_comparison_chart,
    create_cost_waterfall_chart,
    create_revenue_vs_cost_chart,
    create_personnel_breakdown_chart,
    create_sensitivity_analysis_chart,
    render_apportion_mapping
)
from src.components.credentials import render_database_credential, get_credential_manager
from src.helpers.prism.queries import get_overhead_costs_by_apportion, get_productivity_metrics
from src.helpers.prism.database import validate_login


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Stundensatzkalkulation",
    page_icon="📊",
    layout="wide"
)


# ============================================================================
# HEADER
# ============================================================================

st.title("📊 Stundensatzkalkulation")
st.markdown("""
**Systematische Berechnung von Kosten- und Verkaufsstundensätzen**

Dieses Tool berechnet auf Basis Ihrer Personalkosten und Gemeinkosten die kalkulatorisch notwendigen
Stundensätze für Ihre Mitarbeitergruppen.
""")

st.markdown("---")


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'calculation_results' not in st.session_state:
    st.session_state.calculation_results = None

if 'calculation_details' not in st.session_state:
    st.session_state.calculation_details = None

if 'basic_params' not in st.session_state:
    st.session_state.basic_params = None

if 'overhead_costs' not in st.session_state:
    st.session_state.overhead_costs = None

if 'pricing_params' not in st.session_state:
    st.session_state.pricing_params = None

if 'overhead_surcharge_percent' not in st.session_state:
    st.session_state.overhead_surcharge_percent = 0

if 'plausibility' not in st.session_state:
    st.session_state.plausibility = None

# Database import related session state
if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False

if 'db_connection' not in st.session_state:
    st.session_state.db_connection = None

if 'db_import_date_range' not in st.session_state:
    st.session_state.db_import_date_range = None

if 'db_available_apportions' not in st.session_state:
    st.session_state.db_available_apportions = []


# ============================================================================
# HELPER FUNCTIONS FOR DATABASE IMPORT
# ============================================================================

def import_overhead_costs_from_db(conn, start_date: date, end_date: date, mapping: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Import overhead costs from database and map to cost categories.

    Args:
        conn: Database connection
        start_date: Start date for query
        end_date: End date for query
        mapping: Dictionary mapping overhead categories to apportion values

    Returns:
        Dictionary with overhead costs per category
    """
    # Fetch data from database
    df = get_overhead_costs_by_apportion(conn, start_date, end_date)

    # Initialize overhead costs
    overhead_costs = {
        'office_costs': 0.0,
        'it_infrastructure': 0.0,
        'office_supplies': 0.0,
        'insurance': 0.0,
        'marketing': 0.0,
        'administration': 0.0,
        'other': 0.0
    }

    # Sum costs according to mapping
    for category, apportions in mapping.items():
        for apportion in apportions:
            matching_rows = df[df['data_invoice_position_apportion'] == apportion]
            if not matching_rows.empty:
                overhead_costs[category] += matching_rows['total_cost'].sum()

    return overhead_costs


def import_productivity_metrics_from_db(conn, start_date: date, end_date: date) -> Dict[str, float]:
    """
    Import productivity metrics from database.

    Args:
        conn: Database connection
        start_date: Start date for query
        end_date: End date for query

    Returns:
        Dictionary with productivity metrics
    """
    # Fetch data from database
    df = get_productivity_metrics(conn, start_date, end_date)

    if df.empty:
        return None

    # Extract metrics from first row (aggregated data)
    row = df.iloc[0]

    return {
        'avg_vacation_days': float(row['avg_vacation_days']) if pd.notna(row['avg_vacation_days']) else 0,
        'avg_sick_days': float(row['avg_sick_days']) if pd.notna(row['avg_sick_days']) else 0,
        'avg_hours_per_day': float(row['avg_hours_per_day']) if pd.notna(row['avg_hours_per_day']) else 8.0,
        'productivity_percent': float(row['productivity_percent']) if pd.notna(row['productivity_percent']) else 100.0
    }


# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "📝 Eingabe",
    "🧮 Berechnung",
    "📊 Übersicht & Export"
])


# ============================================================================
# TAB 1: INPUT
# ============================================================================

with tab1:
    st.markdown("## 1️⃣ Dateneingabe")
    st.info("💡 **Hinweis:** Füllen Sie alle Felder aus und klicken Sie auf 'Berechnen', um die Stundensätze zu kalkulieren.")

    # Database import section (optional)
    with st.expander("🗄️ Daten aus Datenbank importieren (Optional)", expanded=False):
        st.markdown("Importieren Sie Gemeinkosten und Produktivitätsdaten direkt aus Ihrer Prism-Datenbank.")

        # Database credentials
        st.markdown("### 🔑 Datenbank-Verbindung")
        prism_connected = render_database_credential(
            api_name="prism",
            display_name="Prism Database",
            fields={'username': 'Username', 'password': 'Password'},
            test_func=lambda username, password: validate_login(
                username, password, "particles.poool.cc", "pa_prism"
            )
        )

        if prism_connected:
            st.success("✅ Verbindung zur Datenbank hergestellt")

            # Date range selector
            st.markdown("### 📅 Zeitraum wählen")
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Von",
                    value=date(date.today().year, 1, 1),
                    help="Startdatum für den Datenimport"
                )
            with col2:
                end_date = st.date_input(
                    "Bis",
                    value=date.today(),
                    help="Enddatum für den Datenimport"
                )

            st.session_state.db_import_date_range = (start_date, end_date)

            # Fetch available apportions button
            if st.button("🔍 Verfügbare Zuordnungen laden", key="fetch_apportions"):
                try:
                    # Get database credentials
                    manager = get_credential_manager()
                    prism_creds = manager.get_credentials("prism")

                    # Create connection
                    conn = st.connection("postgresql",
                                       dialect="postgresql",
                                       type="sql",
                                       host="particles.poool.cc",
                                       database="pa_prism",
                                       username=prism_creds["username"],
                                       password=prism_creds["password"]
                                       )

                    st.session_state.db_connection = conn

                    # Fetch apportion data
                    with st.spinner("Lade Zuordnungen..."):
                        df_apportions = get_overhead_costs_by_apportion(conn, start_date, end_date)

                        if df_apportions.empty:
                            st.warning("⚠️ Keine Daten im gewählten Zeitraum gefunden.")
                        else:
                            st.session_state.db_available_apportions = df_apportions['data_invoice_position_apportion'].tolist()
                            st.success(f"✅ {len(st.session_state.db_available_apportions)} Zuordnungen gefunden")

                except Exception as e:
                    st.error(f"❌ Fehler beim Laden der Zuordnungen: {str(e)}")

            # Create tabs for different import types
            st.markdown("---")
            tab_overhead, tab_productivity = st.tabs([
                "💰 Gemeinkosten",
                "⏱️ Produktivität"
            ])

            # Tab 1: Overhead Costs Import
            with tab_overhead:
                if st.session_state.db_available_apportions:
                    # Apportion mapping configuration
                    mapping = render_apportion_mapping(st.session_state.db_available_apportions)

                    st.markdown("---")

                    # Import button
                    if st.button("📥 Gemeinkosten importieren", key="import_overhead", type="primary"):
                        try:
                            with st.spinner("Importiere Gemeinkosten..."):
                                overhead_data = import_overhead_costs_from_db(
                                    st.session_state.db_connection,
                                    start_date,
                                    end_date,
                                    mapping
                                )

                                # Update session state for overhead costs form fields
                                total_imported = sum(overhead_data.values())
                                for key, value in overhead_data.items():
                                    st.session_state[key] = value

                                st.success(f"✅ Gemeinkosten erfolgreich importiert: €{total_imported:,.2f}")

                                # Show breakdown
                                st.markdown("**Importierte Werte:**")
                                overhead_labels = {
                                    'office_costs': 'Bürokosten',
                                    'it_infrastructure': 'IT-Infrastruktur',
                                    'office_supplies': 'Büromaterial',
                                    'insurance': 'Versicherungen',
                                    'marketing': 'Marketing & Werbung',
                                    'administration': 'Verwaltung',
                                    'other': 'Sonstige Kosten'
                                }
                                for key, value in overhead_data.items():
                                    if value > 0:
                                        st.write(f"- {overhead_labels[key]}: €{value:,.2f}")

                        except Exception as e:
                            st.error(f"❌ Fehler beim Import: {str(e)}")
                else:
                    st.info("ℹ️ Bitte laden Sie zuerst die verfügbaren Zuordnungen mit dem Button oben.")

            # Tab 2: Productivity Metrics Import
            with tab_productivity:
                if st.button("📥 Produktivitätsdaten importieren", key="import_productivity", type="primary"):
                    try:
                        with st.spinner("Importiere Produktivitätsdaten..."):
                            metrics = import_productivity_metrics_from_db(
                                st.session_state.db_connection,
                                start_date,
                                end_date
                            )

                            if metrics:
                                st.success("✅ Produktivitätsdaten erfolgreich importiert")

                                # Show what was imported
                                st.markdown("**Importierte Durchschnittswerte:**")
                                st.write(f"- Urlaubstage: {metrics['avg_vacation_days']:.1f} Tage")
                                st.write(f"- Krankheitstage: {metrics['avg_sick_days']:.1f} Tage")
                                st.write(f"- Stunden pro Tag: {metrics['avg_hours_per_day']:.1f} h")
                                st.write(f"- Produktivität: {metrics['productivity_percent']:.1f}%")

                                st.info("💡 Diese Werte können als Standard für neue Mitarbeitergruppen verwendet werden.")
                            else:
                                st.warning("⚠️ Keine Produktivitätsdaten im gewählten Zeitraum gefunden.")

                    except Exception as e:
                        st.error(f"❌ Fehler beim Import: {str(e)}")

        else:
            st.warning("⚠️ Bitte konfigurieren Sie die Datenbank-Verbindung oben, um Daten zu importieren.")

        st.markdown("---")

    # Employee groups (outside form because it has buttons)
    employee_groups = render_employee_groups_form()

    st.markdown("---")

    with st.form("calculation_form"):
        # Basic parameters
        basic_params = render_basic_parameters()

        st.markdown("---")

        # Overhead costs
        overhead_costs = render_overhead_costs_form()

        st.markdown("---")

        # Pricing parameters
        pricing_params = render_pricing_parameters_form()

        st.markdown("---")

        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button(
                "🚀 Stundensätze berechnen",
                type="primary",
                use_container_width=True
            )

    # Process calculation
    if submitted:
        # Validation
        if not employee_groups:
            st.error("❌ Mindestens eine Mitarbeitergruppe erforderlich!")
        else:
            try:
                with st.spinner("Berechne Stundensätze..."):
                    # Initialize calculator
                    calculator = HourlyRateCalculator(
                        working_days_per_year=basic_params['working_days_per_year'],
                        hours_per_day=basic_params['hours_per_day']
                    )

                    # Calculate overhead surcharge
                    overhead_surcharge_percent, overhead_breakdown = calculator.calculate_overhead_surcharge(
                        employee_groups,
                        overhead_costs
                    )

                    # Calculate for all groups
                    df_results = calculator.calculate_all_groups(
                        employee_groups,
                        overhead_costs,
                        pricing_params
                    )

                    # Get detailed breakdowns
                    calculation_details = []
                    for group in employee_groups:
                        breakdown = calculator.calculate_group_complete(
                            group,
                            overhead_surcharge_percent,
                            pricing_params
                        )
                        calculation_details.append(breakdown)

                    # Calculate plausibility
                    plausibility = calculator.calculate_plausibility(
                        df_results,
                        overhead_costs.total()
                    )

                    # Store in session state
                    st.session_state.calculation_results = df_results
                    st.session_state.calculation_details = calculation_details
                    st.session_state.basic_params = basic_params
                    st.session_state.overhead_costs = overhead_costs
                    st.session_state.pricing_params = pricing_params
                    st.session_state.overhead_surcharge_percent = overhead_surcharge_percent
                    st.session_state.plausibility = plausibility

                st.success("✅ Kalkulation erfolgreich durchgeführt! Wechseln Sie zu den Tabs 'Berechnung' oder 'Übersicht'.")

            except Exception as e:
                st.error(f"❌ Fehler bei der Berechnung: {str(e)}")
                st.exception(e)


# ============================================================================
# TAB 2: CALCULATION STEPS
# ============================================================================

with tab2:
    st.markdown("## 2️⃣ Berechnungsschritte")

    if st.session_state.calculation_details is None:
        st.info("ℹ️ Bitte führen Sie zuerst eine Berechnung im Tab 'Eingabe' durch.")
    else:
        st.markdown("""
        Hier sehen Sie die detaillierten Berechnungsschritte für jede Mitarbeitergruppe.
        Klicken Sie auf eine Gruppe, um die Formel-basierten Berechnungen zu sehen.
        """)

        st.markdown("---")

        # Display common overhead surcharge
        st.markdown("### 🏢 Gemeinkostenzuschlag")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Gemeinkosten gesamt",
                f"{st.session_state.overhead_costs.total():,.2f} €"
            )
        with col2:
            st.metric(
                "Personalkosten gesamt",
                f"{st.session_state.plausibility['total_personnel_cost']:,.2f} €"
            )
        with col3:
            st.metric(
                "Gemeinkostenzuschlag",
                f"{st.session_state.overhead_surcharge_percent:.2f} %",
                help="Dieser Zuschlag wird auf jeden Kostenstundensatz aufgeschlagen"
            )

        st.markdown("---")

        # Display calculation steps for each group
        st.markdown("### 🔍 Detaillierte Berechnung pro Gruppe")

        for detail in st.session_state.calculation_details:
            render_calculation_steps(detail)


# ============================================================================
# TAB 3: RESULTS & EXPORT
# ============================================================================

with tab3:
    st.markdown("## 3️⃣ Ergebnisse & Export")

    if st.session_state.calculation_results is None:
        st.info("ℹ️ Bitte führen Sie zuerst eine Berechnung im Tab 'Eingabe' durch.")
    else:
        # Results table
        render_results_table(st.session_state.calculation_results)

        st.markdown("---")

        # Plausibility checks
        render_plausibility_checks(st.session_state.plausibility)

        st.markdown("---")

        # Visualizations
        st.markdown("### 📈 Visualisierungen")

        # Section 1: Cost Analysis
        with st.expander("💰 Kostenanalyse", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Kostenaufbau (Waterfall)")
                chart_waterfall = create_cost_waterfall_chart(
                    st.session_state.calculation_details,
                    st.session_state.pricing_params
                )
                if chart_waterfall:
                    st.plotly_chart(chart_waterfall, use_container_width=True, config={
                        'displayModeBar': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'kostenaufbau_waterfall',
                            'height': 800,
                            'width': 1200,
                            'scale': 2
                        }
                    })

            with col2:
                st.markdown("#### Personalkostenaufschlüsselung")
                chart_personnel = create_personnel_breakdown_chart(st.session_state.calculation_details)
                if chart_personnel:
                    st.plotly_chart(chart_personnel, use_container_width=True, config={
                        'displayModeBar': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'personalkosten_breakdown',
                            'height': 800,
                            'width': 1200,
                            'scale': 2
                        }
                    })

        # Section 2: Financial Performance
        with st.expander("📊 Finanzielle Performance", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Umsatz vs. Kosten")
                chart_revenue = create_revenue_vs_cost_chart(st.session_state.plausibility)
                if chart_revenue:
                    st.plotly_chart(chart_revenue, use_container_width=True, config={
                        'displayModeBar': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'revenue_vs_cost',
                            'height': 800,
                            'width': 1200,
                            'scale': 2
                        }
                    })

            with col2:
                st.markdown("#### Sensitivitätsanalyse")
                chart_sensitivity = create_sensitivity_analysis_chart(
                    st.session_state.calculation_details,
                    st.session_state.pricing_params,
                    st.session_state.overhead_surcharge_percent
                )
                if chart_sensitivity:
                    st.plotly_chart(chart_sensitivity, use_container_width=True, config={
                        'displayModeBar': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'sensitivity_analysis',
                            'height': 800,
                            'width': 1200,
                            'scale': 2
                        }
                    })

        # Section 3: Rate Comparison & Overhead Distribution
        with st.expander("📈 Vergleiche & Verteilung", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Stundensatzvergleich")
                chart_comparison = create_group_comparison_chart(st.session_state.calculation_results)
                if chart_comparison:
                    st.plotly_chart(chart_comparison, use_container_width=True, config={
                        'displayModeBar': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'rate_comparison',
                            'height': 800,
                            'width': 1200,
                            'scale': 2
                        }
                    })

            with col2:
                st.markdown("#### Gemeinkostenverteilung")
                chart_costs = create_cost_distribution_chart(st.session_state.overhead_costs)
                if chart_costs:
                    st.plotly_chart(chart_costs, use_container_width=True, config={
                        'displayModeBar': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'overhead_distribution',
                            'height': 800,
                            'width': 1200,
                            'scale': 2
                        }
                    })
                else:
                    st.info("Keine Gemeinkosten eingetragen")

        st.markdown("---")

        # Export section
        st.markdown("### 💾 Export")

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            # Excel export
            try:
                excel_file = export_to_excel(
                    st.session_state.calculation_results,
                    st.session_state.calculation_details,
                    st.session_state.basic_params,
                    st.session_state.overhead_costs.total(),
                    st.session_state.plausibility
                )

                filename_excel = f"Stundensatzkalkulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

                st.download_button(
                    label="📊 Excel exportieren",
                    data=excel_file,
                    file_name=filename_excel,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Fehler beim Excel-Export: {str(e)}")

        with col2:
            # JSON export
            try:
                json_data = export_to_json(
                    st.session_state.calculation_results,
                    st.session_state.calculation_details,
                    st.session_state.basic_params,
                    st.session_state.overhead_costs.model_dump(),
                    st.session_state.pricing_params.model_dump(),
                    st.session_state.plausibility
                )

                filename_json = f"Stundensatzkalkulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

                st.download_button(
                    label="📄 JSON exportieren",
                    data=json_data,
                    file_name=filename_json,
                    mime="application/json",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Fehler beim JSON-Export: {str(e)}")

        with col3:
            # CSV export (simple)
            csv_data = st.session_state.calculation_results.to_csv(index=False)
            filename_csv = f"Stundensatzkalkulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            st.download_button(
                label="📑 CSV exportieren",
                data=csv_data,
                file_name=filename_csv,
                mime="text/csv",
                use_container_width=True
            )


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<small>
**Hinweis:** Diese Kalkulation dient als Orientierung. Bitte prüfen Sie die Ergebnisse
und passen Sie sie ggf. an Ihre individuellen Anforderungen an.
</small>
""", unsafe_allow_html=True)
