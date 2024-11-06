import sqlite3

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

flights_data = [
    ('AA101', '2024-11-01', 'On Time', 150.5),
    ('BA202', '2024-11-02', 'On Time', 180.2),
    ('CA303', '2024-11-03', 'Delayed', 200.1)
]

segregation_data = [
    ('2024-11-01', '12:00', 'plastic', 20.5),
    ('2024-11-01', '13:00', 'metal', 5.0),
    ('2024-11-02', '14:00', 'paper', 15.3),
    ('2024-11-03', '15:00', 'plastic', 22.1)
]

channel_data = [
    ('2024-11-01', 'landfill', 120.5),
    ('2024-11-01', 'recycling', 80.5),
    ('2024-11-02', 'landfill', 130.2),
    ('2024-11-02', 'SAF', 50.0)
]

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
