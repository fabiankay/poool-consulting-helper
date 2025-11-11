"""
Prism Database Connection and Validation

Handles database connection and credential validation for the Prism PostgreSQL database.
"""

from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def validate_login(user: str, password: str, host: str = "particles.poool.cc", database: str = "pa_prism") -> Tuple[bool, str]:
    """
    Validate Prism database credentials.

    Args:
        user: Database username
        password: Database password
        host: Database host (default: particles.poool.cc)
        database: Database name (default: pa_prism)

    Returns:
        Tuple of (success, message)
            success: True if connection successful, False otherwise
            message: Success or error message
    """
    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
        connection = engine.connect()
        connection.close()
        return True, "Database connection verified"

    except OperationalError as e:
        return False, f"Invalid database credentials: {str(e)}"
    except Exception as e:
        return False, f"Database connection error: {str(e)}"
