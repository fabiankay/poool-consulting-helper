"""
Poool CRM API Client

A centralized API client for the Poool CRM that handles authentication,
base URL management, and common API operations.
"""

import requests
import pandas as pd
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse


class PooolAPIClient:
    """
    Centralized API client for Poool CRM operations.

    Handles environment management, authentication, and provides
    a clean interface for all API operations.
    """

    def __init__(self, api_key: str, environment: str = "production", custom_url: str = None):
        """
        Initialize the Poool API client.

        Args:
            api_key: API key for authentication
            environment: "production", "staging", or "custom"
            custom_url: Custom base URL when environment is "custom"
        """
        self.api_key = api_key
        self.environment = environment
        self.custom_url = custom_url
        self._base_url = self._get_base_url()
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _get_base_url(self) -> str:
        """Get the appropriate base URL for the configured environment."""
        if self.environment == "staging":
            return "https://staging-app.poool.rocks/api/2"
        elif self.environment == "custom" and self.custom_url:
            # Ensure custom URL ends with /api/2 if not already present
            if not self.custom_url.endswith('/api/2'):
                if self.custom_url.endswith('/'):
                    return f"{self.custom_url}api/2"
                else:
                    return f"{self.custom_url}/api/2"
            return self.custom_url
        else:  # production (default)
            return "https://app.poool.cc/api/2"

    @property
    def base_url(self) -> str:
        """Get the current base URL."""
        return self._base_url

    @property
    def environment_info(self) -> Dict[str, str]:
        """Get information about the current environment."""
        if self.environment == "production":
            return {"name": "Production", "display": "🟢 LIVE", "url": "app.poool.cc"}
        elif self.environment == "staging":
            return {"name": "Staging", "display": "🟡 TEST", "url": "staging-app.poool.rocks"}
        else:  # custom
            try:
                parsed = urlparse(self.custom_url or "")
                domain = parsed.netloc or self.custom_url or "Not configured"
            except:
                domain = self.custom_url or "Not configured"
            return {"name": "Custom", "display": "🔧 CUSTOM", "url": domain}

    def _handle_api_response(self, response: requests.Response, resource_type: str = "resource") -> Tuple[Optional[Dict], Optional[str]]:
        """Handle common API response patterns and errors."""
        if response.status_code in [200, 201]:
            data = response.json()
            return data.get('data', {}), None
        elif response.status_code == 400:
            try:
                error_data = response.json()
                if 'errors' in error_data:
                    errors = error_data['errors']
                    error_msgs = []
                    for field, msgs in errors.items():
                        error_msgs.append(f"{field}: {', '.join(msgs)}")
                    return None, f"Validation errors: {'; '.join(error_msgs)}"
                return None, f"Bad request: {error_data.get('message', 'Invalid data')}"
            except:
                return None, "Bad request: Invalid data format"
        elif response.status_code == 401:
            return None, "Authentication failed: Invalid or expired API key"
        elif response.status_code == 403:
            return None, f"Permission denied: Insufficient privileges to create {resource_type}s"
        elif response.status_code == 429:
            return None, "Rate limit exceeded: Please wait before retrying"
        elif response.status_code == 500:
            return None, "Server error: Please try again later"
        else:
            try:
                error_data = response.json()
                return None, f"API error ({response.status_code}): {error_data.get('message', 'Unknown error')}"
            except:
                return None, f"HTTP {response.status_code}: Unknown error"

    def test_connection(self) -> Tuple[bool, str]:
        """Test API connection by trying to fetch contact types."""
        try:
            response = requests.get(f"{self._base_url}/contact_types", headers=self._headers, timeout=10)

            if response.status_code == 200:
                return True, "Connection successful"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"API returned status {response.status_code}"

        except requests.exceptions.Timeout:
            return False, "Request timeout - please check your internet connection"
        except requests.exceptions.ConnectionError:
            return False, "Connection error - unable to reach Poool API"
        except requests.exceptions.HTTPError as e:
            return False, f"HTTP error: {str(e)}"
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def lookup_company_by_name(self, company_name: str) -> Tuple[Optional[int], Optional[str]]:
        """Look up a company ID by name."""
        try:
            if not company_name or not company_name.strip():
                return None, None

            # Search for companies by name
            params = {
                'search': company_name.strip(),
                'per_page': 5  # Limit results for performance
            }

            response = requests.get(f"{self._base_url}/companies",
                                  headers=self._headers,
                                  params=params,
                                  timeout=30)

            if response.status_code == 200:
                data = response.json()
                companies = data.get('data', [])

                # Look for exact name match (case insensitive)
                company_name_lower = company_name.lower()
                for company in companies:
                    if company.get('name', '').lower() == company_name_lower:
                        return company.get('id'), None

                # If no exact match, return the first partial match
                if companies:
                    return companies[0].get('id'), f"No exact match found, using closest match: {companies[0].get('name', 'Unknown')}"

                return None, f"No company found with name: {company_name}"

            elif response.status_code == 401:
                return None, "Authentication failed: Invalid API key"
            else:
                return None, f"Company lookup failed: HTTP {response.status_code}"

        except Exception as e:
            return None, f"Error looking up company: {str(e)}"

    def create_company(self, company_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Create a company via API."""
        try:
            # Add required type field and wrap in data object
            company_data["type"] = "company"
            payload = {"data": company_data}

            response = requests.post(f"{self._base_url}/companies",
                                   headers=self._headers,
                                   json=payload,
                                   timeout=30)

            return self._handle_api_response(response, "company")

        except Exception as e:
            return None, f"Error creating company: {str(e)}"

    def create_person(self, person_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Create a person via API."""
        try:
            # Wrap in data object (same pattern as companies)
            payload = {"data": person_data}

            response = requests.post(f"{self._base_url}/persons",
                                   headers=self._headers,
                                   json=payload,
                                   timeout=30)

            return self._handle_api_response(response, "person")

        except Exception as e:
            return None, f"Error creating person: {str(e)}"

    def get_all_tags(self) -> Tuple[Dict[str, int], Optional[str]]:
        """Retrieve all available tags and return name-to-ID mapping."""
        tag_mapping = {}
        page = 1

        try:
            while True:
                url = f"{self._base_url}/tags"
                params = {"page": page}

                response = requests.get(url, headers=self._headers, params=params)

                if response.status_code != 200:
                    return {}, f"Failed to fetch tags: {response.status_code} - {response.text}"

                data = response.json()
                tags = data.get('data', [])

                if not tags:
                    break

                # Extract tag name and ID from each tag
                for tag in tags:
                    tag_name = tag.get('title', '').strip()
                    tag_id = tag.get('id')

                    if tag_name and tag_id:
                        # Store both original case and lowercase for flexible lookup
                        tag_mapping[tag_name] = tag_id
                        tag_mapping[tag_name.lower()] = tag_id

                # Check if there are more pages
                links = data.get('links', {})
                if not links.get('next'):
                    break

                page += 1

        except Exception as e:
            return {}, f"Error fetching tags: {str(e)}"

        return tag_mapping, None

    def create_tag_if_missing(self, tag_name: str, color: str = "#007BFF", color_background: str = "#F8F9FA") -> Tuple[Optional[int], Optional[str]]:
        """Create a new tag if it doesn't exist, or return existing tag ID."""
        # First check if tag already exists
        existing_tags, error = self.get_all_tags()
        if error:
            return None, f"Failed to check existing tags: {error}"

        # Case-insensitive lookup
        if tag_name.lower() in existing_tags:
            return existing_tags[tag_name.lower()], None

        # Create new tag
        try:
            url = f"{self._base_url}/tags"

            tag_data = {
                "data": {
                    "title": tag_name.strip(),
                    "color": color,
                    "color_background": color_background,
                    "is_active": True,
                    "available_company": True,
                    "available_person": True,
                    "available_crm_lead": True,
                    "available_company_subsidiary": False,
                    "available_project": True,
                    "available_project_phase": True,
                    "available_asset": True,
                    "available_bill_incoming": False,
                    "available_bill": True,
                    "available_offer": True,
                    "available_order": False,
                    "available_ticket": True,
                    "available_ticket_job": True,
                    "available_ticket_qa": False,
                    "available_ticket_comment": True,
                    "available_check": False,
                    "available_purchase": True,
                    "pos": 999  # Put new tags at the end
                }
            }

            response = requests.post(url, headers=self._headers, json=tag_data)

            if response.status_code in [200, 201]:
                result = response.json()
                tag_id = result.get('data', {}).get('id')
                if tag_id:
                    return tag_id, None
                else:
                    return None, "Tag created but no ID returned"
            else:
                return None, f"Failed to create tag: {response.status_code} - {response.text}"

        except Exception as e:
            return None, f"Error creating tag: {str(e)}"

    def update_company(self, company_id: int, company_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Update a company via API."""
        try:
            # Add required type field and wrap in data object
            company_data["type"] = "company"
            payload = {"data": company_data}

            response = requests.put(f"{self._base_url}/companies/{company_id}",
                                   headers=self._headers,
                                   json=payload,
                                   timeout=30)

            return self._handle_api_response(response, "company")

        except Exception as e:
            return None, f"Error updating company: {str(e)}"

    def update_client(self, client_id: int, client_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Update client-specific data via API."""
        try:
            payload = {"data": client_data}

            response = requests.put(f"{self._base_url}/clients/{client_id}",
                                   headers=self._headers,
                                   json=payload,
                                   timeout=30)

            return self._handle_api_response(response, "client")

        except Exception as e:
            return None, f"Error updating client: {str(e)}"

    def update_supplier(self, supplier_id: int, supplier_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Update supplier-specific data via API."""
        try:
            payload = {"data": supplier_data}

            response = requests.put(f"{self._base_url}/suppliers/{supplier_id}",
                                   headers=self._headers,
                                   json=payload,
                                   timeout=30)

            return self._handle_api_response(response, "supplier")

        except Exception as e:
            return None, f"Error updating supplier: {str(e)}"

    def update_person(self, person_id: int, person_data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        """Update a person via API."""
        try:
            payload = {"data": person_data}

            response = requests.put(f"{self._base_url}/persons/{person_id}",
                                   headers=self._headers,
                                   json=payload,
                                   timeout=30)

            return self._handle_api_response(response, "person")

        except Exception as e:
            return None, f"Error updating person: {str(e)}"

    def get_company_by_id(self, company_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """Get a specific company by ID."""
        try:
            response = requests.get(f"{self._base_url}/companies/{company_id}",
                                   headers=self._headers,
                                   timeout=30)

            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}), None
            elif response.status_code == 404:
                return None, "Company not found"
            else:
                return None, f"Failed to get company: HTTP {response.status_code}"

        except Exception as e:
            return None, f"Error getting company: {str(e)}"

    def search_companies_by_field(self, field: str, value: str) -> Tuple[List[Dict], Optional[str]]:
        """Search for companies by a specific field value."""
        try:
            # Use search parameter for flexible searching
            params = {'search': value, 'per_page': 10}

            response = requests.get(f"{self._base_url}/companies",
                                  headers=self._headers,
                                  params=params,
                                  timeout=30)

            if response.status_code == 200:
                data = response.json()
                return data.get('data', []), None
            else:
                return [], f"Search failed: HTTP {response.status_code}"

        except Exception as e:
            return [], f"Error searching companies: {str(e)}"

    def get_person_by_id(self, person_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """Get a specific person by ID."""
        try:
            response = requests.get(f"{self._base_url}/persons/{person_id}",
                                   headers=self._headers,
                                   timeout=30)

            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}), None
            elif response.status_code == 404:
                return None, "Person not found"
            else:
                return None, f"Failed to get person: HTTP {response.status_code}"

        except Exception as e:
            return None, f"Error getting person: {str(e)}"

    def search_persons_by_field(self, field: str, value: str) -> Tuple[List[Dict], Optional[str]]:
        """Search for persons by a specific field value."""
        try:
            # Use search parameter for flexible searching
            params = {'search': value, 'per_page': 10}

            response = requests.get(f"{self._base_url}/persons",
                                  headers=self._headers,
                                  params=params,
                                  timeout=30)

            if response.status_code == 200:
                data = response.json()
                return data.get('data', []), None
            else:
                return [], f"Search failed: HTTP {response.status_code}"

        except Exception as e:
            return [], f"Error searching persons: {str(e)}"

    def __str__(self) -> str:
        """String representation of the API client."""
        env_info = self.environment_info
        return f"PooolAPIClient({env_info['name']} - {env_info['url']})"

    def __repr__(self) -> str:
        """Detailed representation of the API client."""
        return f"PooolAPIClient(environment='{self.environment}', base_url='{self._base_url}')"