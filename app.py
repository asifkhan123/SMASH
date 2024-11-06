import streamlit as st
from streamlit_card import card
# from live_statistics import live_statistics_page

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

# ---- WASTE CHANNELS PAGE ----
def waste_channels_page():
    st.title("Waste Channels")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Analytics", on_click=lambda: st.session_state.update({"page": "analytics"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

# ---- ANALYTICS PAGE ----
def analytics_page():
    st.title("Analytics")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Analytics", on_click=lambda: st.session_state.update({"page": "analytics"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

# ---- PREDICTIONS PAGE ----
def predictions_page():
    st.title("Predictions")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Analytics", on_click=lambda: st.session_state.update({"page": "analytics"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

# ---- MAIN FUNCTION ----
def main():
    # Set the title of the app
    st.set_page_config(layout="wide")
    
    # Initialize the session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # Check which page to display
    if st.session_state.page == 'home':
        show_home_page()
    elif st.session_state.page == 'live_statistics':
        live_statistics_page()
    elif st.session_state.page == 'summary':
        five_day_summary_page()
    elif st.session_state.page == 'waste_channels':
        waste_channels_page()
    elif st.session_state.page == 'analytics':
        analytics_page()
    elif st.session_state.page == 'predictions':
        predictions_page()

def show_home_page():
    st.title("Home")

    # Create a grid layout for the cards
    row1 = st.columns([1, 1, 1])
    row2 = st.columns([1.5, 1.5])  # Adjusted to fit 5 cards

    # Define the card details
    card_details = [
        {"title": "Live Statistics", "text": "View live waste statistics", "url": "live_statistics"},
        {"title": "5-day summary", "text": "Description for Card 2", "url": "summary"},
        {"title": "Waste channels", "text": "Description for Card 3", "url": "waste_channels"},
        {"title": "Analytics", "text": "Description for Card 4", "url": "analytics"},
        {"title": "Predictions", "text": "Description for Card 5", "url": "predictions"},
    ]

    # Generate cards in the grid
    for i, col in enumerate(row1 + row2):
        if i < len(card_details):  # Ensure we don't exceed the number of cards
            with col:
                card(
                    title=card_details[i]["title"],
                    text=card_details[i]["text"],
                    on_click=lambda url=card_details[i]["url"]: st.session_state.update({"page": url}),
                    styles={
                        "card": {
                            "width": "100%",
                            "padding": "5px",
                            "margin": "0px",
                        },
                    }
                )

if __name__ == "__main__":
    main()