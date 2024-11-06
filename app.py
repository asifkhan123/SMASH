import streamlit as st
from streamlit_card import card

# # ---- MAINPAGE ----

# Set the title of the app
st.set_page_config(layout="wide")
st.title("Home")

# Create a grid layout for the cards
row1 = st.columns([1, 1, 1])
row2 = st.columns([1.5, 1.5])  # Adjusted to fit 5 cards

# Define the card details
card_details = [
    {"title": "Live Statistics", "text": "Description for Card 1", "image": "http://placekitten.com/200/300", "url": "page1", "width": "100%"},
    {"title": "5-day summary", "text": "Description for Card 2", "image": "http://placekitten.com/200/300", "url": "page2", "width": "100%"},
    {"title": "Waste channels", "text": "Description for Card 3", "image": "http://placekitten.com/200/300", "url": "page3", "width": "100%"},
    {"title": "Analytics", "text": "Description for Card 4", "image": "http://placekitten.com/200/300", "url": "page4", "width": "100%"},
    {"title": "Predictions", "text": "Description for Card 5", "image": "http://placekitten.com/200/300", "url": "page5", "width": "100%"},
]

# Create a list to hold the card containers
card_containers = []

# Generate cards in the grid
for i, col in enumerate(row1 + row2):
    if i < len(card_details):  # Ensure we don't exceed the number of cards
        with col:
            hasClicked = card(
                title=card_details[i]["title"],
                text=card_details[i]["text"],
                # image=card_details[i]["image"],
                on_click=lambda url=card_details[i]["url"]: st.session_state.update({"page": url}),
                styles={
                    "card": {
                    "width": card_details[i]["width"],
                    "padding": "5px",
                    "margin": "0px", 
                },
                "text": {
                    "font-family": "serif",
            
                }
                }
            )
            card_containers.append(hasClicked)

# Check which page to display based on the button clicks
if "page" in st.session_state:
    if st.session_state.page == "page1":
        st.write("You navigated to Page 1!")
    elif st.session_state.page == "page2":
        st.write("You navigated to Page 2!")
    elif st.session_state.page == "page3":
        st.write("You navigated to Page 3!")
    elif st.session_state.page == "page4":
        st.write("You navigated to Page 4!")
    elif st.session_state.page == "page5":
        st.write("You navigated to Page 5!")