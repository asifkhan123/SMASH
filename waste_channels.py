import streamlit as st
from graphviz import Digraph
import pandas as pd
import altair as alt

# ---- WASTE CHANNELS PAGE ----
def waste_channels_page():
    st.title("Waste Channels")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live Statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day Summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste Channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

    # Set the title for the app
    st.title("Waste Management Overview")
    st.subheader("Flow of Waste into Channels")

    # Create a flowchart using Graphviz
    dot = Digraph()
    dot.attr(rankdir='TB', size='10,10')  # Top-to-bottom layout
    dot.attr('node', shape='box', style='filled', fillcolor='#f9f9f9', fontcolor='black')
    dot.attr('edge', fontsize='12')

    # Define nodes with colors and styles (sample data) <--
    dot.node('A', 'Total Waste\n(260 tonnes)', fillcolor='#4CAF50')
    dot.node('B', 'Landfill\n(150 tonnes)', fillcolor='#FF5733')
    dot.node('C', 'Recycling\n(80 tonnes)', fillcolor='#3498DB')
    dot.node('D', 'Sustainable Aviation Fuel (SAF)\n(30 tonnes)', fillcolor='#F1C40F')

    # Define edges with colors
    dot.edge('A', 'B', label='Flow to', color='#FF5733')
    dot.edge('A', 'C', label='Flow to', color='#3498DB')
    dot.edge('A', 'D', label='Flow to', color='#F1C40F')

    # Create columns for side-by-side layout
    col1, col2 = st.columns(2)

    # Render the flowchart in the first column
    with col1:
        st.subheader("Waste Flow Diagram")
        st.graphviz_chart(dot)

    # Sample Waste flow data for bar chart
    waste_data = {
        'Channel': ['Landfill', 'Recycling', 'SAF'],
        'Waste Amount (tonnes)': [150, 80, 30]
    }

    df_waste = pd.DataFrame(waste_data)

    # Bar chart to show waste flow into each channel
    with col2:
        st.subheader("Waste Flow Bar Chart")
        bar_chart = alt.Chart(df_waste).mark_bar().encode(
            x=alt.X('Channel', title='Management Channel'),
            y=alt.Y('Waste Amount (tonnes)', title='Waste Amount (tonnes)'),
            color='Channel',
            tooltip=['Channel', 'Waste Amount (tonnes)']
        ).properties(title='Flow of Waste into Management Channels')

        st.altair_chart(bar_chart, use_container_width=True)

    # Recycling rates and environmental impact
    st.subheader("Recycling Rates and Environmental Impact")

    # Example metrics
    total_waste = 260
    recycled_waste = 80
    recycling_rate = (recycled_waste / total_waste) * 100

    # Estimated carbon savings (example value)
    carbon_saved_per_tonne = 0.5  # Assume 0.5 tonnes of CO2 saved per tonne recycled
    total_carbon_saved = recycled_waste * carbon_saved_per_tonne

    # Display metrics
    st.metric(label="Recycling Rate", value=f"{recycling_rate:.2f}%", delta=None)
    st.metric(label="Estimated Carbon Savings", value=f"{total_carbon_saved} tonnes CO2", delta=None)


