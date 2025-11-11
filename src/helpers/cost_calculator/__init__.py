"""
Cost Calculator (Stundensatzkalkulation)

Systematic calculation of cost and sales hourly rates for consulting and service businesses.
"""

from .calculator import (
    EmployeeGroup,
    OverheadCosts,
    PricingParameters,
    HourlyRateCalculator,
)

from .export import (
    export_to_excel,
    export_to_json,
)

__all__ = [
    # Models
    'EmployeeGroup',
    'OverheadCosts',
    'PricingParameters',

    # Calculator
    'HourlyRateCalculator',

    # Export functions
    'export_to_excel',
    'export_to_json',
]
