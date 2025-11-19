"""
Hourly Rate UI Components

Reusable Streamlit UI components for hourly rate calculation interface.
Follows existing app patterns from crm_ui.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
            value=st.session_state.get('office_costs', 24000.0),
            step=1000.0,
            key='office_costs',
            help="Miete, Nebenkosten, etc."
        )

        it_infrastructure = st.number_input(
            "IT-Infrastruktur (€/Jahr)",
            min_value=0.0,
            value=st.session_state.get('it_infrastructure', 15000.0),
            step=1000.0,
            key='it_infrastructure',
            help="Server, Software-Lizenzen, Hardware"
        )

        office_supplies = st.number_input(
            "Büromaterial (€/Jahr)",
            min_value=0.0,
            value=st.session_state.get('office_supplies', 3000.0),
            step=500.0,
            key='office_supplies',
            help="Verbrauchsmaterial, Kleingeräte"
        )

        insurance = st.number_input(
            "Versicherungen (€/Jahr)",
            min_value=0.0,
            value=st.session_state.get('insurance', 5000.0),
            step=500.0,
            key='insurance',
            help="Betriebshaftpflicht, Rechtsschutz, etc."
        )

    with col2:
        marketing = st.number_input(
            "Marketing & Vertrieb (€/Jahr)",
            min_value=0.0,
            value=st.session_state.get('marketing', 10000.0),
            step=1000.0,
            key='marketing',
            help="Werbung, Events, Kundenakquise"
        )

        administration = st.number_input(
            "Verwaltungskosten (€/Jahr)",
            min_value=0.0,
            value=st.session_state.get('administration', 8000.0),
            step=1000.0,
            key='administration',
            help="Buchhaltung, Steuerberater, Rechtsanwalt"
        )

        other = st.number_input(
            "Sonstige Kosten (€/Jahr)",
            min_value=0.0,
            value=st.session_state.get('other', 0.0),
            step=500.0,
            key='other',
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

def create_cost_distribution_chart(overhead: OverheadCosts) -> go.Figure:
    """
    Create pie chart for overhead cost distribution using Plotly

    Args:
        overhead: OverheadCosts object

    Returns:
        Plotly figure
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
    fig = go.Figure(data=[go.Pie(
        labels=data['Kategorie'],
        values=data['Betrag'],
        hovertemplate='<b>%{label}</b><br>Betrag: €%{value:,.2f}<br>Anteil: %{percent}<extra></extra>',
        textinfo='label+percent',
        textposition='auto',
    )])

    fig.update_layout(
        title="Gemeinkostenverteilung",
        showlegend=True,
        height=500,
        margin=dict(t=50, b=20, l=20, r=20)
    )

    return fig


