"""
Hourly Rate Calculator - Business Logic for Hourly Rate Calculations

This module provides the core calculation logic for determining hourly rates
for consulting/service businesses in Germany.
"""

from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import pandas as pd


# ============================================================================
# PYDANTIC DATA MODELS
# ============================================================================

class EmployeeGroup(BaseModel):
    """Employee group configuration for hourly rate calculation"""

    name: str = Field(..., min_length=1, description="Name of employee group")
    count: int = Field(..., gt=0, description="Number of employees")
    annual_salary_gross: float = Field(..., gt=0, description="Average annual gross salary in €")
    social_security_percent: float = Field(20.0, ge=0, le=100, description="Employer social security contribution in %")
    special_payments: float = Field(0.0, ge=0, description="Special payments (bonus, vacation/Christmas bonus) in €")
    vacation_days: int = Field(30, ge=0, le=365, description="Vacation days per year")
    sick_days_average: int = Field(10, ge=0, le=365, description="Average sick days per year")
    productivity_percent: float = Field(75.0, ge=0, le=100, description="Productivity in % (time for billable projects)")

    @field_validator('productivity_percent')
    @classmethod
    def validate_productivity(cls, v: float) -> float:
        """Validate productivity percentage is in reasonable range"""
        if v < 30 or v > 95:
            raise ValueError('Produktivität sollte zwischen 30% und 95% liegen')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Junior Developer",
                "count": 3,
                "annual_salary_gross": 50000,
                "social_security_percent": 20.0,
                "special_payments": 5000,
                "vacation_days": 30,
                "sick_days_average": 10,
                "productivity_percent": 75.0
            }
        }


class OverheadCosts(BaseModel):
    """Overhead costs for the business"""

    office_costs: float = Field(0.0, ge=0, description="Office/rent costs in € per year")
    it_infrastructure: float = Field(0.0, ge=0, description="IT infrastructure in € per year")
    office_supplies: float = Field(0.0, ge=0, description="Office supplies in € per year")
    insurance: float = Field(0.0, ge=0, description="Insurance in € per year")
    marketing: float = Field(0.0, ge=0, description="Marketing & sales in € per year")
    administration: float = Field(0.0, ge=0, description="Administration costs in € per year")
    other: float = Field(0.0, ge=0, description="Other overhead costs in € per year")

    def total(self) -> float:
        """Calculate total overhead costs"""
        return sum([
            self.office_costs,
            self.it_infrastructure,
            self.office_supplies,
            self.insurance,
            self.marketing,
            self.administration,
            self.other
        ])

    def as_dict(self) -> Dict[str, float]:
        """Return overhead costs as dictionary for display"""
        return {
            "Raumkosten": self.office_costs,
            "IT-Infrastruktur": self.it_infrastructure,
            "Büromaterial": self.office_supplies,
            "Versicherungen": self.insurance,
            "Marketing": self.marketing,
            "Verwaltung": self.administration,
            "Sonstige": self.other
        }


class PricingParameters(BaseModel):
    """Calculation parameters for pricing"""

    profit_margin_percent: float = Field(20.0, ge=0, le=200, description="Profit margin in %")
    risk_surcharge_percent: float = Field(5.0, ge=0, le=50, description="Risk surcharge in %")
    discount_percent: float = Field(0.0, ge=0, le=50, description="Discount in %")

    @field_validator('discount_percent')
    @classmethod
    def validate_discount(cls, v: float, info) -> float:
        """Validate discount doesn't exceed reasonable limits"""
        if v > 40:
            raise ValueError('Rabatt sollte 40% nicht überschreiten')
        return v


# ============================================================================
# CALCULATOR CLASS
# ============================================================================

