"""
Credential Manager

Centralized credential storage and management for multiple API integrations.
Provides type-safe access to credentials, connection validation, and status tracking.
"""

import streamlit as st
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Tuple
from datetime import datetime
from enum import Enum


class CredentialType(Enum):
    """Types of credentials supported by the system."""
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    DATABASE = "database"
    CUSTOM = "custom"


class CredentialScope(Enum):
    """Scope of credential storage."""
    GLOBAL = "global"  # Shared across all pages (e.g., CRM)
    PAGE_LOCAL = "page_local"  # Specific to one page (e.g., Personio)


@dataclass
class APIConfig:
    """Configuration for an API integration."""
    name: str
    display_name: str
    credential_type: CredentialType
    scope: CredentialScope
    has_environment: bool = False  # Supports prod/staging/custom
    environment_options: List[str] = field(default_factory=lambda: ['production', 'staging', 'custom'])
    default_environment: str = 'production'
    validator_func: Optional[Callable] = None  # Function to validate/test connection
    credential_fields: List[str] = field(default_factory=list)  # Required credential fields


@dataclass
class ConnectionStatus:
    """Status of an API connection."""
    is_configured: bool = False
    is_tested: bool = False
    is_connected: bool = False
    last_tested: Optional[datetime] = None
    error_message: Optional[str] = None


