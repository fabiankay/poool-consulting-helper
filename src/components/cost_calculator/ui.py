"""
Hourly Rate UI Components

Reusable Streamlit UI components for hourly rate calculation interface.
Follows existing app patterns from crm_ui.py
"""

import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Dict, Optional, Tuple
from src.helpers.cost_calculator import (
    EmployeeGroup,
    OverheadCosts,
    PricingParameters
)


# ============================================================================
# INPUT FORMS
# ============================================================================

def render_basic_parameters() -> Dict:
    """
    Render basic calculation parameters

    Returns:
        Dictionary with fiscal_year, working_days_per_year, hours_per_day
    """
    st.markdown("### ⚙️ Grundparameter")

    col1, col2, col3 = st.columns(3)

    with col1:
        fiscal_year = st.number_input(
            "Geschäftsjahr",
            min_value=2020,
            max_value=2050,
            value=2025,
            step=1,
            help="Für welches Jahr soll die Kalkulation erstellt werden?"
        )

    with col2:
        working_days = st.number_input(
            "Arbeitstage pro Jahr",
            min_value=200,
            max_value=280,
            value=251,
            step=1,
            help="Anzahl der Arbeitstage im Jahr (Standard: 251 für DE 2025)"
        )

    with col3:
        hours_per_day = st.number_input(
            "Stunden pro Tag",
            min_value=6.0,
            max_value=12.0,
            value=8.0,
            step=0.5,
            help="Arbeitsstunden pro Tag"
        )

    return {
        'fiscal_year': int(fiscal_year),
        'working_days_per_year': int(working_days),
        'hours_per_day': float(hours_per_day)
    }


