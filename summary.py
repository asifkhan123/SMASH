import streamlit as st
import pandas as pd
import altair as alt

# ---- 5-DAY SUMMARY PAGE ----
def five_day_summary_page():
    st.title("5-Day Summary")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live Statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day Summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste Channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

    # Sample data for the table <--
    summary_data = {
        "Destination": ["Airport A", "Airport B", "Airport C"],
        "Recyclable (kgs)": [500, 300, 400],
        "Non-Recyclable (kgs)": [200, 150, 300],
    }
    df_summary = pd.DataFrame(summary_data)
    df_summary["Total (kgs)"] = df_summary["Recyclable (kgs)"] + df_summary["Non-Recyclable (kgs)"]

    # Calculate the total row
    total_row = pd.DataFrame({
        "Destination": ["Total"],
        "Recyclable (kgs)": [df_summary["Recyclable (kgs)"].sum()],
        "Non-Recyclable (kgs)": [df_summary["Non-Recyclable (kgs)"].sum()],
        "Total (kgs)": [df_summary["Total (kgs)"].sum()]
    })
    df_summary = pd.concat([df_summary, total_row], ignore_index=True)

    # Display the waste summary table without index
    st.subheader("Waste Summary Table")
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

    # Sample daily waste data for line graph <--
    daily_waste_data = {
        "Day": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
        "Flight A (Recyclable)": [40, 50, 60, 55, 70],
        "Flight A (Non-Recyclable)": [60, 70, 70, 55, 70],
        "Flight B (Recyclable)": [30, 35, 40, 45, 50],
        "Flight B (Non-Recyclable)": [60, 60, 60, 65, 65],
        "Flight C (Recyclable)": [25, 30, 35, 40, 45],
        "Flight C (Non-Recyclable)": [55, 55, 55, 55, 55],
    }
    df_daily_waste = pd.DataFrame(daily_waste_data)

    # Calculate total waste for each flight
    for flight in ["A", "B", "C"]:
        df_daily_waste[f"Flight {flight} (Total)"] = (
            df_daily_waste[f"Flight {flight} (Recyclable)"] +
            df_daily_waste[f"Flight {flight} (Non-Recyclable)"]
        )

    # Line chart for daily waste per flight
    st.subheader("Daily Waste per Flight")
    selected_flight = st.selectbox("Select a flight to view daily waste:", ["Flight A", "Flight B", "Flight C"])

    # Melt the dataframe for Altair
    df_melted = df_daily_waste.melt(id_vars='Day', var_name='Flight Type', value_name='Waste (kgs)')
    
    # Filter for the selected flight only
    df_melted_filtered = df_melted[df_melted['Flight Type'].str.contains(selected_flight)]
    
    # Add the total line for the selected flight
    df_total_filtered = df_daily_waste[['Day', f'Flight {selected_flight[-1]} (Total)']]
    df_total_filtered = df_total_filtered.rename(columns={f'Flight {selected_flight[-1]} (Total)': 'Waste (kgs)'})
    df_total_filtered['Flight Type'] = 'Total'
    
    # Add recyclable and non-recyclable lines for the selected flight
    df_recyclable = df_daily_waste[['Day', f'Flight {selected_flight[-1]} (Recyclable)']]
    df_recyclable = df_recyclable.rename(columns={f'Flight {selected_flight[-1]} (Recyclable)': 'Waste (kgs)'})
    df_recyclable['Flight Type'] = 'Recyclable'

    df_non_recyclable = df_daily_waste[['Day', f'Flight {selected_flight[-1]} (Non-Recyclable)']]
    df_non_recyclable = df_non_recyclable.rename(columns={f'Flight {selected_flight[-1]} (Non-Recyclable)': 'Waste (kgs)'})
    df_non_recyclable['Flight Type'] = 'Non-Recyclable'

    # Combine all DataFrames
    df_combined = pd.concat([df_total_filtered[['Day', 'Flight Type', 'Waste (kgs)']],
                             df_recyclable, df_non_recyclable], ignore_index=True)

    # Create the line chart
    line_chart = alt.Chart(df_combined).mark_line().encode(
        x='Day',
        y='Waste (kgs)',
        color=alt.Color('Flight Type', legend=alt.Legend(title=None)),  # Remove legend title
        tooltip=['Day', 'Flight Type', 'Waste (kgs)']
    ).properties(title=f'Daily Waste for {selected_flight}')

    # Ensure unique legend entries
    line_chart = line_chart.encode(
        color=alt.Color('Flight Type', scale=alt.Scale(domain=['Recyclable', 'Non-Recyclable', 'Total'], 
                                                           range=['#1f77b4', '#ff7f0e', '#2ca02c']),
                        legend=alt.Legend(title=None))  # Remove legend title
    )

    st.altair_chart(line_chart, use_container_width=True)

    # Monthly carbon emissions data
    data = {
        'Category': ['Total Emissions', 'Offsetting'],
        'Value (tonnes CO2)': [14.5, 6]
    }

    df = pd.DataFrame(data)

    # Bar chart for carbon emissions vs offsetting
    st.subheader("Carbon Emissions vs Offsetting for This Month")
    bar_chart = alt.Chart(df).mark_bar().encode(
        x='Category',
        y='Value (tonnes CO2)',
        color='Category',
        tooltip=['Category', 'Value (tonnes CO2)']
    ).properties(title='Carbon Emissions vs Offsetting')

    st.altair_chart(bar_chart, use_container_width=True)

    # Sample Monthly CO2 emissions data <-- (Just extra might not need or might change to daily)
    monthly_data = {
        'Month': [
            'January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October',
            'November', 'December'
        ],
        'CO2 Emissions (tonnes)': [
            12, 14, 13, 15, 14.5,
            12, 10, 11, 9, 7,
            6, 5
        ]
    }

    df_monthly = pd.DataFrame(monthly_data)

    # Current emissions and carbon-zero goal
    current_emissions = 6
    carbon_zero_goal = 100
    remaining_goal = carbon_zero_goal - current_emissions

    # Bar chart for carbon emissions vs offsetting
    data = {
        'Category': ['Total Emissions', 'Offsetting'],
        'Value (tonnes CO2)': [14.5, 6]
    }
    df = pd.DataFrame(data)

    # Shaded line graph for monthly CO2 emissions trends
    st.subheader("Monthly CO2 Emissions Trend")
    line_chart = alt.Chart(df_monthly).mark_area(opacity=0.5, interpolate='monotone').encode(
        x='Month',
        y='CO2 Emissions (tonnes)',
    ).properties(title='Monthly CO2 Emissions')

    line_chart += alt.Chart(df_monthly).mark_line(color='red').encode(
        x='Month',
        y='CO2 Emissions (tonnes)',
    )

    st.altair_chart(line_chart, use_container_width=True)

    # Donut chart for carbon-zero goal progress
    st.subheader("Progress Toward Carbon-Zero Goal")
    goal_data = pd.DataFrame({
        'Category': ['Achieved', 'Remaining'],
        'Value': [current_emissions, remaining_goal]
    })

    donut_chart = alt.Chart(goal_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='Value', type='quantitative'),
        color=alt.Color(field='Category', type='nominal', scale=alt.Scale(domain=['Achieved', 'Remaining'], range=['#4CAF50', '#FF5722'])),
        tooltip=['Category', 'Value']
    ).properties(title='Carbon-Zero Goal Progress')

    st.altair_chart(donut_chart, use_container_width=True)