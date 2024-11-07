import streamlit as st
import pandas as pd
import requests
import json
import sqlite3
from prophet import Prophet
import matplotlib.pyplot as plt
import base64


# ---- PREDICTIONS PAGE ----
def predictions_page():
    with open("logo.jpeg", "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    
    # Create two columns: one for the title and one for the logo
    col1, col2 = st.columns([7, 1])  # Adjust the ratio as needed

    with col1:
        st.title("Predictions")  # Title in the first column

    with col2:
        logo = data  # Adjust this path if necessary
        st.image(logo, width=150)  # Display logo in the second column

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.sidebar.button("Live Statistics", on_click=lambda: st.session_state.update({"page": "live_statistics"}))
    st.sidebar.button("5-day Summary", on_click=lambda: st.session_state.update({"page": "summary"}))
    st.sidebar.button("Waste Channels", on_click=lambda: st.session_state.update({"page": "waste_channels"}))
    st.sidebar.button("Predictions", on_click=lambda: st.session_state.update({"page": "predictions"}))

    # Connect to SQLite database
    conn = sqlite3.connect('flight_waste.db')

    # Fetch flights data
    flights_query = "SELECT flight_number, date, volume FROM flights"
    flights_data = pd.read_sql_query(flights_query, conn).values.tolist()

    # Fetch segregation data
    segregation_query = "SELECT date, time, type, volume FROM segregation"
    segregation_data = pd.read_sql_query(segregation_query, conn).values.tolist()

    # Fetch channel data
    channel_query = "SELECT date, channel, co2_emission FROM channel"
    channel_data = pd.read_sql_query(channel_query, conn).values.tolist()

    # Close the database connection
    conn.close()

    # Format the data into strings
    flights_str = "\n".join([f"ID: {id}, Date: {date}, Weight: {weight}" for id, date, weight in flights_data])
    segregation_str = "\n".join([f"Date: {date}, Time: {time}, Type: {type}, Weight: {weight}" 
                                  for date, time, type, weight in segregation_data])
    channel_str = "\n".join([f"Date: {date}, Type: {type}, Weight: {weight}" 
                              for date, type, weight in channel_data])

    # Prepare the payload for the Gemini API
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "You are an expert in analyzing waste data and providing insights. You will be given 3 different types of data, which serve the following purposes:\n"
                            "Flights Data: You are expected to provide insights on the timeframe one would usually expect high volumes of waste.\n"
                            "Segregation Data: You are expected to provide insights on the waste being segregated and if there are any interesting findings.\n"
                            "Channel Data: You are expected to provide insights on the channels and if there are any interesting findings of the emissions from the channels.\n"
                            "Flights Data:\n" + flights_str + "\n\n"
                            "Segregation Data:\n" + segregation_str + "\n\n"
                            "Channel Data:\n" + channel_str + "\n"
                            "Based on this data, you must provide summary insights in the form of bullet points, and limit yourself to a maximum of 3 bullet points, one for each data category. Do not mention anything about insufficient data."
                        )
                    }
                ]
            }
        ]
    }

    # API request to Gemini
    url = "https://developers.cathaypacific.com/hackathon-apigw/hackathon-middleware/v1/vertex-ai/google-gemini"
    api_key = "0Ws2MAmAseTl39JZLohswZZgWLCxpZ1K" 

    headers = {
        "apiKey": api_key,
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.26.10",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        
        # Extract the message content
        if "candidates" in response_data and response_data["candidates"]:
            message_content = response_data["candidates"][0]["content"]["parts"][0]["text"]
            st.subheader("💡 Insights from Gemini AI:")
            st.markdown(message_content)
        else:
            st.error("No response from our AI model. Please try again.")
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
    
    # Forecasting Future Waste per Channel
    st.subheader("📈 Waste Channel Forecasts")

    # Connect to the database
    conn = sqlite3.connect('flight_waste.db')
    df_channel = pd.read_sql_query("SELECT * FROM channel", conn)
    conn.close()

    # Convert 'date' column to datetime objects
    df_channel['date'] = pd.to_datetime(df_channel['date'])

    fig, axes = plt.subplots(1, 3, figsize=(20, 5))  

    for i, channel in enumerate(df_channel['channel'].unique()):
        df_channel_specific = df_channel[df_channel['channel'] == channel].copy()
        df_channel_specific = df_channel_specific.rename(columns={'date': 'ds', 'co2_emission': 'y'})

        model = Prophet()
        model.fit(df_channel_specific)
        
        future = model.make_future_dataframe(periods=14)
        forecast = model.predict(future)

        # Separate actual and forecast data
        df_channel_specific = df_channel_specific.rename(columns={'ds': 'date'}) 
        actual = df_channel_specific.set_index('date')
        forecast_only = forecast[forecast['ds'] > actual.index.max()]

        # Plotting
        axes[i].plot(actual.index, actual['y'], label='Actual')
        axes[i].plot(forecast_only['ds'], forecast_only['yhat'], 'o:', label='Forecast', linestyle='dotted') 
        axes[i].plot([actual.index[-1], forecast_only['ds'].iloc[0]],
                     [actual['y'].iloc[-1], forecast_only['yhat'].iloc[0]],
                     ':', color='gray', linewidth=1)  # Dotted gray connecting line

        axes[i].set_title(f"Forecast for {channel}")
        axes[i].legend()



    plt.tight_layout() 
    st.pyplot(fig)  