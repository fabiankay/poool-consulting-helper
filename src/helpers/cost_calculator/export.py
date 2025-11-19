"""
Hourly Rate Export Utilities

Export calculation results to various formats (Excel, JSON)
"""

import pandas as pd
import json
from io import BytesIO
from typing import Dict, List
from datetime import datetime


def export_to_excel(
    df_results: pd.DataFrame,
    calculation_details: List[Dict],
    basic_params: Dict,
    overhead_total: float,
    plausibility: Dict
) -> BytesIO:
    """
    Export calculation results to Excel file

    Args:
        df_results: Results DataFrame from calculator
        calculation_details: List of complete breakdowns for each group
        basic_params: Basic parameters (year, working days, etc.)
        overhead_total: Total overhead costs
        plausibility: Plausibility checks and KPIs

    Returns:
        BytesIO object containing Excel file
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter', engine_kwargs={'options': {'nan_inf_to_errors': True}}) as writer:
        workbook = writer.book

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#3199c6',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })

        currency_format = workbook.add_format({
            'num_format': '#,##0.00 €',
            'align': 'right'
        })

        percent_format = workbook.add_format({
            'num_format': '0.0%',
            'align': 'right'
        })

        number_format = workbook.add_format({
            'num_format': '#,##0',
            'align': 'right'
        })

        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'left'
        })

        # ===== Sheet 1: Overview =====
        df_results.to_excel(writer, sheet_name='Übersicht', index=False, startrow=3)
        worksheet_overview = writer.sheets['Übersicht']

        # Add title
        worksheet_overview.write('A1', 'Stundensatzkalkulation - Übersicht', title_format)
        worksheet_overview.write('A2', f"Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

        # Format columns
        worksheet_overview.set_column('A:A', 25)  # Mitarbeitergruppe
        worksheet_overview.set_column('B:B', 12)  # Anzahl MA
        worksheet_overview.set_column('C:C', 20)  # Produktive Std.
        worksheet_overview.set_column('D:G', 22)  # Currency columns

        # Apply header format
        for col_num, value in enumerate(df_results.columns.values):
            worksheet_overview.write(3, col_num, value, header_format)

        # Apply number/currency formats to data
        start_row = 4
        for row in range(len(df_results)):
            worksheet_overview.write(start_row + row, 1, df_results.iloc[row]['Anzahl MA'], number_format)

        # ===== Sheet 2: KPIs =====
        kpi_data = [
            ['Kennzahl', 'Wert'],
            ['Geschäftsjahr', basic_params['fiscal_year']],
            ['Arbeitstage pro Jahr', basic_params['working_days_per_year']],
            ['Stunden pro Tag', basic_params['hours_per_day']],
            [''],
            ['Personalkosten gesamt', plausibility['total_personnel_cost']],
            ['Gemeinkosten gesamt', plausibility['overhead_costs']],
            ['Gesamtkosten', plausibility['total_cost']],
            [''],
            ['Erwarteter Jahresumsatz', plausibility['total_revenue']],
            ['Deckungsbeitrag', plausibility['contribution_margin']],
            ['Deckungsbeitrag %', plausibility['contribution_margin_percent'] / 100],
        ]

        df_kpi = pd.DataFrame(kpi_data[1:], columns=kpi_data[0])
        df_kpi.to_excel(writer, sheet_name='Kennzahlen', index=False)
        worksheet_kpi = writer.sheets['Kennzahlen']

        # Format
        worksheet_kpi.set_column('A:A', 30)
        worksheet_kpi.set_column('B:B', 20)
        worksheet_kpi.write('A1', 'Kennzahl', header_format)
        worksheet_kpi.write('B1', 'Wert', header_format)

        # Apply currency format to currency rows
        # Note: df_kpi has indices 0-10 (11 rows), since we excluded the header with kpi_data[1:]
        # Original kpi_data rows: 5,6,7,9,10 -> df_kpi rows: 4,5,6,8,9
        for row_idx in [4, 5, 6, 8, 9]:
            worksheet_kpi.write(row_idx + 1, 1, df_kpi.iloc[row_idx]['Wert'], currency_format)

        # Apply percent format to percent row (original row 11 -> df_kpi row 10)
        worksheet_kpi.write(10 + 1, 1, df_kpi.iloc[10]['Wert'], percent_format)

        # ===== Sheet 3: Details per Group =====
        for idx, detail in enumerate(calculation_details):
            sheet_name = f"Details_{idx + 1}"[:31]  # Excel sheet name limit

            # Prepare detailed data
            group_name = detail['group_name']
            prod = detail['productive_hours']
            cost = detail['cost']
            full = detail['full_cost']
            sales = detail['sales']

            detail_data = [
                ['Mitarbeitergruppe', group_name],
                ['Anzahl Mitarbeiter', detail['employee_count']],
                [''],
                ['SCHRITT 1: PRODUKTIVE STUNDEN', ''],
                ['Arbeitstage pro Jahr', prod['total_working_days']],
                ['- Urlaubstage', prod['vacation_days']],
                ['- Krankheitstage', prod['sick_days']],
                ['= Anwesenheitstage', prod['attendance_days']],
                ['× Stunden pro Tag', prod['hours_per_day']],
                ['= Anwesenheitsstunden', prod['attendance_hours']],
                ['× Produktivität %', prod['productivity_percent'] / 100],
                ['= Produktive Stunden', prod['productive_hours']],
                [''],
                ['SCHRITT 2: KOSTENSTUNDENSATZ', ''],
                ['Jahresgehalt brutto', cost['annual_salary_gross']],
                ['+ Sozialversicherung AG-Anteil', cost['social_security']],
                ['+ Sonderzahlungen', cost['special_payments']],
                ['= Personalkosten pro MA', cost['personnel_cost_per_employee']],
                ['÷ Produktive Stunden', prod['productive_hours']],
                ['= Kostenstundensatz', cost['cost_rate']],
                [''],
                ['SCHRITT 3: VOLLKOSTENSTUNDENSATZ', ''],
                ['Kostenstundensatz', full['cost_rate']],
                ['+ Gemeinkostenzuschlag %', full['overhead_surcharge_percent'] / 100],
                ['= Gemeinkostenbetrag', full['overhead_amount_per_hour']],
                ['= Vollkostenstundensatz', full['full_cost_rate']],
                [''],
                ['SCHRITT 4: VERKAUFSSTUNDENSATZ', ''],
                ['Vollkostenstundensatz', sales['full_cost_rate']],
                ['+ Gewinnmarge %', sales['profit_margin_percent'] / 100],
                ['= Nach Gewinn', sales['after_profit']],
                ['+ Risikoaufschlag %', sales['risk_surcharge_percent'] / 100],
                ['= Nach Risiko', sales['after_risk']],
                ['- Rabatt %', sales['discount_percent'] / 100],
                ['= VERKAUFSSTUNDENSATZ', sales['sales_rate']],
            ]

            df_detail = pd.DataFrame(detail_data, columns=['Position', 'Wert'])
            df_detail.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet_detail = writer.sheets[sheet_name]

            # Format
            worksheet_detail.set_column('A:A', 35)
            worksheet_detail.set_column('B:B', 20)
            worksheet_detail.write('A1', 'Position', header_format)
            worksheet_detail.write('B1', 'Wert', header_format)

            # Apply currency/percent formats to appropriate rows
            for row_idx, row_data in enumerate(detail_data):
                if 'SCHRITT' in str(row_data[0]) or row_data[0] == 'Mitarbeitergruppe':
                    # Bold format for headers
                    worksheet_detail.write(row_idx + 1, 0, row_data[0], title_format)
                elif '%' in str(row_data[0]):
                    # Percent format
                    if isinstance(row_data[1], (int, float)):
                        worksheet_detail.write(row_idx + 1, 1, row_data[1], percent_format)
                elif any(keyword in str(row_data[0]) for keyword in ['kosten', 'Gehalt', 'Sonderzahlung', 'satz', 'SATZ', 'Gewinn', 'Risiko', 'Betrag']):
                    # Currency format
                    if isinstance(row_data[1], (int, float)):
                        worksheet_detail.write(row_idx + 1, 1, row_data[1], currency_format)
                elif isinstance(row_data[1], (int, float)) and row_data[0] not in ['', 'Anzahl Mitarbeiter']:
                    # Number format
                    worksheet_detail.write(row_idx + 1, 1, row_data[1], number_format)

    output.seek(0)
    return output


def export_to_json(
    df_results: pd.DataFrame,
    calculation_details: List[Dict],
    basic_params: Dict,
    overhead_dict: Dict,
    pricing_params_dict: Dict,
    plausibility: Dict
) -> str:
    """
    Export calculation results to JSON

    Args:
        df_results: Results DataFrame
        calculation_details: List of complete breakdowns
        basic_params: Basic parameters
        overhead_dict: Overhead costs as dict
        pricing_params_dict: Pricing parameters as dict
        plausibility: KPIs

    Returns:
        JSON string
    """
    export_data = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'version': '1.0'
        },
        'basic_parameters': basic_params,
        'overhead_costs': overhead_dict,
        'pricing_parameters': pricing_params_dict,
        'results': {
            'overview': df_results.to_dict(orient='records'),
            'details_per_group': calculation_details,
            'plausibility': plausibility
        }
    }

    return json.dumps(export_data, indent=2, ensure_ascii=False)
