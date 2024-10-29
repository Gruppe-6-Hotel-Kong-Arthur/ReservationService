from database.connection import create_connection

# Get all reservations with days rented (end_date - start_date)
def db_get_reservations():
    connection = create_connection()

    cursor = connection.cursor()

    # Get all reservations and calculate days rented (end_date - start_date)
    cursor.execute('''  
    SELECT *, 
           (julianday(end_date) - julianday(start_date)) AS days_rented
    FROM Reservations
    ''')

    reservations = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return reservations

# Get a reservation by id with days rented (end_date - start_date)
def db_get_reservation(reservation_id):
    connection = create_connection()

    cursor = connection.cursor()
    # Get reservation and calculate days rented (end_date - start_date)
    cursor.execute('''
    SELECT *, 
           (julianday(end_date) - julianday(start_date)) AS days_rented 
    FROM Reservations 
    WHERE id = ?
    ''', (reservation_id,))
    reservation = cursor.fetchone()

    connection.close()
    return dict(reservation) if reservation else None

# Make a reservation 
def db_make_reservation(guest_id, room_id, season_id, start_date, end_date, price):
    connection = create_connection()

    cursor = connection.cursor()
    cursor.execute('INSERT INTO Reservations (guest_id, room_id, season_id, start_date, end_date, price) VALUES (?, ?, ?, ?, ?, ?)',
                    (guest_id, room_id, season_id, start_date, end_date, price))

    connection.commit()
    connection.close()