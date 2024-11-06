import sqlite3

conn = sqlite3.connect('flight_waste.db')
cur = conn.cursor()

# Function to print table schema
def print_table_schema(table_name):
    cur.execute(f'PRAGMA table_info({table_name})')
    columns = cur.fetchall()
    print(f"Structure of table '{table_name}':")
    for column in columns:
        print(column)
    print("\n")

# Check the structure of each table
tables = ['flights', 'segregation', 'channel']
for table in tables:
    print_table_schema(table)

conn.close()
