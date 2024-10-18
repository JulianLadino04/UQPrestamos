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

def create_prestamo(fecha_solicitud, empleado_id, monto, periodo, fecha_desembolso):
    if not validar_monto(empleado_id, monto):
        print(f"No se pudo registrar la solicitud debido a un monto excedido para el empleado {empleado_id}.")
        return None

    connection = get_connection()
    cursor = connection.cursor()
    
    try:
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

        # Sentencia SQL para insertar
        sql = '''INSERT INTO PRESTAMO (ID_SOLICITUD, FECHA_SOLICITUD, EMPLEADO_ID, MONTO, PERIODO, ESTADO, TASA_INTERES, FECHA_DESEMBOLSO) 
                 VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'''  # Se corrigió la coma faltante

        # Obtener el ID de la solicitud generada
        id_solicitud = cursor.var(oracledb.NUMBER)

         # Comprobar si las fechas son ya objetos datetime
        if isinstance(fecha_solicitud, str):
            fecha_solicitud = datetime.strptime(fecha_solicitud, "%Y-%m-%d")  # Convertir si es cadena
        if isinstance(fecha_desembolso, str):
            fecha_desembolso = datetime.strptime(fecha_desembolso, "%Y-%m-%d")  # Convertir si es cadena

        # Ejecutar la inserción
        cursor.execute(sql, (id_solicitud, fecha_solicitud, empleado_id, monto, periodo, 'Aprobada', tasa_interes, fecha_desembolso))

        # Commit para guardar los cambios
        connection.commit()
        
        # Si ID_SOLICITUD es autoincremental, no se puede obtener aquí directamente.
        # Esto podría necesitar una consulta para obtener el último ID insertado si no se asigna automáticamente.
        print(f"Prestamo registrado correctamente con ID: {id_solicitud}")
        return id_solicitud  # Esto depende de cómo gestiones el ID en tu base de datos
        
    except ValueError as e:
        print(e)

    except Exception as e:
        print(f"Error al registrar el Prestamo: {e}")

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

def pasar_solicitud_prestamo(id_solicitud, fecha_solicitud, id_empleado, monto, periodo, estado, tasa_interes, fecha_desembolso):
    if not validar_monto(id_empleado, monto):
        print(f"No se pudo registrar el prestamo debido a un monto excedido para el empleado {id_empleado}.")
        return None

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Sentencia SQL para insertar
        sql = '''INSERT INTO PRESTAMO (ID_SOLICITUD, FECHA_SOLICITUD, EMPLEADO_ID, MONTO, PERIODO, ESTADO, TASA_INTERES, FECHA_DESEMBOLSO) 
                 VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'''  # Se corrigió la coma faltante

         # Comprobar si las fechas son ya objetos datetime
        if isinstance(fecha_solicitud, str):
            fecha_solicitud = datetime.strptime(fecha_solicitud, "%Y-%m-%d")  # Convertir si es cadena
        if isinstance(fecha_desembolso, str):
            fecha_desembolso = datetime.strptime(fecha_desembolso, "%Y-%m-%d")  # Convertir si es cadena

        # Ejecutar la inserción
        cursor.execute(sql, (int(id_solicitud), fecha_solicitud, int(id_empleado), int(monto), int(periodo), estado, float(tasa_interes), fecha_desembolso))

        # Commit para guardar los cambios
        connection.commit()
        
        print(f"Prestamo registrado correctamente con ID: {id_solicitud}")
        return id_solicitud  # Esto depende de cómo gestiones el ID en tu base de datos
        
    except ValueError as e:
        print(e)

    except Exception as e:
        print(f"Error al registrar el Prestamo: {e}")

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
    sql = "DELETE FROM PRESTAMO WHERE ID_SOLICITUD = :1"
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

    # Convertir id_empleado a número, si es necesario
    id_empleado = int(id_empleado)  # Convertir a entero si es una cadena

    # Establecer conexión con la base de datos
    connection = get_connection()
    cursor = connection.cursor()

    # Definir la consulta SQL para obtener préstamos del empleado
    sql = "SELECT * FROM PRESTAMO WHERE EMPLEADO_ID = :1"
    print(f"Ejecutando SQL: {sql} con id_empleado = {id_empleado}")  # Depuración
    print(f"id_empleado: {id_empleado}, tipo: {type(id_empleado)}")

    try:
        # Ejecutar la consulta
        cursor.execute(sql, (id_empleado,))
        
        # Obtener todos los préstamos
        prestamos = cursor.fetchall() 
        print(f"Préstamos obtenidos: {prestamos}")  # Verifica el contenido
        
        # Convertir cada fila obtenida en una lista
        prestamos_lista = []
        for prestamo in prestamos:
            prestamos_lista.append(list(prestamo))  # Convertir la tupla en lista y añadirla a la lista general
        
        # Depuración: Imprimir los resultados obtenidos
        print(f"Préstamos obtenidos: {prestamos_lista}")
    
    except Exception as e:
        print(f"Error al obtener préstamos: {e}")  # Manejo de errores
        prestamos_lista = []  # Inicializar como lista vacía en caso de error
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

    # Devolver la lista de préstamos
    return prestamos_lista




