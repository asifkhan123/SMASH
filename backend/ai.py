import requests
import json

# Define the API endpoint and keys (keys should be kept private and not pushed, but it is manually inserted as a quick solution for now)
url = "https://developers.cathaypacific.com/hackathon-apigw/hackathon-middleware/v1/vertex-ai/google-gemini"
api_key = "0Ws2MAmAseTl39JZLohswZZgWLCxpZ1K" 

# Sample data
flights_data = [
    ('CA101', '2024-11-01', 150.5),
    ('CA202', '2024-11-02', 180.2),
    ('BA202', '2024-11-03', 200.1)
]

segregation_data = [
    ('2024-11-01', '12:00', 'metal', 20.5),
    ('2024-11-01', '15:00', 'paper', 15.3),
    ('2024-11-03', '15:00', 'plastic', 5.0)
]

channel_data = [
    ('2024-11-01', 'landfill', 120.5),
    ('2024-11-02', 'recycling', 50.0)
]

# Format the data into strings
flights_str = "\n".join([f"ID: {id}, Date: {date}, Weight: {weight}" for id, date, weight in flights_data])
segregation_str = "\n".join([f"Date: {date}, Time: {time}, Type: {type}, Weight: {weight}" 
                              for date, time, type, weight in segregation_data])
channel_str = "\n".join([f"Date: {date}, Type: {type}, Weight: {weight}" 
                          for date, type, weight in channel_data])

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
                        "Based on this data, you must provide summary insights in the form of bullet points, and limit yourself to a maximum of 3 bullet points, one for each data category."
                    )
                }
            ]
        }
    ]
}

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
        print("Gemini's response:", message_content)
    else:
        print("No response from our AI model. Please try again.")
else:
    print(f"Error: {response.status_code}, {response.text}")