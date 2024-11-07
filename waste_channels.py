import streamlit as st
from graphviz import Digraph
import pandas as pd
import altair as alt
import sqlite3
import base64

# ---- WASTE CHANNELS PAGE ----
def waste_channels_page():
    with open("logo.jpeg", "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    
    # Create two columns: one for the title and one for the logo
    col1, col2 = st.columns([7, 1])  # Adjust the ratio as needed

    with col1:
        st.title("Waste Management Overview")  # Title in the first column

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

    # Set the title for the app
    st.subheader("Flow of Waste into Channels")

    # Connect to SQLite database
    conn = sqlite3.connect('flight_waste.db')

    # Fetch waste channel data from the database
    channels_query = """
    SELECT 
        channel, 
        SUM(co2_emission) AS total_co2_emission
    FROM channel
    GROUP BY channel
    """
    df_channels = pd.read_sql_query(channels_query, conn)

    # Calculate total waste (sum of CO2 emissions)
    total_waste = df_channels['total_co2_emission'].sum()

    # Create a flowchart using Graphviz
    dot = Digraph()
    dot.attr(rankdir='TB', size='10,10')  # Top-to-bottom layout
    dot.attr('node', shape='box', style='filled', fillcolor='#f9f9f9', fontcolor='black')
    dot.attr('edge', fontsize='12')

    # Define nodes for each channel
    dot.node('A', f'Total Waste\n({total_waste:.1f} tonnes)', fillcolor='#4CAF50')
    for index, row in df_channels.iterrows():
        dot.node(chr(66 + index), f"{row['channel'].capitalize()}\n({row['total_co2_emission']:.1f} tonnes)", fillcolor='#3498DB')

    # Define edges with colors
    for index in range(len(df_channels)):
        dot.edge('A', chr(66 + index), label='Flow to', color='#3498DB')

    # Create columns for side-by-side layout
    col1, col2 = st.columns(2)

    # Render the flowchart in the first column
    with col1:
        st.markdown("<h2 style='font-size: 20px;'>Waste Flow Diagram</h2>", unsafe_allow_html=True)
        st.graphviz_chart(dot)

    # Bar chart to show waste flow into each channel
    with col2:
        bar_chart = alt.Chart(df_channels).mark_bar().encode(
            x=alt.X('channel:O', title='Management Channel'),
            y=alt.Y('total_co2_emission:Q', title='Waste Amount (tonnes)'),
            color='channel:N',
            tooltip=['channel:N', 'total_co2_emission:Q']
        ).properties(title='Flow of Waste into Management Channels')

        st.altair_chart(bar_chart, use_container_width=True)

    # Recycling rates and environmental impact
    st.subheader("Total Environmental Impact")

    # Calculate recycling metrics based on the channel data
    recycled_waste = df_channels.loc[df_channels['channel'] == 'recycling', 'total_co2_emission'].values[0] if not df_channels[df_channels['channel'] == 'recycling'].empty else 0
    recycling_rate = (recycled_waste / total_waste * 100) if total_waste > 0 else 0

    # Estimated carbon savings
    carbon_saved_per_tonne = 0.5  # Assume 0.5 tonnes of CO2 saved per tonne recycled
    total_carbon_saved = recycled_waste * carbon_saved_per_tonne

    # Display metrics
    st.metric(label="Recycling Rate", value=f"{recycling_rate:.2f}%", delta=None)
    st.metric(label="Estimated Carbon Savings", value=f"{total_carbon_saved:.2f} tonnes CO2", delta=None)

    # Close the database connection
    conn.close()