class HourlyRateCalculator:
    """
    Calculator for hourly rate calculations

    Implements the standard German hourly rate calculation methodology:
    1. Calculate productive hours per employee
    2. Calculate cost per hour (personnel costs)
    3. Add overhead surcharge
    4. Add profit margin, risk surcharge, and discount
    """

    def __init__(self, working_days_per_year: int = 251, hours_per_day: float = 8.0):
        """
        Initialize calculator with working days configuration

        Args:
            working_days_per_year: Working days per year (default: 251 for Germany 2025)
            hours_per_day: Working hours per day (default: 8.0)
        """
        self.working_days_per_year = working_days_per_year
        self.hours_per_day = hours_per_day

    def calculate_productive_hours(self, group: EmployeeGroup) -> Dict:
        """
        Calculate productive hours per employee per year

        Formula:
        1. Attendance days = Working days - Vacation - Sick days
        2. Attendance hours = Attendance days × Hours/day
        3. Productive hours = Attendance hours × Productivity%

        Args:
            group: Employee group configuration

        Returns:
            Dictionary with breakdown of calculations
        """
        attendance_days = (
            self.working_days_per_year
            - group.vacation_days
            - group.sick_days_average
        )

        attendance_hours = attendance_days * self.hours_per_day

        productive_hours = attendance_hours * (group.productivity_percent / 100)

        return {
            'total_working_days': self.working_days_per_year,
            'vacation_days': group.vacation_days,
            'sick_days': group.sick_days_average,
            'attendance_days': attendance_days,
            'hours_per_day': self.hours_per_day,
            'attendance_hours': attendance_hours,
            'productivity_percent': group.productivity_percent,
            'productive_hours': productive_hours
        }

    def calculate_cost_rate(
        self,
        group: EmployeeGroup,
        productive_hours: float
    ) -> Dict:
        """
        Calculate cost per hour (personnel costs only)

        Formula:
        1. Personnel costs = Salary + Social security + Special payments
        2. Cost rate = Personnel costs / Productive hours

        Args:
            group: Employee group configuration
            productive_hours: Productive hours per employee per year

        Returns:
            Dictionary with cost breakdown
        """
        social_security = group.annual_salary_gross * (group.social_security_percent / 100)

        personnel_cost_per_employee = (
            group.annual_salary_gross
            + social_security
            + group.special_payments
        )

        total_personnel_cost = personnel_cost_per_employee * group.count

        if productive_hours == 0:
            raise ValueError(
                f"Produktive Stunden können nicht 0 sein. "
                f"Prüfen Sie Urlaubstage, Krankheitstage und Produktivität für Gruppe '{group.name}'"
            )

        cost_rate = personnel_cost_per_employee / productive_hours

        return {
            'annual_salary_gross': group.annual_salary_gross,
            'social_security': social_security,
            'social_security_percent': group.social_security_percent,
            'special_payments': group.special_payments,
            'personnel_cost_per_employee': personnel_cost_per_employee,
            'employee_count': group.count,
            'total_personnel_cost': total_personnel_cost,
            'productive_hours': productive_hours,
            'cost_rate': cost_rate
        }

    def calculate_overhead_surcharge(
        self,
        groups: List[EmployeeGroup],
        overhead: OverheadCosts
    ) -> Tuple[float, Dict]:
        """
        Calculate overhead surcharge percentage

        Formula:
        Overhead surcharge % = (Total overhead / Total personnel costs) × 100

        Args:
            groups: List of all employee groups
            overhead: Overhead costs

        Returns:
            Tuple of (surcharge_percent, breakdown_dict)
        """
        # Calculate total personnel costs
        total_personnel_cost = 0.0
        for group in groups:
            productive_hours = self.calculate_productive_hours(group)['productive_hours']
            cost_breakdown = self.calculate_cost_rate(group, productive_hours)
            total_personnel_cost += cost_breakdown['total_personnel_cost']

        overhead_total = overhead.total()

        if total_personnel_cost == 0:
            overhead_surcharge_percent = 0.0
        else:
            overhead_surcharge_percent = (overhead_total / total_personnel_cost) * 100

        return overhead_surcharge_percent, {
            'overhead_total': overhead_total,
            'total_personnel_cost': total_personnel_cost,
            'overhead_surcharge_percent': overhead_surcharge_percent
        }

    def calculate_full_cost_rate(
        self,
        cost_rate: float,
        overhead_surcharge_percent: float
    ) -> Dict:
        """
        Calculate full cost per hour including overhead

        Formula:
        Full cost = Cost rate × (1 + Overhead surcharge %)

        Args:
            cost_rate: Base cost per hour
            overhead_surcharge_percent: Overhead surcharge percentage

        Returns:
            Dictionary with calculation breakdown
        """
        overhead_amount = cost_rate * (overhead_surcharge_percent / 100)
        full_cost_rate = cost_rate + overhead_amount

        return {
            'cost_rate': cost_rate,
            'overhead_surcharge_percent': overhead_surcharge_percent,
            'overhead_amount_per_hour': overhead_amount,
            'full_cost_rate': full_cost_rate
        }

    def calculate_sales_rate(
        self,
        full_cost_rate: float,
        params: PricingParameters
    ) -> Dict:
        """
        Calculate final sales price per hour

        Formula:
        1. After profit = Full cost × (1 + Profit margin %)
        2. After risk = After profit × (1 + Risk %)
        3. Sales price = After risk × (1 - Discount %)

        Args:
            full_cost_rate: Full cost per hour
            params: Pricing parameters

        Returns:
            Dictionary with step-by-step calculation
        """
        after_profit = full_cost_rate * (1 + params.profit_margin_percent / 100)
        profit_amount = after_profit - full_cost_rate

        after_risk = after_profit * (1 + params.risk_surcharge_percent / 100)
        risk_amount = after_risk - after_profit

        sales_rate = after_risk * (1 - params.discount_percent / 100)
        discount_amount = after_risk - sales_rate

        return {
            'full_cost_rate': full_cost_rate,
            'profit_margin_percent': params.profit_margin_percent,
            'profit_amount': profit_amount,
            'after_profit': after_profit,
            'risk_surcharge_percent': params.risk_surcharge_percent,
            'risk_amount': risk_amount,
            'after_risk': after_risk,
            'discount_percent': params.discount_percent,
            'discount_amount': discount_amount,
            'sales_rate': sales_rate
        }

    def calculate_group_complete(
        self,
        group: EmployeeGroup,
        overhead_surcharge_percent: float,
        params: PricingParameters
    ) -> Dict:
        """
        Complete calculation for one employee group

        Args:
            group: Employee group
            overhead_surcharge_percent: Overhead surcharge percentage
            params: Pricing parameters

        Returns:
            Dictionary with all calculation steps
        """
        # Step 1: Productive hours
        productive_breakdown = self.calculate_productive_hours(group)

        # Step 2: Cost per hour
        cost_breakdown = self.calculate_cost_rate(
            group,
            productive_breakdown['productive_hours']
        )

        # Step 3: Full cost per hour
        full_cost_breakdown = self.calculate_full_cost_rate(
            cost_breakdown['cost_rate'],
            overhead_surcharge_percent
        )

        # Step 4: Sales price per hour
        sales_breakdown = self.calculate_sales_rate(
            full_cost_breakdown['full_cost_rate'],
            params
        )

        return {
            'group_name': group.name,
            'employee_count': group.count,
            'productive_hours': productive_breakdown,
            'cost': cost_breakdown,
            'full_cost': full_cost_breakdown,
            'sales': sales_breakdown
        }

    def calculate_all_groups(
        self,
        groups: List[EmployeeGroup],
        overhead: OverheadCosts,
        params: PricingParameters
    ) -> pd.DataFrame:
        """
        Calculate hourly rates for all employee groups

        Args:
            groups: List of employee groups
            overhead: Overhead costs
            params: Pricing parameters

        Returns:
            DataFrame with results for all groups
        """
        # First calculate overhead surcharge
        overhead_surcharge_percent, _ = self.calculate_overhead_surcharge(groups, overhead)

        # Calculate for each group
        results = []
        for group in groups:
            breakdown = self.calculate_group_complete(group, overhead_surcharge_percent, params)

            results.append({
                'Mitarbeitergruppe': group.name,
                'Anzahl MA': group.count,
                'Produktive Std./Jahr': breakdown['productive_hours']['productive_hours'],
                'Kostenstundensatz (€/h)': breakdown['cost']['cost_rate'],
                'Vollkostensatz (€/h)': breakdown['full_cost']['full_cost_rate'],
                'Verkaufsstundensatz (€/h)': breakdown['sales']['sales_rate'],
                'Personalkosten gesamt (€/Jahr)': breakdown['cost']['total_personnel_cost'],
                'Erwarteter Umsatz (€/Jahr)': (
                    breakdown['sales']['sales_rate']
                    * breakdown['productive_hours']['productive_hours']
                    * group.count
                )
            })

        return pd.DataFrame(results)

    def calculate_plausibility(
        self,
        df: pd.DataFrame,
        overhead_total: float
    ) -> Dict:
        """
        Calculate plausibility checks and KPIs

        Args:
            df: Results DataFrame from calculate_all_groups
            overhead_total: Total overhead costs

        Returns:
            Dictionary with KPIs and warnings
        """
        total_personnel_cost = df['Personalkosten gesamt (€/Jahr)'].sum()
        total_revenue = df['Erwarteter Umsatz (€/Jahr)'].sum()
        total_cost = total_personnel_cost + overhead_total

        contribution_margin = total_revenue - total_cost
        contribution_margin_percent = (contribution_margin / total_revenue * 100) if total_revenue > 0 else 0

        warnings = []
        if contribution_margin < 0:
            warnings.append("⚠️ WARNUNG: Negativer Deckungsbeitrag! Kosten übersteigen Umsatz.")
        if contribution_margin_percent < 10:
            warnings.append("⚠️ WARNUNG: Sehr geringe Marge! Prüfen Sie Ihre Kalkulation.")

        return {
            'total_personnel_cost': total_personnel_cost,
            'overhead_costs': overhead_total,
            'total_cost': total_cost,
            'total_revenue': total_revenue,
            'contribution_margin': contribution_margin,
            'contribution_margin_percent': contribution_margin_percent,
            'warnings': warnings
        }
