import pandas as pd
import os
from datetime import datetime, timedelta
from database.connection import create_connection

# Map of room type names to their room IDs
room_type_map = {
    "Spa Executive": 1,
    "Grand Lit": 2,
    "Standard Single": 3,
    "LOFT Suite": 4,
    "Suite": 5,
    "Standard Double": 6,
    "Junior Suite": 7,
    "Superior Double": 8
}

def init_db():
    _create_tables()
    if not _check_data_exists():
        _read_csv_data()
    print("Database initialized successfully.")

def _create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
        id INTEGER PRIMARY KEY,
        guest_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        season_id INTEGER NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        price REAL NOT NULL CHECK (price >= 0)
    )''')
    
    cursor.execute('''CREATE INDEX IF NOT EXISTS guest_id_index ON Reservations (guest_id)''')
    cursor.execute('''CREATE INDEX IF NOT EXISTS room_id_index ON Reservations (room_id)''')
    
    connection.commit()
    connection.close()

def _check_data_exists():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Reservations")
    count = cursor.fetchone()[0]
    connection.close()
    return count > 0

def _get_season_id(season):
    season_mapping = {'low': 1, 'mid': 2, 'high': 3}
    return season_mapping.get(season.lower(), 1)

def _generate_dates(days_rented):
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=int(days_rented))
    return start_date.isoformat(), end_date.isoformat()

def _read_csv_data():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                           'csv/international_names_with_rooms_1000.csv')
    data = pd.read_csv(csv_path)
    
    connection = create_connection()
    cursor = connection.cursor()
    
    guest_id = 1
    
    try:
        for _, row in data.iterrows():
            start_date, end_date = _generate_dates(row['Days Rented'])
            season_id = _get_season_id(row['Season'])
            
            # Determine room_id from type_name
            room_type_name = row['Room Type']  # Adjust column name as per CSV
            room_id = room_type_map.get(room_type_name)

            if room_id is None:
                print(f"Error: Room type '{room_type_name}' not found.")
                continue
            
            cursor.execute('''
                INSERT INTO Reservations (
                    guest_id, room_id, season_id, 
                    start_date, end_date, price
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                guest_id, 
                room_id,
                season_id,
                start_date,
                end_date,
                float(row['Price'])
            ))
            
            guest_id += 1
        
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    connection.close()
