"""
Prism Database Queries

SQL query functions for fetching data from the Prism PostgreSQL database.
"""

import datetime
from typing import List, Tuple, Optional
from streamlit.connections import SQLConnection
import streamlit as st
import pandas as pd


@st.cache_data
def get_timetrack_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT
                jsonb_array_elements_text(prism_source_reference->'client_id') AS client_id,
                SUM(data_timetrack_cost_client::numeric) as total_timetrack_cost
            FROM
                timetrack_times
            WHERE
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY
                client_id;
            """
    df = _conn.query(query)
    return df


@st.cache_data
def get_revenue_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT
                jsonb_array_elements_text(prism_source_reference->'company_id') AS client_id,
                SUM(data_item_value::numeric) as total_revenue
            FROM
                calculation_report
            WHERE
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
                AND data_item_account_type = 'receivable'
            GROUP BY
                client_id;
    """
    df = _conn.query(query)
    return df


@st.cache_data
def get_cost_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT
                jsonb_array_elements_text(prism_source_reference->'client_id') AS client_id,
                SUM(data_invoice_position_netto::numeric) as total_cost
            FROM
                accounts_payable
            WHERE
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY
                client_id;
    """
    df = _conn.query(query)
    return df


@st.cache_data
def get_offer_data(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    query = f"""
            SELECT
                jsonb_array_elements_text(prism_source_reference->'client_id') AS client_id,
                SUM(data_calculation_position_total_sum::numeric) as total_offer
            FROM
                calculation_positions
            WHERE
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
                AND data_calculation_type = 'offer'
            GROUP BY
                client_id;
    """
    df = _conn.query(query)
    return df


@st.cache_data
def get_overhead_costs_by_apportion(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """
    Get overhead costs grouped by data_invoice_position_apportion field from accounts_payable table.

    Args:
        _conn: Streamlit SQL connection to Prism database
        start_date: Start date for filtering
        end_date: End date for filtering

    Returns:
        DataFrame with columns: data_invoice_position_apportion, total_cost
    """
    query = f"""
            SELECT
                data_invoice_position_apportion,
                SUM(data_invoice_position_netto::numeric) as total_cost
            FROM
                accounts_payable
            WHERE
                data_day_date BETWEEN '{start_date}' AND '{end_date}'
                AND data_invoice_position_apportion IS NOT NULL
            GROUP BY
                data_invoice_position_apportion
            ORDER BY
                data_invoice_position_apportion;
            """
    df = _conn.query(query)
    return df


@st.cache_data
def get_productivity_metrics(_conn: SQLConnection, start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """
    Get productivity metrics from timetrack_days table including vacation, sick days, and working hours.

    Args:
        _conn: Streamlit SQL connection to Prism database
        start_date: Start date for filtering
        end_date: End date for filtering

    Returns:
        DataFrame with aggregated productivity metrics
    """
    query = f"""
            SELECT
                COUNT(DISTINCT data_employee_id) as total_employees,
                AVG(CASE WHEN data_day_type = 'vacation' THEN 1 ELSE 0 END *
                    COUNT(*) OVER ()) as avg_vacation_days,
                AVG(CASE WHEN data_day_type = 'sick' THEN 1 ELSE 0 END *
                    COUNT(*) OVER ()) as avg_sick_days,
                AVG(data_hours_tracked::numeric) as avg_hours_per_day,
                SUM(CASE WHEN data_is_billable = true THEN data_hours_tracked::numeric ELSE 0 END) /
                    NULLIF(SUM(data_hours_tracked::numeric), 0) * 100 as productivity_percent
            FROM
                timetrack_days
            WHERE
                data_day_date BETWEEN '{start_date}' AND '{end_date}';
            """
    df = _conn.query(query)
    return df


@st.cache_data(show_spinner=False)
def create_clustering_df(
    username: str,
    password: str,
    timeframe: List[datetime.date] = None
) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Create clustering dataframe from Prism database.

    Fetches and merges timetrack, revenue, cost, and offer data for the specified
    date range, then calculates profit and prepares data for clustering analysis.

    Args:
        username: Database username
        password: Database password
        timeframe: List of [start_date, end_date], defaults to last year

    Returns:
        Tuple of (dataframe, error_message)
            dataframe: Prepared DataFrame indexed by client_id, None if error
            error_message: None if successful, error string otherwise
    """
    # Default timeframe to last year
    if timeframe is None:
        today = datetime.date.today()
        timeframe = [datetime.date(today.year - 1, 1, 1), today]

    try:
        # Initialize connection
        _conn = st.connection("postgresql",
                         dialect="postgresql",
                         type="sql",
                         host="particles.poool.cc",
                         database="pa_prism",
                         username=username,
                         password=password
                         )

        # Fetch data from all sources
        timetrack_data = get_timetrack_data(_conn, timeframe[0], timeframe[1])
        revenue_data = get_revenue_data(_conn, timeframe[0], timeframe[1])
        cost_data = get_cost_data(_conn, timeframe[0], timeframe[1])
        offer_data = get_offer_data(_conn, timeframe[0], timeframe[1])

        # Get all client tokens
        client_ids = set(timetrack_data["client_id"]).union(
            set(revenue_data["client_id"]),
            set(cost_data["client_id"]),
            set(offer_data["client_id"])
        )

        # Create dataframe with all client tokens and respective data
        df = pd.DataFrame(client_ids, columns=["client_id"])
        df = df.merge(timetrack_data, on="client_id", how="left")
        df = df.merge(revenue_data, on="client_id", how="left")
        df = df.merge(cost_data, on="client_id", how="left")
        df = df.merge(offer_data, on="client_id", how="left")

        # Remove rows where client_token is null (e.g. Cost without client_id)
        df = df.dropna(subset=["client_id"])

        # Fill missing values with 0
        df.fillna(0, inplace=True)

        # Calculate profit
        df['Total profit'] = df['total_revenue'] - df['total_cost'] - df['total_timetrack_cost']

        # Rename columns
        df.rename(columns={
            "total_timetrack_cost": "Total timetrack cost",
            "total_revenue": "Total revenue",
            "total_cost": "Total cost",
            "total_offer": "Total offer"
        }, inplace=True)

        # Set client_token as index
        df.set_index("client_id", inplace=True)

        return df, None

    except Exception as e:
        return None, f"Database error: {str(e)}"
