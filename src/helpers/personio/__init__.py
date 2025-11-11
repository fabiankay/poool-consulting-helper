"""
Personio helper functions and API client.

Provides centralized API client and helper functions for interacting with the Personio HR API.
"""

from .api_client import PersonioAPIClient
from .helpers import (
    create_personio_client,
    get_employees,
    get_absences,
    get_attendances,
    process_employees_data,
    process_absences_data,
    process_attendances_data,
)

__all__ = [
    'PersonioAPIClient',
    'create_personio_client',
    'get_employees',
    'get_absences',
    'get_attendances',
    'process_employees_data',
    'process_absences_data',
    'process_attendances_data',
]
