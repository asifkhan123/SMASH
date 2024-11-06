import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---- LIVE STATISTICS PAGE ----
def live_statistics_page():
    st.title("Live Statistics")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live Statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day Summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste Channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

    # Sample flight data <--
    flight_data = {
        "Flight Number": ["A1", "A2", "B1", "B2", "C1"],
        "Status": ["On Time", "Delayed", "On Time", "Cancelled", "On Time"],
        "Total Waste (tons)": [120, 150, 90, 200, 300],
    }

    # Create a DataFrame
    df_flights = pd.DataFrame(flight_data)

    # Create two columns for layout at the top of the page
    col1, col2 = st.columns([1, 1])  # Adjust column width as needed

    # Display the flight data table in the first column
    with col1:
        st.subheader("Flight Data")
        st.dataframe(df_flights)

    # Sample waste segregation data <--
    waste_segmentation = {
        "Plastic": 40,
        "Organic": 30,
        "Metal": 20,
        "Glass": 10,
    }

    # Create a pie chart
    fig, ax = plt.subplots(figsize=(4, 4))  # Smaller figure size for the pie chart
    ax.pie(waste_segmentation.values(), labels=waste_segmentation.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Display the pie chart in the second column
    with col2:
        st.subheader("Waste Segregation")
        st.pyplot(fig)

        # Last updated timestamp
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Last Updated: {last_updated}")

def get_flight_data(flight):
    # Sample data (replace this with actual data retrieval logic) <--
    if flight == "Flight A":
        return 120, ["Plastic", "Organic"]
    elif flight == "Flight B":
        return 150, ["Metal", "Glass"]
    elif flight == "Flight C":
        return 90, ["Organic", "Paper"]
    return 0, []
