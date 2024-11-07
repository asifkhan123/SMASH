import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime
import base64

# ---- LIVE STATISTICS PAGE ----
def live_statistics_page():
    with open("logo.jpeg", "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    
    # Create two columns: one for the title and one for the logo
    col1, col2 = st.columns([7, 1])  # Adjust the ratio as needed

    with col1:
        st.title("Live Statistics")  # Title in the first column

    with col2:
        logo = data  # Adjust this path if necessary
        st.image(logo, width=150)  # Display logo in the second column

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live Statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("Overall Summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste Channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

    # Connect to SQLite database
    conn = sqlite3.connect('flight_waste.db')
    
    # Fetch flight data
    flight_query = "SELECT flight_number AS 'Flight Number', date, volume, status FROM flights"
    df_flights = pd.read_sql_query(flight_query, conn)

    # Rename the volume column for clarity
    df_flights.rename(columns={'volume': 'Total Waste (tons)'}, inplace=True)

    # Create two columns for layout at the top of the page
    col1, col2 = st.columns([3, 2])  # Adjust column width as needed

    # Display the flight data table in the first column
    with col1:
        st.subheader("Flight Data")
        st.dataframe(df_flights)

    # Fetch waste segregation data
    segregation_query = "SELECT type, SUM(volume) as total_volume FROM segregation GROUP BY type"
    df_segmentation = pd.read_sql_query(segregation_query, conn)

    # Create a pie chart
    fig, ax = plt.subplots(figsize=(4, 4))  # Smaller figure size for the pie chart
    ax.pie(df_segmentation['total_volume'], labels=df_segmentation['type'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart in the second column
    with col2:
        st.subheader("Waste Segregation")
        st.pyplot(fig)

        # Last updated timestamp
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Last Updated: {last_updated}")

    # Close the database connection
    conn.close()
