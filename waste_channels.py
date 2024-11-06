import streamlit as st

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
