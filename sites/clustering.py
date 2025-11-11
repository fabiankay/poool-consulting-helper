import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

from src.helpers.prism import create_clustering_df, run_clustering
from src.helpers.crm import create_api_client, test_api_connection
from src.components.credentials import render_database_credential, render_api_key_credential, get_credential_manager
from src.helpers.prism import validate_login

st.set_page_config(
    page_title="Client Clustering",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Client Clustering Analysis")
st.markdown("Use Prism database to run clustering algorithms on clients and create segmentation tags in Poool CRM.")

st.markdown("""
**What is clustering?** Clustering uses data to group similar items together. We group clients based on
financial metrics like revenue, costs, profit, or timetrack information.

**How to use:**
1. **Configure credentials** below (Prism database + Poool CRM API)
2. **Select clustering options** (number of clusters, features, date range)
3. **Run clustering** to analyze client segments
4. **Name clusters** based on their characteristics
5. **Send to Poool** to create tags and assign them to companies
""")

# Credentials Section
st.markdown("---")
with st.expander("🔑 Configure API Credentials", expanded=False):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Prism Database")
        st.caption("Analytics database for financial data")
        prism_connected = render_database_credential(
            api_name="prism",
            display_name="Prism Database",
            fields={'username': 'Username', 'password': 'Password'},
            test_func=lambda username, password: validate_login(
                username, password, "particles.poool.cc", "pa_prism"
            )
        )

    with col2:
        st.markdown("#### Poool CRM API")
        st.caption("For creating and assigning cluster tags")
        crm_connected = render_api_key_credential(
            api_name="poool_crm",
            display_name="Poool CRM",
            has_environment=True,
            validator_func=test_api_connection
        )

# Check if both are configured
if not (prism_connected and crm_connected):
    st.warning("⚠️ Please configure both Prism Database and Poool CRM credentials above to continue.")
    st.stop()

# Get credential manager
manager = get_credential_manager()

# Initialize session state for options
if "options" not in st.session_state:
    today = datetime.date.today()
    last_year = datetime.date(today.year - 1, 1, 1)
    st.session_state.options = {
        "num_clusters": 3,
        "features": ["Total revenue", "Total profit"],
        "timeframe": [last_year, today]
    }

if "data" not in st.session_state:
    st.session_state.data = {}

# Clustering Options Form
st.markdown("---")
st.subheader("📊 Clustering Configuration")

with st.form(key="clustering_form"):
    num_clusters = st.number_input(
        "Number of clusters",
        min_value=2,
        max_value=10,
        value=st.session_state.options["num_clusters"],
        help="How many client segments to identify"
    )

    features = st.multiselect(
        "Select features for clustering",
        options=["Total revenue", "Total cost", "Total offer", "Total timetrack cost", "Total profit"],
        default=st.session_state.options["features"],
        help="Financial metrics to use for grouping clients"
    )

    timeframe = st.date_input(
        "Select date range",
        value=st.session_state.options["timeframe"],
        format="DD.MM.YYYY",
        help="Time period for financial data"
    )

    submit_button = st.form_submit_button(label="🔍 Run Clustering Analysis")

# Run clustering when form is submitted
if submit_button:
    if not features:
        st.error("Please select at least one feature for clustering")
        st.stop()

    if len(timeframe) != 2:
        st.error("Please select both start and end dates")
        st.stop()

    # Update options
    st.session_state.options["num_clusters"] = num_clusters
    st.session_state.options["features"] = features
    st.session_state.options["timeframe"] = timeframe

    # Get Prism credentials
    prism_creds = manager.get_credentials("prism")
    username = prism_creds.get('username')
    password = prism_creds.get('password')

    # Fetch clustering data
    with st.spinner("Fetching financial data from Prism database..."):
        df, error = create_clustering_df(username, password, list(timeframe))

        if error:
            st.error(f"❌ Failed to fetch data: {error}")
            st.stop()

        st.session_state.data["clustering_df"] = df
        st.success(f"✅ Fetched data for {len(df)} clients")

# Display results if clustering has been run
if "clustering_df" in st.session_state.data:
    df = st.session_state.data["clustering_df"].copy()

    st.markdown("---")
    st.subheader("📈 Data Preview")
    st.dataframe(df, use_container_width=True)

    # Run clustering algorithm
    df_clustered, kmeans = run_clustering(
        df,
        st.session_state.options["num_clusters"],
        st.session_state.options["features"]
    )

    # Cluster Naming Section
    st.markdown("---")
    st.subheader("🏷️ Cluster Analysis & Naming")
    st.markdown("Review cluster characteristics and assign meaningful names:")

    cluster_names = {}
    cols = st.columns(st.session_state.options["num_clusters"])

    for i in range(st.session_state.options["num_clusters"]):
        with cols[i]:
            st.markdown(f"### Cluster {i+1}")

            # Show centroid values
            st.markdown("**Average values:**")
            for j, val in enumerate(kmeans.cluster_centers_[i]):
                feature_name = st.session_state.options["features"][j]
                st.metric(feature_name, f"{val:,.2f}")

            # Show cluster size
            cluster_size = len(df_clustered[df_clustered["cluster"] == i])
            st.info(f"👥 {cluster_size} clients in this cluster")

            # Name input
            cluster_name = st.text_input(
                "Cluster name",
                value=f"Cluster {i+1}",
                key=f"cluster_name_{i}",
                help="Give this segment a meaningful name (e.g., 'High Value', 'Growing', 'At Risk')"
            )
            cluster_names[i] = cluster_name

    # Add cluster names to dataframe
    df_clustered["cluster_name"] = df_clustered["cluster"].map(cluster_names)

    # Feature Distribution Visualization
    st.markdown("---")
    st.subheader("📊 Feature Distribution by Cluster")

    feature = st.selectbox(
        "Select feature to visualize",
        options=st.session_state.options["features"],
        help="View how this metric is distributed across clusters"
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    histogram = sns.histplot(
        data=df_clustered,
        x=feature,
        hue="cluster_name",
        multiple="stack",
        binwidth=max(df_clustered[feature])/20 if max(df_clustered[feature]) > 0 else 1,
        ax=ax
    )
    plt.title(f'Distribution of {feature} by Cluster')
    plt.xlabel(f'Client\'s {feature}')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    histogram.legend_.set_title('Cluster')
    sns.despine()
    st.pyplot(fig)

    # Send Results to Poool
    st.markdown("---")
    st.subheader("🚀 Send Results to Poool CRM")
    st.markdown("""
    This will:
    1. Create tags in Poool CRM for each cluster
    2. Assign the appropriate tag to each company based on their cluster
    3. Enable segmentation and targeted analysis in Poool
    """)

    if st.button("📤 Send Cluster Tags to Poool", type="primary"):
        # Get CRM credentials
        crm_creds = manager.get_credentials("poool_crm")

        # Create API client
        client = create_api_client(
            api_key=crm_creds['api_key'],
            environment=crm_creds.get('environment', 'production'),
            custom_url=crm_creds.get('custom_url')
        )

        # Progress tracking
        total_companies = df_clustered.index.nunique()
        progress_text = "Creating cluster tags and assigning to companies..."
        progress_bar = st.progress(0, text=progress_text)
        progress_counter = 0

        success_count = 0
        error_count = 0
        errors = []

        # Process each cluster
        for i in range(st.session_state.options["num_clusters"]):
            cluster_name = cluster_names[i]

            # Create tag in Poool (won't duplicate if exists)
            tag_id, error = client.create_tag_if_missing(
                tag_name=f"Cluster: {cluster_name}",
                color="#000000",
                color_background="#f3f3f3"
            )

            if error:
                st.error(f"❌ Failed to create tag '{cluster_name}': {error}")
                error_count += 1
                continue

            st.info(f"✅ Created/found tag: '{cluster_name}' (ID: {tag_id})")

            # Get all client IDs in this cluster
            cluster_client_ids = df_clustered[df_clustered["cluster"] == i].index.tolist()

            # Add tag to each company in the cluster
            for client_id in cluster_client_ids:
                progress_counter += 1
                progress_bar.progress(
                    progress_counter / total_companies,
                    text=f"Processing company {progress_counter}/{total_companies}..."
                )

                try:
                    # Fetch company
                    company, error = client.get_company_by_id(int(client_id))

                    if error:
                        errors.append(f"Company {client_id}: {error}")
                        error_count += 1
                        continue

                    # Add tag to tags array (if not already present)
                    tags = company.get('tags', [])
                    if not any(t.get('id') == tag_id for t in tags):
                        tags.append({"id": tag_id})

                        # Update company
                        _, error = client.update_company(int(client_id), {"tags": tags})

                        if error:
                            errors.append(f"Company {client_id}: Failed to update tags - {error}")
                            error_count += 1
                        else:
                            success_count += 1
                    else:
                        # Tag already exists
                        success_count += 1

                except Exception as e:
                    errors.append(f"Company {client_id}: Unexpected error - {str(e)}")
                    error_count += 1

        # Clear progress bar
        progress_bar.empty()

        # Show results
        st.markdown("---")
        st.subheader("📊 Results Summary")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Successful", success_count)
        with col2:
            st.metric("❌ Errors", error_count)
        with col3:
            success_rate = (success_count / total_companies * 100) if total_companies > 0 else 0
            st.metric("Success Rate", f"{success_rate:.1f}%")

        if success_count > 0:
            st.success(f"🎉 Successfully tagged {success_count} companies with cluster segments!")

        # Show errors if any
        if errors:
            with st.expander(f"⚠️ View Errors ({len(errors)})", expanded=False):
                for error_msg in errors[:50]:  # Limit to first 50
                    st.error(error_msg)
                if len(errors) > 50:
                    st.caption(f"... and {len(errors) - 50} more errors")
