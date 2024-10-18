import oracledb
import datetime

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

## ----------- SOLICITUD DE PRÉSTAMO ----------- ##

# Validar el monto según el tipo de empleado
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

# Registrar solicitud
def registrar_solicitud(fecha_solicitud, empleado_id, monto, periodo):
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

        # SQL para insertar la solicitud
        sql = '''INSERT INTO SOLICITUD (FECHA_SOLICITUD, ID_EMPLEADO, MONTO_SOLICITADO, PERIODO_MESES, ESTADO, TASA_INTERES) 
                 VALUES (:1, :2, :3, :4, :5, :6) RETURNING ID_SOLICITUD INTO :7'''
        
        # Obtener el ID de la solicitud generada
        id_solicitud = cursor.var(oracledb.NUMBER)
        
        cursor.execute(sql, (fecha_solicitud, empleado_id, monto, periodo, 'Pendiente', tasa_interes, id_solicitud))
        connection.commit()
        
        print(f"Solicitud registrada correctamente con ID: {id_solicitud.getvalue()}")
        return id_solicitud.getvalue()
    except ValueError as e:
        print(e)

    except Exception as e:
        print(f"Error al registrar la solicitud: {e}")

    finally:
        cursor.close()
        connection.close()

# Leer una solicitud
def leer_solicitud(id_solicitud):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "SELECT * FROM SOLICITUD WHERE ID_SOLICITUD = :1"
        cursor.execute(sql, (id_solicitud,))
        solicitud = cursor.fetchone()
        
        if solicitud:
            print(solicitud)
        else:
            print(f"No se encontró ninguna solicitud con ID: {id_solicitud}")
    except Exception as e:
        print(f"Error al leer la solicitud: {e}")
    finally:
        cursor.close()
        connection.close()

# Actualizar solicitud y aprobar si corresponde
def actualizar_solicitud(id_solicitud, nuevo_estado):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Validar que el nuevo estado esté dentro de los valores permitidos
        estados_permitidos = ['Pendiente', 'En estudio', 'Aprobada', 'Rechazada']
        if nuevo_estado not in estados_permitidos:
            raise ValueError(f"Estado '{nuevo_estado}' no permitido. Solo se permiten: {estados_permitidos}")
        
        # Actualizar el estado de la solicitud
        sql_update = "UPDATE SOLICITUD SET ESTADO = :1 WHERE ID_SOLICITUD = :2"
        cursor.execute(sql_update, (nuevo_estado, id_solicitud))
        
        # Si el nuevo estado es "aprobada", insertar un préstamo
        if nuevo_estado == 'aprobada':
            # Obtener los datos de la solicitud
            sql_select = "SELECT FECHA_SOLICITUD, ID_EMPLEADO, MONTO_SOLICITADO, PERIODO_MESES, TASA_INTERES FROM SOLICITUD WHERE ID_SOLICITUD = :1"
            cursor.execute(sql_select, (id_solicitud,))
            solicitud = cursor.fetchone()
            
            if solicitud:
                fecha_solicitud, empleado_id, monto, periodo, tasa_interes = solicitud

                # Validar que los valores de la solicitud cumplen con las restricciones
                if not fecha_solicitud or not empleado_id or monto <= 0 or periodo not in [24, 36, 48, 60, 72]:
                    raise ValueError("Los valores de la solicitud no son válidos según las restricciones.")
                
                # Calcular la fecha de desembolso (día 3 del mes siguiente a la aprobación)
                fecha_desembolso = (fecha_solicitud.replace(day=1) + datetime.timedelta(days=32)).replace(day=3)
                
                # Insertar en la tabla PRESTAMO
                sql_insert_prestamo = '''
                    INSERT INTO PRESTAMO (ID_SOLICITUD, FECHA_SOLICITUD, EMPLEADO_ID, MONTO, PERIODO, ESTADO, TASA_INTERES, FECHA_DESEMBOLSO)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                '''
                cursor.execute(sql_insert_prestamo, (
                    id_solicitud, fecha_solicitud, empleado_id, monto, periodo, 'APROBADO', tasa_interes, fecha_desembolso
                ))
                
                print(f"Préstamo generado correctamente para la solicitud con ID '{id_solicitud}'.")
            else:
                print(f"No se encontró la solicitud con ID {id_solicitud} para aprobar.")
        
        # Confirmar los cambios
        connection.commit()
        print(f"Solicitud con ID '{id_solicitud}' actualizada correctamente.")
    
    except oracledb.DatabaseError as e:
        print(f"Error al actualizar la solicitud o insertar el préstamo: {e}")
        connection.rollback()
    
    except ValueError as ve:
        print(f"Error de validación: {ve}")
    
    finally:
        cursor.close()
        connection.close()

# Eliminar solicitud
def eliminar_solicitud(id_solicitud):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "DELETE FROM SOLICITUD WHERE ID_SOLICITUD = :1"
        cursor.execute(sql, (id_solicitud,))
        connection.commit()
        print(f"Solicitud con ID '{id_solicitud}' eliminada correctamente.")
    except Exception as e:
        print(f"Error al eliminar la solicitud: {e}")
    finally:
        cursor.close()
        connection.close()

# Mostrar todas las solicitudes
def mostrar_solicitudes():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM SOLICITUD")
        records = cursor.fetchall()
        for record in records:
            print(record)
    except Exception as e:
        print(f"Error al mostrar las solicitudes: {e}")
    finally:
        cursor.close()
        connection.close()

def update_solicitud(solicitud_id, monto, periodo):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE SOLICITUD SET MONTO_SOLICITADO = :1, PERIODO_MESES = :2 WHERE ID_SOLICITUD = :3"
    cursor.execute(sql, (monto, periodo, solicitud_id))
    connection.commit()
    cursor.close()
    connection.close()

