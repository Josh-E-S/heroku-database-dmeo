import os
import streamlit as st
import pandas as pd
import requests

# Fetch environment variables (set in Heroku)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Function to fetch data from Supabase REST API
def get_data_from_supabase():
    try:
        # Define the table you want to fetch data from
        TABLE_NAME = "users"  # Adjust to match your table name

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

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Convert to a pandas DataFrame (adjust column names to match your table structure)
            df = pd.DataFrame(data)
            return df
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}, Error: {response.text}")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return pd.DataFrame()

# Streamlit app
st.title("Supabase Data in Streamlit")

st.write("Fetching data from Supabase REST API:")

# Fetch and display the data
data = get_data_from_supabase()

if not data.empty:
    st.write(data)
else:
    st.write("No data available.")
