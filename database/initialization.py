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

    # cursor.execute(''' database here ''')

    connection.commit()
    connection.close()
    pass
