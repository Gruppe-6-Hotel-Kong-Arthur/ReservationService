from database.connection import create_connection

# Initializes database with tables and data
def init_db():
    _create_tables()

    # If data does not exist in database, insert base data and read CSV data
    # if not _check_data_exists():
    #    _insert_season_multiplier_data()
    #    _insert_room_type_data()
    #    _read_csv_data()

    print("Database initialized successfully.")

# Creates initial database tables
def _create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    # SQLite database reservations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        id INTEGER PRIMARY KEY,
        guest_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        season_id INTEGER NOT NULL,
        start_date TEXT NOT NULL CHECK (start_date >= CURRENT_DATE),
        end_date TEXT NOT NULL CHECK (end_date >= start_date),
        price REAL NOT NULL CHECK (price >= 0),
    )''')

    # Create SQLite indexes for Reservations table
    cursor.execute(''' CREATE INDEX IF NOT EXISTS guest_id_index ON Reservations (guest_id) ''')
    cursor.execute(''' CREATE INDEX IF NOT EXISTS room_id_index ON Reservations (room_id) ''')

    connection.commit()
    connection.close()
