"""
Personio API Client

A centralized API client for the Personio HR API that handles OAuth2 authentication,
token management, pagination, and common API operations.
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class PersonioAPIClient:
    """
    Centralized API client for Personio HR API operations.

    Handles OAuth2 authentication, token management, pagination,
    and provides a clean interface for all API operations.
    """

    BASE_URL = "https://api.personio.de"
    AUTH_URL = f"{BASE_URL}/v2/auth/token"
    API_V1_URL = f"{BASE_URL}/v1"

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize the Personio API client.

        Args:
            client_id: Personio API Client ID
            client_secret: Personio API Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None

    def authenticate(self) -> Tuple[Optional[str], Optional[datetime], Optional[str]]:
        """
        Obtain access token from Personio API using OAuth2 client credentials flow.

        Returns:
            Tuple of (access_token, expires_at, error)
        """
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            response = requests.post(self.AUTH_URL, headers=headers, data=data)
            response.raise_for_status()

            token_data = response.json()
            access_token = token_data.get('access_token')
            expires_in = token_data.get('expires_in', 3600)  # Default to 1 hour

            # Calculate expiration time (subtract 60s for safety margin)
            expires_at = datetime.now() + timedelta(seconds=expires_in - 60)

            # Store token internally
            self.access_token = access_token
            self.token_expires_at = expires_at

            return access_token, expires_at, None

        except requests.exceptions.RequestException as e:
            return None, None, f"API-Anfrage fehlgeschlagen: {str(e)}"
        except Exception as e:
            return None, None, f"Unerwarteter Fehler: {str(e)}"

    def is_token_valid(self) -> bool:
        """Check if the current access token is still valid."""
        if not self.access_token or not self.token_expires_at:
            return False
        return datetime.now() < self.token_expires_at

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests with current access token."""
        return {
            'accept': 'application/json',
            'authorization': f'Bearer {self.access_token}'
        }

    def _make_paginated_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        limit: int = 200
    ) -> Tuple[Optional[List], Optional[str]]:
        """
        Make a paginated GET request to Personio API.

        Args:
            endpoint: API endpoint path (e.g., '/company/employees')
            params: Optional query parameters (excluding limit/offset)
            limit: Number of records per page (default 200)

        Returns:
            Tuple of (all_records, error)
        """
        if not self.is_token_valid():
            return None, "Token ist ungültig oder abgelaufen. Bitte authentifizieren Sie sich zuerst."

        url = f"{self.API_V1_URL}{endpoint}"
        headers = self._get_headers()
        all_records = []
        offset = 0

        # Prepare base parameters
        if params is None:
            params = {}

        try:
            while True:
                # Add pagination parameters
                page_params = {**params, 'limit': limit, 'offset': offset}

                response = requests.get(url, headers=headers, params=page_params)
                response.raise_for_status()

                data = response.json()
                records = data.get('data', [])

                if not records:
                    break

                all_records.extend(records)

                # Check if there are more pages
                if len(records) < limit:
                    break

                offset += limit

            return all_records, None

        except requests.exceptions.RequestException as e:
            return None, f"API-Anfrage fehlgeschlagen: {str(e)}"
        except Exception as e:
            return None, f"Unerwarteter Fehler: {str(e)}"

    def get_employees(self) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Retrieve all employees from Personio API with automatic pagination.

        Returns:
            Tuple of (employees_data, error) where employees_data is {'data': [employees]}
        """
        records, error = self._make_paginated_request('/company/employees')

        if error:
            return None, error

        return {'data': records}, None

    def get_absences(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Retrieve all absences (time-offs) from Personio API with automatic pagination.

        Args:
            start_date: Optional start date in YYYY-MM-DD format
            end_date: Optional end date in YYYY-MM-DD format

        Returns:
            Tuple of (absences_data, error) where absences_data is {'data': [absences]}
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        records, error = self._make_paginated_request('/company/time-offs', params)

        if error:
            return None, error

        return {'data': records}, None

    def get_attendances(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Retrieve all attendances from Personio API with automatic pagination.

        Args:
            start_date: Optional start date in YYYY-MM-DD format
            end_date: Optional end date in YYYY-MM-DD format

        Returns:
            Tuple of (attendances_data, error) where attendances_data is {'data': [attendances]}
        """
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date

        records, error = self._make_paginated_request('/company/attendances', params)

        if error:
            return None, error

        return {'data': records}, None
