import random
import oracledb

# Función para conectarse a la base de datos
def get_connection():
    try:
        connection = oracledb.connect(
            user="SYSTEM", 
            password="0000", 
            dsn="localhost:1521/xe"
        )
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")


## ------------ PRESTAMO --------------- ##

def create_prestamo(solicitud_id, monto, tasa_interes):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO PRESTAMO (solicitud_id, monto, tasa_interes) VALUES (:1, :2, :3)"
    cursor.execute(sql, (solicitud_id, monto, tasa_interes))
    connection.commit()
    cursor.close()
    connection.close()

def read_prestamos():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM PRESTAMO"
    cursor.execute(sql)
    prestamos = cursor.fetchall()
    cursor.close()
    connection.close()
    return prestamos

def update_prestamo(prestamo_id, monto):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE PRESTAMO SET monto = :1 WHERE id = :2"
    cursor.execute(sql, (monto, prestamo_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_prestamo(prestamo_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM PRESTAMO WHERE id = :1"
    cursor.execute(sql, (prestamo_id,))
    connection.commit()
    cursor.close()
    connection.close()

def mostrarPrestamos():
    connection = get_connection()
    cursor = connection.cursor()
    SQL = '''
        select *
        from system.PRESTAMO
    '''
    cursor.execute(SQL)
    records = cursor.fetchall()
    for x in records:
        print(x)
