import sqlite3
import random
import datetime


# Connect to SQLite database
conn = sqlite3.connect('flight_waste.db')
cur = conn.cursor()

# Create tables
cur.execute('''
CREATE TABLE IF NOT EXISTS flights (
    flight_number TEXT NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    volume REAL NOT NULL,
    PRIMARY KEY (flight_number, date)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS segregation (
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    type TEXT NOT NULL,
    volume REAL NOT NULL,
    PRIMARY KEY (date, time, type)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS channel (
    date TEXT NOT NULL,
    channel TEXT NOT NULL,
    co2_emission REAL NOT NULL,
    PRIMARY KEY (date, channel)
)
''')

# Sample data for tables


# Flights Data
flights_data = []
start_date = datetime.date(2024, 11, 1)
end_date = datetime.date(2024, 11, 30)
flight_numbers = [f"UO{i:03}" for i in range(1, 31)]  # Example flight numbers
statuses = ["On Time", "Delayed", "Cancelled"]

current_date = start_date
while current_date <= end_date:
    flight_number = random.choice(flight_numbers)
    status = random.choice(statuses)
    volume = random.uniform(100, 250)  # Example volume range
    flights_data.append((flight_number, current_date.strftime('%Y-%m-%d'), status, volume))
    current_date += datetime.timedelta(days=1)

# Segregation Data
segregation_data = []
start_date = datetime.date(2024, 11, 1)
end_date = datetime.date(2024, 11, 30)
times = [f"{hour:02}:00" for hour in range(8, 20)] # Example times (8 AM to 8 PM)
types = ["landfill, recyclable, organic compost"]

current_date = start_date
while current_date <= end_date:
    for _ in range(random.randint(1, 5)): # Random number of entries per day (1 to 5)
        time = random.choice(times)
        type = random.choice(types)
        volume = random.uniform(1, 30)  # Example volume range
        segregation_data.append((current_date.strftime('%Y-%m-%d'), time, type, volume))
    current_date += datetime.timedelta(days=1)

start_date = datetime.date(2024, 11, 1)
end_date = datetime.date(2024, 11, 30)
channels = ['landfill', 'recycling', 'SAF']
channel_data = []
current_date = start_date
while current_date <= end_date:
    for channel in channels:
        if channel == 'landfill':
            co2_emission = random.uniform(150, 180)
        elif channel == 'recycling':
            co2_emission = random.uniform(90, 100)
        else:
            co2_emission = random.uniform(80, 120)
        channel_data.append((current_date.strftime('%Y-%m-%d'), channel, co2_emission))
    current_date += datetime.timedelta(days=1)

# Insert data into tables
cur.executemany('''
INSERT INTO flights (flight_number, date, status, volume)
VALUES (?, ?, ?, ?)
''', flights_data)

cur.executemany('''
INSERT INTO segregation (date, time, type, volume)
VALUES (?, ?, ?, ?)
''', segregation_data)

cur.executemany('''
INSERT INTO channel (date, channel, co2_emission)
VALUES (?, ?, ?)
''', channel_data)


conn.commit()
conn.close()
