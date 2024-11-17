import random
from datetime import datetime
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

def create_prestamo(fecha_solicitud, empleado_id, monto, periodo):
    
    if not validar_monto(empleado_id, monto):
        print(f"No se pudo registrar la solicitud debido a un monto excedido para el empleado {empleado_id}.")
        return None

    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Convertir monto a flotante
        monto = float(monto)  # Asegurarse de que el monto sea un número flotante

        # Convertir periodo a entero
        periodo = int(periodo)

        # Asignar tasa de interés según el período
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

        # Asegúrate de que el monto se calcula correctamente
        monto_total = monto + (monto * tasa_interes / 100)  # Ajusta la tasa a porcentaje
        valor_cuota = monto_total / periodo
        
        # Calcular la fecha de desembolso
        if isinstance(fecha_solicitud, str):
            try:
                fecha_solicitud = datetime.strptime(fecha_solicitud, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                fecha_solicitud = datetime.strptime(fecha_solicitud, "%Y-%m-%d")

        mes_siguiente = fecha_solicitud.month % 12 + 1
        año_siguiente = fecha_solicitud.year + (fecha_solicitud.month // 12)

        fecha_desembolso = datetime(año_siguiente, mes_siguiente, 3)

        # Obtener el ID_PRESTAMO siguiente
        cursor.execute("SELECT MAX(ID_PRESTAMO) FROM PRESTAMO")
        max_id_prestamo = cursor.fetchone()[0]
        id_prestamo = max_id_prestamo + 1 if max_id_prestamo is not None else 1

        # Sentencia SQL para insertar
        sql = '''INSERT INTO PRESTAMO (ID_PRESTAMO, FECHA_SOLICITUD, EMPLEADO_ID, MONTO, PERIODO, ESTADO, TASA_INTERES, FECHA_DESEMBOLSO, VALOR_CUOTA) 
                 VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)'''

        # Ejecutar la inserción
        cursor.execute(sql, (id_prestamo, fecha_solicitud, empleado_id, monto_total, periodo, 'APROBADA', tasa_interes, fecha_desembolso, valor_cuota))

        # Commit para guardar los cambios
        connection.commit()
        print(f"Préstamo registrado correctamente con ID: {id_prestamo}")

    except Exception as e:
        print(f"Error al registrar el préstamo: {e}")
        connection.rollback()  # Revertir si ocurre un error

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
        
        # Convertir monto a flotante y luego a entero
        monto_float = float(monto)
        monto_int = int(monto_float)  # Si necesitas truncar el valor a entero

        if monto_int > limites_monto.get(tipo_empleado, 0):
            raise ValueError(f"El monto solicitado excede el límite permitido para el tipo de empleado {tipo_empleado}.")
        else:
            return True
    except Exception as e:
        print(f"Error al validar el monto: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def pasar_solicitud_prestamo(ID_PRESTAMO, fecha_solicitud, id_empleado, monto, periodo, estado, tasa_interes, fecha_desembolso):
    if not validar_monto(id_empleado, monto):
        print(f"No se pudo registrar el prestamo debido a un monto excedido para el empleado {id_empleado}.")
        return None

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Sentencia SQL para insertar
        sql = '''INSERT INTO PRESTAMO (ID_PRESTAMO, FECHA_SOLICITUD, EMPLEADO_ID, MONTO, PERIODO, ESTADO, TASA_INTERES, FECHA_DESEMBOLSO) 
                 VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'''  # Se corrigió la coma faltante

         # Comprobar si las fechas son ya objetos datetime
        if isinstance(fecha_solicitud, str):
            fecha_solicitud = datetime.strptime(fecha_solicitud, "%Y-%m-%d")  # Convertir si es cadena
        if isinstance(fecha_desembolso, str):
            fecha_desembolso = datetime.strptime(fecha_desembolso, "%Y-%m-%d")  # Convertir si es cadena

        # Ejecutar la inserción
        cursor.execute(sql, (int(ID_PRESTAMO), fecha_solicitud, int(id_empleado), int(monto), int(periodo), estado, float(tasa_interes), fecha_desembolso))

        # Commit para guardar los cambios
        connection.commit()
        
        print(f"Prestamo registrado correctamente con ID: {ID_PRESTAMO}")
        return ID_PRESTAMO  # Esto depende de cómo gestiones el ID en tu base de datos
        
    except ValueError as e:
        print(e)

    except Exception as e:
        print(f"Error al registrar el Prestamo: {e}")

    finally:
        cursor.close()
        connection.close()

def read_prestamos_todos():
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
    sql = "UPDATE PRESTAMO SET MONTO = :1, PERIODO = :2  WHERE ID_PRESTAMO = :3"
    cursor.execute(sql, (monto, periodo, prestamo_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_prestamo(prestamo_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM PRESTAMO WHERE ID_PRESTAMO = :1"
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

def read_prestamos(id_empleado):
    if not id_empleado:
        print("Error: id_empleado está vacío. No se puede ejecutar la consulta.")
        return []

    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRESTAMO WHERE EMPLEADO_ID = :1"
            print(f"Ejecutando SQL: {sql} con id_empleado = {id_empleado}")
            
            cursor.execute(sql, (id_empleado,))
            prestamos = cursor.fetchall()
            print(f"Préstamos obtenidos: {prestamos}")

    except Exception as e:
        print(f"Error al obtener préstamos: {e}")
        prestamos = []  # Cambiamos esto para que sea una lista vacía en caso de error
    finally:
        connection.close()

    return prestamos  # Devolver todos los registros


def read_prestamos_pendientes(id_empleado):
    if not id_empleado:
        print("Error: id_empleado está vacío. No se puede ejecutar la consulta.")
        return []

    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRESTAMO WHERE EMPLEADO_ID = :1 AND ESTADO = 'APROBADA'"
            print(f"Ejecutando SQL: {sql} con id_empleado = {id_empleado}")
            
            cursor.execute(sql, (id_empleado,))
            prestamos = cursor.fetchall()
            print(f"Préstamos obtenidos: {prestamos}")

            # Modificar la conversión para que retorne solo el ID del préstamo
            prestamos_lista = [prestamo[0] for prestamo in prestamos]  # Solo el primer campo (ID del préstamo)
            print(f"IDs de préstamos obtenidos: {prestamos_lista}")

    except Exception as e:
        print(f"Error al obtener préstamos: {e}")
        prestamos_lista = []
    finally:
        connection.close()

    return prestamos_lista  # Devuelve la lista de préstamos

def obtener_cuota_prestamo (id_prestamo):
    if not id_prestamo:
        print("Error: id_prestamo está vacío. No se puede ejecutar la consulta.")
        return []

    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT VALOR_CUOTA FROM PRESTAMO WHERE ID_PRESTAMO    = :1"
        
            cursor.execute(sql, (id_prestamo,))
            prestamos = cursor.fetchall()
            print(f"Valor Cuota préstamos obtenidos: {prestamos}")

            # Modificar la conversión para que retorne solo el ID del préstamo
            valor_cuota = prestamos[0] # Solo el primer campo (ID del préstamo)
            print(f"valor cuota obtenido: {valor_cuota}")

    except Exception as e:
        print(f"Error al obtener préstamos: {e}")
        prestamos_lista = []
    finally:
        connection.close()

    return valor_cuota

def obtener_cantidad_cuotas_prestamo(id_prestamo):
    if not id_prestamo:
        print("Error: id_prestamo está vacío. No se puede ejecutar la consulta.")
        return 0  # Retornar 0 o un valor por defecto en caso de error

    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT PERIODO FROM PRESTAMO WHERE ID_PRESTAMO = :1"
        
            cursor.execute(sql, (id_prestamo,))
            prestamos = cursor.fetchall()
            print(f"Numero de cuotas obtenidos: {prestamos}")

            if prestamos:  # Verifica si se obtuvo algún resultado
                numero_cuotas = prestamos[0][0]  # Acceder al primer elemento de la primera tupla
                print(f"Numero de cuotas obtenidos: {numero_cuotas}")
            else:
                numero_cuotas = 0  # Si no hay resultados, retorna 0 o un valor por defecto

    except Exception as e:
        print(f"Error al obtener préstamos: {e}")
        numero_cuotas = 0  # Retornar 0 en caso de excepción
    finally:
        connection.close()

    return numero_cuotas  # Asegúrate de retornar solo el número de cuotas

def prestamo_finalizado(id_prestamo):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE PRESTAMO SET ESTADO = :1  WHERE ID_PRESTAMO = :2"
    cursor.execute(sql, ('PAGADO',id_prestamo))
    connection.commit()
    cursor.close()
    connection.close()