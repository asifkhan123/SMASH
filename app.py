import streamlit as st
# Set the page configuration
st.set_page_config(layout="wide")

from streamlit_card import card
from live_statistics import live_statistics_page
from summary import five_day_summary_page
from waste_channels import waste_channels_page
from predictions import predictions_page
import base64

# Load images and encode them
def load_images():
    images = []
    image_files = ["live.jpeg", "summary.jpeg", "wastechannels.jpeg", "predictions.jpeg"]
    
    for filename in image_files:
        with open(filename, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data)
            images.append("data:image/png;base64," + encoded.decode("utf-8"))
    
    return images

# ---- MAIN FUNCTION ----
def main():
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
    elif st.session_state.page == 'predictions':
        predictions_page()

def show_home_page():
    st.title("Home")

    # Create a grid layout for the cards
    row1 = st.columns([1, 1])
    row2 = st.columns([1, 1])  # Adjusted to fit 4 cards

    # Define the card details
    card_details = [
        {"title": "Live Statistics", "text": "View live waste statistics", "url": "live_statistics"},
        {"title": "5-day Summary", "text": "Description for Card 2", "url": "summary"},
        {"title": "Waste Channels", "text": "Description for Card 3", "url": "waste_channels"},
        {"title": "Predictions and Recommended Actions", "text": "Description for Card 4", "url": "predictions"},
    ]

    data = load_images()

    # Generate cards in the grid
    for i, col in enumerate(row1 + row2):
        if i < len(card_details):  # Ensure we don't exceed the number of cards
            with col:
                card(
                    title=card_details[i]["title"],
                    text=card_details[i]["text"],
                    image=data[i],
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