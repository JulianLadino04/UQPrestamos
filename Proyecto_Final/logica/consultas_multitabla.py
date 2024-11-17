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

# ----------- MULTITABLA ----------- #

def obtener_pagos_cliente(id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''SELECT p.ID_PRESTAMO, a.VALOR_PAGO, a.MOROSO, a.NUMERO_CUOTA
                 FROM EMPLEADO e
                 INNER JOIN PRESTAMO p ON e.ID_EMPLEADO = p.EMPLEADO_ID
                 INNER JOIN PAGO a ON p.ID_PRESTAMO = a.ID_PRESTAMO
                 WHERE e.ID_EMPLEADO = :1'''  # Asegúrate de usar el campo correcto
        cursor.execute(sql, (id,))
        resultados = cursor.fetchall()  # Devuelve todos los resultados

        # Retorna solo los valores necesarios para la tabla
        return [(prestamo[0], prestamo[1], prestamo[2], prestamo[3]) for prestamo in resultados]  # (ID_PRESTAMO, VALOR_PAGO, MOROSO, NUMERO_CUOTA)

    except Exception as e:
        print(f"Error al obtener los pagos: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def obtener_pagos_prestamo(id_prestamo):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''SELECT a.ID_PRESTAMO, a.VALOR_PAGO, a.MOROSO, a.NUMERO_CUOTA
                 FROM PAGO a
                 WHERE a.ID_PRESTAMO = :1'''  # Filtra por ID_PRESTAMO
        
        cursor.execute(sql, (id_prestamo,))
        resultados = cursor.fetchall()  # Devuelve todos los resultados

        # Retorna solo los valores necesarios para la tabla
        return [(pago[0], pago[1], pago[2], pago[3]) for pago in resultados]  # (ID_PRESTAMO, VALOR_PAGO, MOROSO, NUMERO_CUOTA)

    except Exception as e:
        print(f"Error al obtener los pagos para el préstamo con ID {id_prestamo}: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
