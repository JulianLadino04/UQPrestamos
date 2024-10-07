import random
import oracledb

# Función para conectarse a la base de datos
def get_connection():
    try:
        connection = oracledb.connect(
            user="SYSTEM", 
            password="1091884402", 
            dsn="localhost:1521/xe"
        )
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")


## ------------ PRESTAMO --------------- ##

def create_prestamo(fecha_solicitud, empleado_id, monto, periodo, tasa_interes, fecha_desembolso):
    if not validar_monto(empleado_id, monto):
        print(f"No se pudo registrar la solicitud debido a un monto excedido para el empleado {empleado_id}.")
        return None

    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Convertir periodo a entero
        periodo = int(periodo)

        # Asignar tasa de interés según el período usando if-elif-else
        if periodo == 24:
            tasa_interes = 7.0
        elif periodo == 36:
            tasa_interes = 7.5
        elif periodo == 48:
            tasa_interes = 8.0
        elif periodo == 60:
            tasa_interes = 8.3
        elif periodo == 72:
            tasa_interes = 8.6
        else:
            raise ValueError(f"Periodo no válido: {periodo}")
    
        print(f"Tasa de interés asignada: {tasa_interes}%")

        # Sentencia SQL para insertar
        sql = '''INSERT INTO SOLICITUD (ID_SOLICITUD, FECHA_SOLICITUD, ID_EMPLEADO, MONTO_SOLICITADO, PERIODO_MESES, ESTADO, TASA_INTERES, FECHA_DESEMBOLSO) 
         VALUES (:1, :2, :3, :4, :5, :6, :7 :8) RETURNING ID_SOLICITUD INTO :8'''

        # Obtener el ID de la solicitud generada (si es necesario)
        id_solicitud = cursor.var(oracledb.NUMBER)

        # Ejecutar la inserción
        cursor.execute(sql, (id_solicitud, fecha_solicitud, empleado_id, monto, periodo, 'Aprobada', tasa_interes, fecha_desembolso))
        
        print(f"Solicitud registrada correctamente con ID: {id_solicitud.getvalue()}")
        return id_solicitud.getvalue()
    except ValueError as e:
        print(e)

    except Exception as e:
        print(f"Error al registrar la solicitud: {e}")

    finally:
        cursor.close()
        connection.close()

def validar_monto(empleado_id, monto):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "SELECT CARGO FROM EMPLEADO WHERE ID_EMPLEADO = :1"
        cursor.execute(sql, (empleado_id,))
        tipo_empleado = cursor.fetchone()[0]
        
        limites_monto = {
            'Operario': 10000000,
            'Administrativo': 15000000,
            'Ejecutivo': 20000000,
            'Otros': 12000000
        }
        
        if int(monto) > limites_monto.get(tipo_empleado, 0):
            raise ValueError(f"El monto solicitado excede el límite permitido para el tipo de empleado {tipo_empleado}.")
        else:
            return True
    except Exception as e:
        print(f"Error al validar el monto: {e}")
        return False
    finally:
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

def update_prestamo(prestamo_id, monto, periodo):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE PRESTAMO SET MONTO = :1, PERIODO = :2  WHERE ID_SOLICITUDs = :3"
    cursor.execute(sql, (monto, periodo, prestamo_id))
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
