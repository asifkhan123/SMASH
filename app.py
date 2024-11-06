import streamlit as st
from streamlit_card import card
from live_statistics import live_statistics_page
from summary import five_day_summary_page
from waste_channels import waste_channels_page
from analytics import analytics_page
from predictions import predictions_page

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