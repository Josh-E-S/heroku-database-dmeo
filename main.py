import os
import streamlit as st
import pandas as pd
import psycopg2

# Fetch environment variables (set in Heroku)
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# Function to connect to PostgreSQL database and fetch data
def get_data_from_db():
    try:
        # Connect to your PostgreSQL DB
        conn = psycopg2.connect(SUPABASE_DB_URL)
        
        # Create a cursor object
        cur = conn.cursor()
        
        # Execute a SQL query (adjust with your table name)
        cur.execute("SELECT * FROM your_table_name")
        
        # Fetch all rows from the query
        rows = cur.fetchall()
        
        # Convert to a pandas DataFrame (adjust column names)
        df = pd.DataFrame(rows, columns=["Column1", "Column2", "Column3"]) 
        
        # Close the connection
        cur.close()
        conn.close()

        return df
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return pd.DataFrame()

# Streamlit app
st.title("Supabase (PostgreSQL) Data in Streamlit")

st.write("Fetching data from PostgreSQL database:")

# Fetch and display the data
data = get_data_from_db()

if not data.empty:
    st.write(data)
else:
    st.write("No data available.")
