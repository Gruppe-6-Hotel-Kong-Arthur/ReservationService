from database.connection import create_connection

def db_get_reservations():
    connection = create_connection()

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Reservations')

    reservations = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return reservations

def db_get_reservation(reservation_id):
    connection = create_connection()

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Reservations WHERE id = ?', (reservation_id,))

    reservation = cursor.fetchone()

    connection.close()
    return reservation


def db_make_reservation(guest_id, room_id, season_id, start_date, end_date):
    connection = create_connection()

    cursor = connection.cursor()
    cursor.execute('INSERT INTO Reservations (guest_id, room_id, season_id, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
                    (guest_id, room_id, season_id, start_date, end_date))

    connection.commit()
    connection.close()