def render_employee_groups_form() -> List[EmployeeGroup]:
    """
    Render dynamic form for employee groups with add/remove functionality

    Uses session state to manage list of groups.

    Returns:
        List of EmployeeGroup objects
    """
    st.markdown("### 👥 Mitarbeitergruppen")

    # Initialize session state for groups
    if 'employee_groups_count' not in st.session_state:
        st.session_state.employee_groups_count = 1
        # Initialize first group with defaults
        st.session_state['group_name_0'] = 'Beispielgruppe'
        st.session_state['group_count_0'] = 1
        st.session_state['group_salary_0'] = 50000.0
        st.session_state['group_social_0'] = 20.0
        st.session_state['group_special_0'] = 0.0
        st.session_state['group_vacation_0'] = 30
        st.session_state['group_sick_0'] = 10
        st.session_state['group_productivity_0'] = 75.0

    groups_list = []

    # Render each group
    for idx in range(st.session_state.employee_groups_count):
        # Check if this group exists (not deleted)
        if f'group_name_{idx}' not in st.session_state:
            continue

        group_name = st.session_state.get(f'group_name_{idx}', f'Gruppe {idx + 1}')

        with st.expander(f"⚙️ {group_name}", expanded=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                name = st.text_input(
                    "Gruppenname",
                    key=f"group_name_{idx}",
                    help="z.B. 'Junior Entwickler', 'Senior Berater'"
                )

            with col2:
                if st.button("🗑️ Löschen", key=f"delete_{idx}", type="secondary"):
                    # Remove all keys for this group
                    for key in [f'group_name_{idx}', f'group_count_{idx}', f'group_salary_{idx}',
                               f'group_social_{idx}', f'group_special_{idx}', f'group_vacation_{idx}',
                               f'group_sick_{idx}', f'group_productivity_{idx}']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()

            col1, col2, col3 = st.columns(3)

            with col1:
                count = st.number_input(
                    "Anzahl Mitarbeiter",
                    min_value=1,
                    max_value=1000,
                    step=1,
                    key=f"group_count_{idx}"
                )

            with col2:
                salary = st.number_input(
                    "Ø Jahresgehalt brutto (€)",
                    min_value=0.0,
                    max_value=500000.0,
                    step=1000.0,
                    key=f"group_salary_{idx}",
                    help="Durchschnittliches Bruttogehalt pro Jahr"
                )

            with col3:
                social_sec = st.number_input(
                    "Sozialversicherung AG (%)",
                    min_value=0.0,
                    max_value=50.0,
                    step=1.0,
                    key=f"group_social_{idx}",
                    help="Arbeitgeberanteil (Standard: ~20%)"
                )

            col1, col2, col3 = st.columns(3)

            with col1:
                special_pay = st.number_input(
                    "Sonderzahlungen (€)",
                    min_value=0.0,
                    max_value=100000.0,
                    step=500.0,
                    key=f"group_special_{idx}",
                    help="Urlaubs-/Weihnachtsgeld, Boni"
                )

            with col2:
                vacation = st.number_input(
                    "Urlaubstage",
                    min_value=0,
                    max_value=365,
                    step=1,
                    key=f"group_vacation_{idx}"
                )

            with col3:
                sick = st.number_input(
                    "Ø Krankheitstage",
                    min_value=0,
                    max_value=365,
                    step=1,
                    key=f"group_sick_{idx}"
                )

            productivity = st.slider(
                "Produktivität (%)",
                min_value=30.0,
                max_value=95.0,
                step=5.0,
                key=f"group_productivity_{idx}",
                help="Anteil der Zeit für abrechenbare Projekte (Rest: interne Aufgaben, Meetings, etc.)"
            )

            # Create EmployeeGroup object from current widget values
            try:
                group = EmployeeGroup(
                    name=name,
                    count=int(count),
                    annual_salary_gross=float(salary),
                    social_security_percent=float(social_sec),
                    special_payments=float(special_pay),
                    vacation_days=int(vacation),
                    sick_days_average=int(sick),
                    productivity_percent=float(productivity)
                )
                groups_list.append(group)
            except Exception as e:
                st.error(f"Fehler in Gruppe '{name}': {str(e)}")

    # Add new group button
    if st.button("➕ Neue Gruppe hinzufügen", type="secondary"):
        idx = st.session_state.employee_groups_count
        st.session_state.employee_groups_count += 1
        # Initialize new group with defaults
        st.session_state[f'group_name_{idx}'] = f'Gruppe {idx + 1}'
        st.session_state[f'group_count_{idx}'] = 1
        st.session_state[f'group_salary_{idx}'] = 50000.0
        st.session_state[f'group_social_{idx}'] = 20.0
        st.session_state[f'group_special_{idx}'] = 0.0
        st.session_state[f'group_vacation_{idx}'] = 30
        st.session_state[f'group_sick_{idx}'] = 10
        st.session_state[f'group_productivity_{idx}'] = 75.0
        st.rerun()

    return groups_list


def render_overhead_costs_form() -> OverheadCosts:
    """
    Render overhead costs input form

    Returns:
        OverheadCosts object
    """
    st.markdown("### 💰 Gemeinkosten")
    st.info("💡 Tragen Sie die jährlichen Gemeinkosten ein. Die Summe wird automatisch auf die Stundensätze umgelegt.")

    col1, col2 = st.columns(2)

    with col1:
        office_costs = st.number_input(
            "Raumkosten (€/Jahr)",
            min_value=0.0,
            value=24000.0,
            step=1000.0,
            help="Miete, Nebenkosten, etc."
        )

        it_infrastructure = st.number_input(
            "IT-Infrastruktur (€/Jahr)",
            min_value=0.0,
            value=15000.0,
            step=1000.0,
            help="Server, Software-Lizenzen, Hardware"
        )

        office_supplies = st.number_input(
            "Büromaterial (€/Jahr)",
            min_value=0.0,
            value=3000.0,
            step=500.0,
            help="Verbrauchsmaterial, Kleingeräte"
        )

        insurance = st.number_input(
            "Versicherungen (€/Jahr)",
            min_value=0.0,
            value=5000.0,
            step=500.0,
            help="Betriebshaftpflicht, Rechtsschutz, etc."
        )

    with col2:
        marketing = st.number_input(
            "Marketing & Vertrieb (€/Jahr)",
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            help="Werbung, Events, Kundenakquise"
        )

        administration = st.number_input(
            "Verwaltungskosten (€/Jahr)",
            min_value=0.0,
            value=8000.0,
            step=1000.0,
            help="Buchhaltung, Steuerberater, Rechtsanwalt"
        )

        other = st.number_input(
            "Sonstige Kosten (€/Jahr)",
            min_value=0.0,
            value=0.0,
            step=500.0,
            help="Alle weiteren Gemeinkosten"
        )

    overhead = OverheadCosts(
        office_costs=office_costs,
        it_infrastructure=it_infrastructure,
        office_supplies=office_supplies,
        insurance=insurance,
        marketing=marketing,
        administration=administration,
        other=other
    )

    # Show total
    st.markdown("---")
    st.metric(
        "**Gemeinkosten gesamt**",
        f"{overhead.total():,.2f} €",
        help="Summe aller Gemeinkosten pro Jahr"
    )

    return overhead


def render_pricing_parameters_form() -> PricingParameters:
    """
    Render pricing parameters form

    Returns:
        PricingParameters object
    """
    st.markdown("### 📈 Kalkulationsparameter")

    col1, col2, col3 = st.columns(3)

    with col1:
        profit = st.slider(
            "Gewinnmarge (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=5.0,
            help="Angestrebte Gewinnmarge"
        )

    with col2:
        risk = st.slider(
            "Risikoaufschlag (%)",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=1.0,
            help="Puffer für Ausfallrisiken, Zahlungsverzug"
        )

    with col3:
        discount = st.slider(
            "Rabatt (%)",
            min_value=0.0,
            max_value=30.0,
            value=0.0,
            step=5.0,
            help="Standardrabatt für Kunden"
        )

    return PricingParameters(
        profit_margin_percent=profit,
        risk_surcharge_percent=risk,
        discount_percent=discount
    )


# ============================================================================
# CALCULATION DISPLAY
# ============================================================================

def render_calculation_steps(breakdown: Dict):
    """
    Render step-by-step calculation breakdown for one employee group

    Args:
        breakdown: Complete calculation breakdown from calculator.calculate_group_complete()
    """
    st.markdown(f"#### {breakdown['group_name']} ({breakdown['employee_count']} MA)")

    # Step 1: Productive Hours
    with st.expander("📅 Schritt 1: Produktive Stunden", expanded=False):
        prod = breakdown['productive_hours']

        st.markdown(f"""
        **Berechnung der produktiven Stunden pro Mitarbeiter:**

        1. **Anwesenheitstage** = {prod['total_working_days']} Arbeitstage - {prod['vacation_days']} Urlaub - {prod['sick_days']} Krankheit
           = **{prod['attendance_days']} Tage**

        2. **Anwesenheitsstunden** = {prod['attendance_days']} Tage × {prod['hours_per_day']} Std/Tag
           = **{prod['attendance_hours']:.0f} Stunden**

        3. **Produktive Stunden** = {prod['attendance_hours']:.0f} Std × {prod['productivity_percent']:.0f}% Produktivität
           = **{prod['productive_hours']:.0f} Stunden**
        """)

        st.metric("Produktive Stunden pro MA/Jahr", f"{prod['productive_hours']:.0f} h")

    # Step 2: Cost per Hour
    with st.expander("💵 Schritt 2: Kostenstundensatz", expanded=False):
        cost = breakdown['cost']

        st.markdown(f"""
        **Berechnung der Personalkosten pro Mitarbeiter:**

        1. **Jahresgehalt brutto**: {cost['annual_salary_gross']:,.2f} €

        2. **Sozialversicherung AG-Anteil** ({cost['social_security_percent']:.1f}%):
           {cost['annual_salary_gross']:,.2f} € × {cost['social_security_percent']:.1f}% = **{cost['social_security']:,.2f} €**

        3. **Sonderzahlungen**: {cost['special_payments']:,.2f} €

        4. **Personalkosten gesamt**:
           {cost['annual_salary_gross']:,.2f} € + {cost['social_security']:,.2f} € + {cost['special_payments']:,.2f} €
           = **{cost['personnel_cost_per_employee']:,.2f} €**

        5. **Kostenstundensatz**:
           {cost['personnel_cost_per_employee']:,.2f} € ÷ {cost['productive_hours']:.0f} Std
           = **{cost['cost_rate']:.2f} €/h**
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Personalkosten pro MA", f"{cost['personnel_cost_per_employee']:,.2f} €")
        with col2:
            st.metric("Kostenstundensatz", f"{cost['cost_rate']:.2f} €/h")

    # Step 3: Full Cost
    with st.expander("🏢 Schritt 3: Vollkostenstundensatz", expanded=False):
        full = breakdown['full_cost']

        st.markdown(f"""
        **Vollkosten inklusive Gemeinkostenzuschlag:**

        1. **Kostenstundensatz**: {full['cost_rate']:.2f} €/h

        2. **Gemeinkostenzuschlag** ({full['overhead_surcharge_percent']:.2f}%):
           {full['cost_rate']:.2f} € × {full['overhead_surcharge_percent']:.2f}% = **{full['overhead_amount_per_hour']:.2f} €/h**

        3. **Vollkostenstundensatz**:
           {full['cost_rate']:.2f} € + {full['overhead_amount_per_hour']:.2f} €
           = **{full['full_cost_rate']:.2f} €/h**
        """)

        st.metric("Vollkostenstundensatz", f"{full['full_cost_rate']:.2f} €/h")

    # Step 4: Sales Price
    with st.expander("💰 Schritt 4: Verkaufsstundensatz", expanded=False):
        sales = breakdown['sales']

        st.markdown(f"""
        **Verkaufspreis mit Gewinn, Risiko und Rabatt:**

        1. **Vollkosten**: {sales['full_cost_rate']:.2f} €/h

        2. **+ Gewinnmarge** ({sales['profit_margin_percent']:.1f}%):
           {sales['full_cost_rate']:.2f} € × (1 + {sales['profit_margin_percent']:.1f}%) = **{sales['after_profit']:.2f} €/h**

        3. **+ Risikoaufschlag** ({sales['risk_surcharge_percent']:.1f}%):
           {sales['after_profit']:.2f} € × (1 + {sales['risk_surcharge_percent']:.1f}%) = **{sales['after_risk']:.2f} €/h**

        4. **- Rabatt** ({sales['discount_percent']:.1f}%):
           {sales['after_risk']:.2f} € × (1 - {sales['discount_percent']:.1f}%) = **{sales['sales_rate']:.2f} €/h**
        """)

        st.metric("✅ Verkaufsstundensatz", f"{sales['sales_rate']:.2f} €/h", delta=f"+{sales['sales_rate'] - sales['full_cost_rate']:.2f} € vs. Vollkosten")


# ============================================================================
# RESULTS DISPLAY
# ============================================================================

def render_results_table(df: pd.DataFrame):
    """
    Render formatted results table with color coding

    Args:
        df: Results DataFrame from calculator.calculate_all_groups()
    """
    st.markdown("### 📊 Ergebnisübersicht")

    # Format the dataframe for display
    df_display = df.copy()

    # Format currency columns
    currency_cols = [
        'Kostenstundensatz (€/h)',
        'Vollkostensatz (€/h)',
        'Verkaufsstundensatz (€/h)',
        'Personalkosten gesamt (€/Jahr)',
        'Erwarteter Umsatz (€/Jahr)'
    ]

    for col in currency_cols:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: f"{x:,.2f} €")

    # Format hours column
    if 'Produktive Std./Jahr' in df_display.columns:
        df_display['Produktive Std./Jahr'] = df_display['Produktive Std./Jahr'].apply(lambda x: f"{x:,.0f} h")

    # Display with streamlit
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )


def render_plausibility_checks(plausibility: Dict):
    """
    Render plausibility checks and KPIs

    Args:
        plausibility: Dictionary from calculator.calculate_plausibility()
    """
    st.markdown("### ✅ Plausibilitätsprüfung")

    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Personalkosten",
            f"{plausibility['total_personnel_cost']:,.0f} €",
            help="Gesamte Personalkosten pro Jahr"
        )

    with col2:
        st.metric(
            "Gemeinkosten",
            f"{plausibility['overhead_costs']:,.0f} €",
            help="Gemeinkosten pro Jahr"
        )

    with col3:
        st.metric(
            "Erwarteter Umsatz",
            f"{plausibility['total_revenue']:,.0f} €",
            help="Erwarteter Jahresumsatz bei voller Auslastung"
        )

    with col4:
        delta_color = "normal" if plausibility['contribution_margin'] > 0 else "inverse"
        st.metric(
            "Deckungsbeitrag",
            f"{plausibility['contribution_margin']:,.0f} €",
            f"{plausibility['contribution_margin_percent']:.1f}%",
            delta_color=delta_color,
            help="Umsatz - Kosten"
        )

    # Show warnings
    if plausibility['warnings']:
        st.markdown("---")
        for warning in plausibility['warnings']:
            st.warning(warning)


# ============================================================================
# VISUALIZATIONS
# ============================================================================

def create_cost_distribution_chart(overhead: OverheadCosts) -> alt.Chart:
    """
    Create pie chart for overhead cost distribution

    Args:
        overhead: OverheadCosts object

    Returns:
        Altair chart
    """
    # Prepare data
    cost_dict = overhead.as_dict()
    data = pd.DataFrame([
        {"Kategorie": k, "Betrag": v}
        for k, v in cost_dict.items()
        if v > 0
    ])

    if data.empty:
        return None

    # Create chart
    chart = alt.Chart(data).mark_arc().encode(
        theta=alt.Theta(field="Betrag", type="quantitative"),
        color=alt.Color(field="Kategorie", type="nominal", legend=alt.Legend(title="Kostenart")),
        tooltip=[
            alt.Tooltip("Kategorie:N", title="Kostenart"),
            alt.Tooltip("Betrag:Q", title="Betrag (€)", format=",.2f")
        ]
    ).properties(
        title="Gemeinkostenverteilung",
        width=400,
        height=400
    )

    return chart


def create_group_comparison_chart(df: pd.DataFrame) -> alt.Chart:
    """
    Create bar chart comparing hourly rates across employee groups

    Args:
        df: Results DataFrame

    Returns:
        Altair chart
    """
    # Prepare data
    data = df[['Mitarbeitergruppe', 'Kostenstundensatz (€/h)', 'Vollkostensatz (€/h)', 'Verkaufsstundensatz (€/h)']].copy()

    # Melt for grouped bar chart
    data_melted = data.melt(
        id_vars=['Mitarbeitergruppe'],
        var_name='Stundensatzart',
        value_name='Betrag'
    )

    # Shorten labels
    data_melted['Stundensatzart'] = data_melted['Stundensatzart'].replace({
        'Kostenstundensatz (€/h)': 'Kosten',
        'Vollkostensatz (€/h)': 'Vollkosten',
        'Verkaufsstundensatz (€/h)': 'Verkauf'
    })

    # Create chart
    chart = alt.Chart(data_melted).mark_bar().encode(
        x=alt.X('Mitarbeitergruppe:N', title='Mitarbeitergruppe', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Betrag:Q', title='Stundensatz (€/h)'),
        color=alt.Color('Stundensatzart:N', title='Stundensatzart', scale=alt.Scale(scheme='category10')),
        xOffset='Stundensatzart:N',
        tooltip=[
            alt.Tooltip('Mitarbeitergruppe:N'),
            alt.Tooltip('Stundensatzart:N', title='Art'),
            alt.Tooltip('Betrag:Q', title='Betrag (€/h)', format='.2f')
        ]
    ).properties(
        title="Stundensatzvergleich nach Mitarbeitergruppe",
        width=600,
        height=400
    )

    return chart
