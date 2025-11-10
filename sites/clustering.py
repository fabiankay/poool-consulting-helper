import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from src.helpers.prism import create_clustering_df, run_clustering
from src.helpers.poool_api import create_tag, add_tag_to_client, get_companies

st.write("# Example 2: Clustering 🔍")
st.write("In this example, we will use the Poools Prism database to run a clustering algorithm on clients. This will help us identify different segments of clients based on their behavior. Results will be sent to Poool as Tags for further analysis.")
st.write("**Explaining clustering:** Clustering uses data to group similar items together. In this case, we will group clients based on information like total profit, revenue, costs or timetrack information. For example we can group clients based on their respective profits or revenues within the last year.")
st.write("""
         **How to use:** 
         1. Select the number of clusters, the features to use, and the timeframe for the data.
         2. Click 'Run Clustering' to see the results.
         3. inspect the results and assign names to each cluster.
         4. Click 'Send Results to Poool' to send the results to Poool as Tags.
         """)


# Check required session state variables.
if "prism_username" not in st.session_state or "prism_password" not in st.session_state:
    st.error("Please set your Prism Credentials first.")

if "poool_api_key" not in st.session_state:
    # add a link to 1_🚀_Setup.py
    st.error("Please set your Poool API key first.")

if "poool_api_key" not in st.session_state or "prism_username" not in st.session_state or "prism_password" not in st.session_state:
    st.page_link("sites/setup.py", label="Setup", icon="🚀")
    st.stop()

# Form to select the number of clusters, the features to use, and the timeframe for the data.
st.write("### Select options for clustering")

with st.form(key="clustering_form"):
    st.session_state["options"]["num_clusters"] = st.number_input("Number of clusters", min_value=2, max_value=10, value=3)
    st.session_state["options"]["features"] = st.multiselect("Select features", options=["Total revenue", "Total cost", "Total offer", "Total timetrack cost", "Total profit"], default=st.session_state["options"]["features"])
    st.session_state["options"]["timeframe"] = st.date_input("Select timeframe", st.session_state["options"]["timeframe"], format="DD.MM.YYYY")
    submit_button = st.form_submit_button(label="Run Clustering")

if submit_button:
    with st.spinner("Running Cluster analysis..."):
        st.session_state["data"]["clustering_df"] = create_clustering_df(st.session_state["options"]["timeframe"])

if "clustering_df" in st.session_state["data"]:
    # select features by selecting columns
    df = st.session_state["data"]["clustering_df"].copy()
    st.write(df)
    df, kmeans = run_clustering(df, st.session_state["options"]["num_clusters"], st.session_state["options"]["features"])

    st.write("### Clustering Results")
    # display the results by showing the centroids of the clusters and input fields to name the clusters
    st.write("#### Cluster Names")
    # create a dict to store the names of the clusters for each number
    cluster_names = {}

    cols = st.columns(st.session_state["options"]["num_clusters"])

    for i in range(st.session_state["options"]["num_clusters"]):
        with cols[i]:
            st.write(f"##### Cluster {i+1}")
            # show centroid values for cluster i including labels of values
            for j, val in enumerate(kmeans.cluster_centers_[i]):
                st.write(f"{st.session_state['options']['features'][j]}: {round(val, 2)}")

            # number of entries in cluster i
            st.write(f"Number of clients: {len(df[df['cluster'] == i])}")
        
            cluster_name = st.text_input(f"Cluster {i+1} Name", value=f"Cluster {i+1}")
            cluster_names[i] = cluster_name
    
    # add cluster names to the dataframe
    df["cluster_name"] = df["cluster"].map(cluster_names)
    
    st.write("#### Feature Distribution")
    # Display the results of the clustering algorithm as feature distributions for each cluster.
    feature = st.selectbox("Select feature", options=st.session_state["options"]["features"])

    histogram = sns.histplot(data=df, x=feature, hue="cluster_name", multiple="stack", binwidth=max(df[feature])/20)
    plt.title(f'Distribution of {feature}')
    plt.xlabel(f'Client\'s {feature}')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    histogram.legend_.set_title('Cluster')
    sns.despine()
    st.write(histogram.figure)

# Let's send the results to Poool as Tags
if "clustering_df" in st.session_state["data"]:   
    st.write("#### Send Results to Poool")
    st.write("This will send the cluster names to Poool as Tags. This will allow for further analysis of the different client segments.")
    send_button = st.button("Send Results to Poool")

    if send_button:
        # add progress bar for sending clusters to Poool

        companies = get_companies(st.session_state["poool_api_key"])
        
        counter = 0
        size = df.index.nunique()
        progress_text = f"Sending Clustering Results to Poool. Sending Client {counter} of {size}. Please wait."
        # progress step size is number of client_ids
        progress_status = 0
        progress_step = 1 / size
        progress_bar = st.progress(progress_status, text=progress_text)

        for i in range(st.session_state["options"]["num_clusters"]):
            # send cluster names to Poool as Tags
            response = create_tag(cluster_names[i], st.session_state["poool_api_key"])
            tag_id = response.json()["data"]["id"]
            # add tag to all clients in cluster i
            for client_id in df[df["cluster"] == i].index:
                counter += 1
                progress_status += progress_step
                progress_text = f"Sending Clustering Results to Poool. Sending Client {counter} of {size}. Please wait."
                progress_bar.progress(progress_status, text=progress_text)
                response = add_tag_to_client(client_id, tag_id, st.session_state["poool_api_key"])
                if not response:
                    st.error(f"Error setting Tag on Company ID {client_id} - Not Found")
                if response.status_code != 200:
                    st.error(f"Error sending Company ID {client_id} to Poool.")
                    st.write(response.json())

        progress_bar.empty()            
        st.success("Clustering Results sent to Poool successfully.")
