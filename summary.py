import streamlit as st

# ---- 5-DAY SUMMARY PAGE ----
def five_day_summary_page():
    st.title("5-Day Summary")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Analytics", on_click=lambda: st.session_state.update({"page": "analytics"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

    # Simulate 5-day summary data
    summary_data = {
        "Flight A": [100, 120, 130, 110, 140],
        "Flight B": [90, 95, 100, 110, 115],
        "Flight C": [80, 85, 90, 95, 100],
    }

    # Display the summary for each flight
    for flight, volumes in summary_data.items():
        st.subheader(f"{flight} Waste Summary")
        st.write("Daily volumes (tons):", volumes)
        st.write("Total waste over 5 days:", sum(volumes), "tons")
        st.write("Average daily waste:", sum(volumes) / len(volumes), "tons")
        st.write("---")  # Separator for better readability