import os
import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Fetch environment variables (set in Heroku)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
@st.cache_resource
def init_supabase() -> Client:
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        st.error("Missing Supabase URL or Key. Please check environment variables.")
        return None

# Fetch data from Supabase
def fetch_data():
    supabase = init_supabase()
    if supabase:
        response = supabase.table("your_table_name").select("*").execute()
        if response.status_code == 200:
            return pd.DataFrame(response.data)
        else:
            st.error(f"Error fetching data: {response.error_message}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()

# Streamlit app
st.title("Supabase Data in Streamlit")

st.write("Fetching data from Supabase:")

# Retrieve and display data
data = fetch_data()

if not data.empty:
    st.write(data)
else:
    st.write("No data available or error fetching data.")