class CredentialManager:
    """
    Singleton credential manager for centralized credential storage and access.

    Manages all API credentials across the application, providing type-safe access
    and automatic session state management.
    """

    _instance = None
    _initialized = False

    def __new__(cls):
        """Singleton pattern - only one instance per session."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize credential manager (only once per session)."""
        # Always ensure session state is initialized
        self._init_session_state()

        if not CredentialManager._initialized:
            self._apis: Dict[str, APIConfig] = {}
            CredentialManager._initialized = True

    def _init_session_state(self):
        """Initialize session state for credential storage."""
        # Always check and initialize session state, regardless of class initialization status
        if '_credential_store' not in st.session_state:
            st.session_state._credential_store = {}

        if '_connection_status' not in st.session_state:
            st.session_state._connection_status = {}

        if '_credential_clients' not in st.session_state:
            st.session_state._credential_clients = {}  # For OAuth2 client objects, etc.

    def register_api(self,
                    name: str,
                    display_name: str,
                    credential_type: CredentialType,
                    scope: CredentialScope = CredentialScope.GLOBAL,
                    has_environment: bool = False,
                    environment_options: Optional[List[str]] = None,
                    default_environment: str = 'production',
                    validator_func: Optional[Callable] = None,
                    credential_fields: Optional[List[str]] = None) -> None:
        """
        Register an API integration with the credential manager.

        Args:
            name: Internal API name (e.g., 'poool_crm', 'personio')
            display_name: Display name for UI (e.g., 'Poool CRM API')
            credential_type: Type of credentials required
            scope: Whether credentials are global or page-local
            has_environment: Whether this API supports environment selection
            environment_options: List of available environments
            default_environment: Default environment to use
            validator_func: Function to test connection (returns (success, message))
            credential_fields: List of required credential field names
        """
        config = APIConfig(
            name=name,
            display_name=display_name,
            credential_type=credential_type,
            scope=scope,
            has_environment=has_environment,
            environment_options=environment_options or ['production', 'staging', 'custom'],
            default_environment=default_environment,
            validator_func=validator_func,
            credential_fields=credential_fields or []
        )

        self._apis[name] = config

        # Initialize storage and status for this API
        if name not in st.session_state._credential_store:
            st.session_state._credential_store[name] = {}

        if name not in st.session_state._connection_status:
            st.session_state._connection_status[name] = ConnectionStatus()

    def set_credentials(self, api_name: str, **credentials) -> None:
        """
        Set credentials for an API.

        Args:
            api_name: Name of the API
            **credentials: Credential key-value pairs (e.g., api_key='xxx', environment='production')
        """
        if api_name not in self._apis:
            raise ValueError(f"API '{api_name}' not registered. Call register_api() first.")

        st.session_state._credential_store[api_name].update(credentials)

        # Update status
        status = st.session_state._connection_status[api_name]
        status.is_configured = bool(credentials)
        status.is_tested = False  # Reset test status when credentials change
        status.is_connected = False

    def get_credentials(self, api_name: str) -> Dict[str, Any]:
        """
        Get credentials for an API.

        Args:
            api_name: Name of the API

        Returns:
            Dictionary of credential key-value pairs
        """
        if api_name not in self._apis:
            raise ValueError(f"API '{api_name}' not registered.")

        return st.session_state._credential_store.get(api_name, {}).copy()

    def get_credential(self, api_name: str, field: str, default: Any = None) -> Any:
        """
        Get a specific credential field.

        Args:
            api_name: Name of the API
            field: Field name (e.g., 'api_key', 'environment')
            default: Default value if field not set

        Returns:
            Credential field value or default
        """
        credentials = self.get_credentials(api_name)
        return credentials.get(field, default)

    def is_configured(self, api_name: str) -> bool:
        """
        Check if an API has credentials configured.

        Args:
            api_name: Name of the API

        Returns:
            True if credentials are set
        """
        if api_name not in self._apis:
            return False

        credentials = self.get_credentials(api_name)
        config = self._apis[api_name]

        # Check if all required fields are present
        if config.credential_fields:
            return all(field in credentials and credentials[field] for field in config.credential_fields)

        # Otherwise just check if any credentials exist
        return bool(credentials)

    def test_connection(self, api_name: str) -> Tuple[bool, str]:
        """
        Test connection for an API using its validator function.

        Args:
            api_name: Name of the API

        Returns:
            Tuple of (success, message)
        """
        if api_name not in self._apis:
            return False, f"API '{api_name}' not registered"

        config = self._apis[api_name]

        if not config.validator_func:
            return False, "No validation function configured"

        if not self.is_configured(api_name):
            return False, "Credentials not configured"

        try:
            credentials = self.get_credentials(api_name)
            success, message = config.validator_func(**credentials)

            # Update status
            status = st.session_state._connection_status[api_name]
            status.is_tested = True
            status.is_connected = success
            status.last_tested = datetime.now()
            status.error_message = None if success else message

            return success, message

        except Exception as e:
            status = st.session_state._connection_status[api_name]
            status.is_tested = True
            status.is_connected = False
            status.last_tested = datetime.now()
            status.error_message = str(e)

            return False, f"Connection test failed: {str(e)}"

    def get_status(self, api_name: str) -> ConnectionStatus:
        """
        Get connection status for an API.

        Args:
            api_name: Name of the API

        Returns:
            ConnectionStatus object
        """
        if api_name not in st.session_state._connection_status:
            return ConnectionStatus()

        return st.session_state._connection_status[api_name]

    def get_all_apis(self) -> List[APIConfig]:
        """
        Get all registered APIs.

        Returns:
            List of APIConfig objects
        """
        return list(self._apis.values())

    def get_api_config(self, api_name: str) -> Optional[APIConfig]:
        """
        Get configuration for a specific API.

        Args:
            api_name: Name of the API

        Returns:
            APIConfig object or None
        """
        return self._apis.get(api_name)

    def set_client(self, api_name: str, client: Any) -> None:
        """
        Store a client object for an API (e.g., OAuth2 client).

        Args:
            api_name: Name of the API
            client: Client object to store
        """
        st.session_state._credential_clients[api_name] = client

    def get_client(self, api_name: str) -> Optional[Any]:
        """
        Get stored client object for an API.

        Args:
            api_name: Name of the API

        Returns:
            Client object or None
        """
        return st.session_state._credential_clients.get(api_name)

    def clear_credentials(self, api_name: str) -> None:
        """
        Clear credentials for an API.

        Args:
            api_name: Name of the API
        """
        if api_name in st.session_state._credential_store:
            st.session_state._credential_store[api_name] = {}

        if api_name in st.session_state._credential_clients:
            del st.session_state._credential_clients[api_name]

        if api_name in st.session_state._connection_status:
            st.session_state._connection_status[api_name] = ConnectionStatus()

    def reset(self) -> None:
        """Reset all credentials and connection status."""
        st.session_state._credential_store = {}
        st.session_state._connection_status = {}
        st.session_state._credential_clients = {}


# Convenience function for accessing the singleton
def get_credential_manager() -> CredentialManager:
    """Get the global credential manager instance."""
    return CredentialManager()
