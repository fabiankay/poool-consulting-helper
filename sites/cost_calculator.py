"""
Hourly Rate Calculation Page

Hourly rate calculation tool for consulting/service businesses.
Calculates cost-based and sales-based hourly rates with overhead allocation.
"""

import streamlit as st
from typing import List, Dict
from datetime import datetime

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
    create_group_comparison_chart
)


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

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Gemeinkostenverteilung")
            chart_costs = create_cost_distribution_chart(st.session_state.overhead_costs)
            if chart_costs:
                st.altair_chart(chart_costs, use_container_width=True)
            else:
                st.info("Keine Gemeinkosten eingetragen")

        with col2:
            st.markdown("#### Stundensatzvergleich")
            chart_comparison = create_group_comparison_chart(st.session_state.calculation_results)
            st.altair_chart(chart_comparison, use_container_width=True)

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
