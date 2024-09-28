import os
import streamlit as st
import pandas as pd
import requests

# Fetch environment variables (set in Heroku or locally)
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Supabase URL from environment variable
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Supabase API Key from environment variable

# Function to fetch data from Supabase REST API
def get_data_from_supabase():
    try:
        # Use st.spinner to show a message while attempting connection
        with st.spinner("Attempting to connect to Supabase..."):
            # Define the table you want to fetch data from
            TABLE_NAME = "Product"  # Adjust to match your actual table name

            # Headers for authorization
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            }

            # URL to fetch data from
            url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"

            # Query parameters (select all fields)
            params = {
                "select": "*"
            }

            # Make the request to Supabase REST API
            response = requests.get(url, headers=headers, params=params)

            # Check if the connection to Supabase was successful
            if response.status_code == 200:
                st.success("Connection to Supabase successful.")
            else:
                st.error(f"Connection to Supabase unsuccessful. Status code: {response.status_code}")
                return pd.DataFrame()

            # Data retrieval
            data = response.json()

            # Check if data was retrieved
            if data:
                st.success("Data retrieval successful.")
                # Convert to a pandas DataFrame (adjust column names to match your table structure)
                df = pd.DataFrame(data)
                return df
            else:
                st.error("Data retrieval unsuccessful or no data available.")
                return pd.DataFrame()

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return pd.DataFrame()

# Streamlit app
st.title("Supabase Product Data in Streamlit")

# Feedback messages for each step
st.write("Fetching data from Supabase REST API:")

# Fetch and display the data from the Product table
data = get_data_from_supabase()

# Check if data was successfully retrieved
if not data.empty:
    # Display the table with the same width as the messages
    st.dataframe(data, use_container_width=True)
else:
    st.write("No data available.")
