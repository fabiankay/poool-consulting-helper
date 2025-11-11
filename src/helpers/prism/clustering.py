"""
Prism Clustering Analysis

K-Means clustering functionality for client segmentation based on financial data.
"""

from typing import List
from sklearn.cluster import KMeans
import streamlit as st
import pandas as pd


@st.cache_data(show_spinner=False)
def run_clustering(df: pd.DataFrame, num_clusters: int, features: List[str]) -> tuple[pd.DataFrame, KMeans]:
    """
    Run K-Means clustering on the provided dataframe.

    Args:
        df: DataFrame with client financial data
        num_clusters: Number of clusters to create (2-10 recommended)
        features: List of feature column names to use for clustering

    Returns:
        Tuple of (clustered_dataframe, kmeans_model)
            clustered_dataframe: DataFrame with 'cluster' column added
            kmeans_model: Fitted KMeans model
    """
    df = df[features].copy()
    kmeans = KMeans(n_clusters=num_clusters)
    df["cluster"] = kmeans.fit_predict(df)
    return df, kmeans