def create_group_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart comparing hourly rates across employee groups using Plotly

    Args:
        df: Results DataFrame

    Returns:
        Plotly figure
    """
    # Prepare data
    groups = df['Mitarbeitergruppe'].tolist()
    cost_rates = df['Kostenstundensatz (€/h)'].tolist()
    full_cost_rates = df['Vollkostensatz (€/h)'].tolist()
    sales_rates = df['Verkaufsstundensatz (€/h)'].tolist()

    # Create chart
    fig = go.Figure(data=[
        go.Bar(name='Kosten', x=groups, y=cost_rates, text=[f'€{v:.2f}' for v in cost_rates], textposition='auto'),
        go.Bar(name='Vollkosten', x=groups, y=full_cost_rates, text=[f'€{v:.2f}' for v in full_cost_rates], textposition='auto'),
        go.Bar(name='Verkauf', x=groups, y=sales_rates, text=[f'€{v:.2f}' for v in sales_rates], textposition='auto')
    ])

    fig.update_layout(
        title="Stundensatzvergleich nach Mitarbeitergruppe",
        xaxis_title="Mitarbeitergruppe",
        yaxis_title="Stundensatz (€/h)",
        barmode='group',
        height=500,
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def create_cost_waterfall_chart(calculation_details: List[Dict], pricing_params: PricingParameters) -> go.Figure:
    """
    Create waterfall chart showing cost build-up from base cost to sales rate

    Args:
        calculation_details: List of calculation details per group
        pricing_params: Pricing parameters (profit, risk, discount)

    Returns:
        Plotly figure
    """
    # Use first group as example (or could show average)
    if not calculation_details:
        return None

    # Average across all groups for a representative view
    base_cost = sum(d['cost']['cost_rate'] for d in calculation_details) / len(calculation_details)
    overhead = sum(d['full_cost']['overhead_amount_per_hour'] for d in calculation_details) / len(calculation_details)
    full_cost = sum(d['full_cost']['full_cost_rate'] for d in calculation_details) / len(calculation_details)

    # Calculate profit, risk, discount amounts
    profit_amount = full_cost * (pricing_params.profit_margin_percent / 100)
    risk_amount = (full_cost + profit_amount) * (pricing_params.risk_surcharge_percent / 100)
    before_discount = full_cost + profit_amount + risk_amount
    discount_amount = before_discount * (pricing_params.discount_percent / 100)
    final_rate = before_discount - discount_amount

    # Create waterfall
    fig = go.Figure(go.Waterfall(
        name="Kostenaufbau",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=["Kosten-<br>stundensatz", "Gemein-<br>kosten", "Gewinn-<br>marge", "Risiko-<br>zuschlag", "Rabatt", "Verkaufs-<br>preis"],
        textposition="outside",
        text=[f"€{base_cost:.2f}", f"+€{overhead:.2f}",
              f"+€{profit_amount:.2f}", f"+€{risk_amount:.2f}", f"-€{discount_amount:.2f}", f"€{final_rate:.2f}"],
        y=[base_cost, overhead, profit_amount, risk_amount, -discount_amount, final_rate],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#2ecc71"}},
        decreasing={"marker": {"color": "#e74c3c"}},
        totals={"marker": {"color": "#3498db"}}
    ))

    fig.update_layout(
        title="Kostenaufbau: Von Basiskosten zum Verkaufspreis (Durchschnitt)",
        yaxis_title="Stundensatz (€/h)",
        showlegend=False,
        height=500,
        margin=dict(t=50, b=100)
    )

    return fig


def create_revenue_vs_cost_chart(plausibility: Dict) -> go.Figure:
    """
    Create chart comparing revenue vs costs with contribution margin

    Args:
        plausibility: Plausibility check data with financial metrics

    Returns:
        Plotly figure
    """
    personnel_cost = plausibility['total_personnel_cost']
    overhead_cost = plausibility['overhead_costs']
    total_cost = plausibility['total_cost']
    revenue = plausibility['total_revenue']
    contribution_margin = plausibility['contribution_margin']

    # Create stacked bar for costs
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Personalkosten',
        x=['Kosten', 'Umsatz'],
        y=[personnel_cost, 0],
        marker_color='#3498db',
        text=[f'€{personnel_cost:,.0f}', ''],
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        name='Gemeinkosten',
        x=['Kosten', 'Umsatz'],
        y=[overhead_cost, 0],
        marker_color='#9b59b6',
        text=[f'€{overhead_cost:,.0f}', ''],
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        name='Deckungsbeitrag',
        x=['Kosten', 'Umsatz'],
        y=[0, contribution_margin],
        marker_color='#2ecc71',
        text=['', f'€{contribution_margin:,.0f}'],
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        name='Gesamtkosten (Basis)',
        x=['Kosten', 'Umsatz'],
        y=[0, total_cost],
        marker_color='#95a5a6',
        text=['', f'€{total_cost:,.0f}'],
        textposition='inside',
        showlegend=True
    ))

    # Add contribution margin percentage as annotation
    fig.add_annotation(
        x=1,
        y=revenue + revenue * 0.05,
        text=f"Deckungsbeitrag: {plausibility['contribution_margin_percent']:.1f}%",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#2ecc71",
        font=dict(size=12, color="#2ecc71", family="Arial Black"),
        bgcolor="white",
        bordercolor="#2ecc71",
        borderwidth=2,
        borderpad=4
    )

    fig.update_layout(
        title="Gesamtkosten vs. Erwarteter Umsatz",
        yaxis_title="Betrag (€/Jahr)",
        barmode='stack',
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    return fig


def create_personnel_breakdown_chart(calculation_details: List[Dict]) -> go.Figure:
    """
    Create stacked horizontal bar showing personnel cost breakdown per group

    Args:
        calculation_details: List of calculation details per group

    Returns:
        Plotly figure
    """
    if not calculation_details:
        return None

    # Extract data
    groups = [d['group_name'] for d in calculation_details]
    base_salaries = [d['cost']['annual_salary_gross'] * d['cost']['employee_count']
                     for d in calculation_details]
    social_security = [d['cost']['social_security'] * d['cost']['employee_count']
                       for d in calculation_details]
    special_payments = [d['cost']['special_payments'] * d['cost']['employee_count']
                        for d in calculation_details]

    # Create chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Bruttogehalt',
        y=groups,
        x=base_salaries,
        orientation='h',
        marker_color='#3498db',
        text=[f'€{v:,.0f}' for v in base_salaries],
        textposition='inside',
        hovertemplate='<b>Bruttogehalt</b><br>€%{x:,.2f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Sozialversicherung',
        y=groups,
        x=social_security,
        orientation='h',
        marker_color='#e67e22',
        text=[f'€{v:,.0f}' for v in social_security],
        textposition='inside',
        hovertemplate='<b>Sozialversicherung</b><br>€%{x:,.2f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Sonderzahlungen',
        y=groups,
        x=special_payments,
        orientation='h',
        marker_color='#9b59b6',
        text=[f'€{v:,.0f}' for v in special_payments],
        textposition='inside',
        hovertemplate='<b>Sonderzahlungen</b><br>€%{x:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title="Personalkostenaufschlüsselung nach Gruppe",
        xaxis_title="Gesamtkosten pro Gruppe (€/Jahr)",
        yaxis_title="Mitarbeitergruppe",
        barmode='stack',
        height=max(400, len(groups) * 80),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='y unified'
    )

    return fig


def create_sensitivity_analysis_chart(calculation_details: List[Dict], pricing_params: PricingParameters,
                                       overhead_percent: float) -> go.Figure:
    """
    Create sensitivity analysis showing impact of parameter changes on sales rate

    Args:
        calculation_details: List of calculation details per group
        pricing_params: Current pricing parameters
        overhead_percent: Current overhead percentage

    Returns:
        Plotly figure
    """
    if not calculation_details:
        return None

    # Use average sales rate as baseline
    baseline_rate = sum(d['sales']['sales_rate'] for d in calculation_details) / len(calculation_details)
    base_full_cost = sum(d['full_cost']['full_cost_rate'] for d in calculation_details) / len(calculation_details)

    # Define parameter variations (-20% to +20%)
    variations = [-20, -10, 0, 10, 20]

    # Calculate impacts
    def calc_rate_with_profit(profit_delta):
        new_profit = pricing_params.profit_margin_percent + profit_delta
        profit_amount = base_full_cost * (new_profit / 100)
        risk_amount = (base_full_cost + profit_amount) * (pricing_params.risk_surcharge_percent / 100)
        before_discount = base_full_cost + profit_amount + risk_amount
        discount_amount = before_discount * (pricing_params.discount_percent / 100)
        return before_discount - discount_amount

    def calc_rate_with_overhead(overhead_delta):
        base_cost = sum(d['cost']['cost_rate'] for d in calculation_details) / len(calculation_details)
        new_overhead_percent = overhead_percent + overhead_delta
        new_overhead_amount = base_cost * (new_overhead_percent / 100)
        new_full_cost = base_cost + new_overhead_amount
        profit_amount = new_full_cost * (pricing_params.profit_margin_percent / 100)
        risk_amount = (new_full_cost + profit_amount) * (pricing_params.risk_surcharge_percent / 100)
        before_discount = new_full_cost + profit_amount + risk_amount
        discount_amount = before_discount * (pricing_params.discount_percent / 100)
        return before_discount - discount_amount

    def calc_rate_with_discount(discount_delta):
        new_discount = pricing_params.discount_percent + discount_delta
        profit_amount = base_full_cost * (pricing_params.profit_margin_percent / 100)
        risk_amount = (base_full_cost + profit_amount) * (pricing_params.risk_surcharge_percent / 100)
        before_discount = base_full_cost + profit_amount + risk_amount
        discount_amount = before_discount * (new_discount / 100)
        return before_discount - discount_amount

    profit_impacts = [calc_rate_with_profit(v) - baseline_rate for v in variations]
    overhead_impacts = [calc_rate_with_overhead(v) - baseline_rate for v in variations]
    discount_impacts = [calc_rate_with_discount(v) - baseline_rate for v in variations]

    # Create chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=variations,
        y=profit_impacts,
        mode='lines+markers',
        name='Gewinnmarge',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=variations,
        y=overhead_impacts,
        mode='lines+markers',
        name='Gemeinkosten',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8)
    ))

    fig.add_trace(go.Scatter(
        x=variations,
        y=discount_impacts,
        mode='lines+markers',
        name='Rabatt',
        line=dict(color='#f39c12', width=3),
        marker=dict(size=8)
    ))

    # Add horizontal line at zero
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title=f"Sensitivitätsanalyse: Auswirkung auf Verkaufspreis (Basis: €{baseline_rate:.2f}/h)",
        xaxis_title="Prozentuale Änderung des Parameters (%)",
        yaxis_title="Änderung des Verkaufspreises (€/h)",
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.15,
        showarrow=False,
        text="Hinweis: Zeigt wie sich ±20% Änderungen der Parameter auf den finalen Verkaufspreis auswirken",
        font=dict(size=10, color="gray"),
        xanchor="center"
    )

    return fig


# ============================================================================
# DATABASE IMPORT COMPONENTS
# ============================================================================

def render_apportion_mapping(available_apportion: List[str]) -> Dict[str, List[str]]:
    """
    Render UI for mapping data_invoice_position_apportion values to overhead cost categories.

    Args:
        available_apportion: List of unique apportion values from database

    Returns:
        Dictionary mapping overhead categories to selected apportion values
    """
    st.markdown("#### 🔗 Zuordnung: Datenbank → Kostenkategorien")
    st.markdown("Wählen Sie für jede Kostenkategorie, welche Datenbank-Zuordnungen (data_invoice_position_apportion) dazu gehören:")

    overhead_categories = {
        'office_costs': 'Bürokosten',
        'it_infrastructure': 'IT-Infrastruktur',
        'office_supplies': 'Büromaterial',
        'insurance': 'Versicherungen',
        'marketing': 'Marketing & Werbung',
        'administration': 'Verwaltung',
        'other': 'Sonstige Kosten'
    }

    mapping = {}

    # Create a multiselect for each overhead category
    for key, label in overhead_categories.items():
        mapping[key] = st.multiselect(
            label=label,
            options=available_apportion,
            default=st.session_state.get(f'apportion_mapping_{key}', []),
            key=f'apportion_mapping_{key}',
            help=f"Wählen Sie alle Datenbank-Zuordnungen, die zu '{label}' gehören"
        )

    # Show unmapped apportions as warning
    all_mapped = set()
    for apportions in mapping.values():
        all_mapped.update(apportions)

    unmapped = set(available_apportion) - all_mapped
    if unmapped:
        st.warning(f"⚠️ Nicht zugeordnete Werte: {', '.join(unmapped)}")
        st.info("Diese Werte werden bei der Zuordnung ignoriert. Sie können sie der Kategorie 'Sonstige Kosten' zuordnen.")

    return mapping
