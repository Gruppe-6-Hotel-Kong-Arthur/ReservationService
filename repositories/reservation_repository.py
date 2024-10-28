from database.connection import create_connection

def db_get_reservations():
    connection = create_connection()

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Reservations')

    reservations = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return reservations