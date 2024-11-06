import streamlit as st

# ---- LIVE STATISTICS PAGE ----
def live_statistics_page():
    st.title("Live Statistics")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Analytics", on_click=lambda: st.session_state.update({"page": "analytics"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))



    # Dropdown menu to select a flight
    flight_options = ["Flight A", "Flight B", "Flight C"]  #Use database
    selected_flight = st.selectbox("Select a flight:", flight_options)

    # Simulate data for the selected flight - modify this
    if selected_flight:
        volume, waste_types = get_flight_data(selected_flight)
        st.write(f"Volume of waste for {selected_flight}: {volume} tons")
        st.write(f"Types of waste: {', '.join(waste_types)}")

def get_flight_data(flight):
    # Simulated data (replace this with actual data retrieval logic)
    if flight == "Flight A":
        return 120, ["Plastic", "Organic"]
    elif flight == "Flight B":
        return 150, ["Metal", "Glass"]
    elif flight == "Flight C":
        return 90, ["Organic", "Paper"]
    return 0, []
