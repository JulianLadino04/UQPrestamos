import oracledb
from datetime import datetime

def get_connection():
    try:
        connection = oracledb.connect(
            user="SYSTEM", 
            password="Arango2004", 
            dsn="localhost:1521/xe"
        )
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")
        
def registrar_pago(numero_prestamo, numero_pago, fecha_pago, valor):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Convertir la fecha de pago de str a datetime
        fecha_pago_dt = datetime.strptime(fecha_pago, "%Y-%m-%d")

        # Verificar que la fecha de pago sea antes del 10 de cada mes
        if fecha_pago_dt.day > 10:
            moroso = 'Y'
        else:
            moroso = 'N'
        
        sql = '''INSERT INTO PAGO (ID_PRESTAMO, NUMERO_CUOTA, FECHA_PAGO, VALOR_PAGO, MOROSO) 
                 VALUES (:1, :2, :3, :4, :5)'''
        cursor.execute(sql, (numero_prestamo, numero_pago, fecha_pago_dt, valor, moroso))
        connection.commit()
        print("Pago registrado correctamente.")
    except Exception as e:
        print(f"Error al registrar el pago: {e}")
    finally:
        cursor.close()
        connection.close()

def leer_pagos():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PAGO")
        pagos = cursor.fetchall()
        for pago in pagos:
            print(pago)
    except Exception as e:
        print(f"Error al leer pagos: {e}")
    finally:
        cursor.close()
        connection.close()

def mostrar_morosos():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''SELECT NUMERO_PRESTAMO, NUMERO_PAGO, FECHA_PAGO, VALOR 
                 FROM PAGO 
                 WHERE MOROSO = 'Y' '''
        cursor.execute(sql)
        morosos = cursor.fetchall()
        
        if morosos:
            print("Pagos morosos:")
            for pago in morosos:
                print(pago)
        else:
            print("No hay pagos morosos.")
    except Exception as e:
        print(f"Error al mostrar los morosos: {e}")
    finally:
        cursor.close()
        connection.close()
        
def enviar_pagos_prestamo(id_prestamo):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''SELECT * 
                 FROM PAGO 
                 WHERE ID_PRESTAMO = :1'''
        cursor.execute(sql, (id_prestamo,))
        
        # Obtener nombres de columnas
        columns = [col[0] for col in cursor.description]
        
        # Convertir las filas a una lista de diccionarios
        pagos = []
        for row in cursor.fetchall():
            pagos.append(dict(zip(columns, row)))
        
        return pagos  # Ahora 'pagos' es una lista de diccionarios
    except Exception as e:
        print(f"Error al obtener pagos: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
        
def prestamo_finalizado(id_prestamo):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''UPDATE PRESTAMO
        SET ESTADO =:1 WHERE ID_PRESTAMO =:2'''
        cursor.execute(sql, ('PAGADA',id_prestamo))
        # Confirmar los cambios en la base de datos
        connection.commit()
        print("Prestamo actualizado correctamente.") # Ahora 'pagos' es una lista de diccionarios
    except Exception as e:
        print(f"Error al el prestamo: {e}")
        return None
    finally:
        cursor.close()
        connection.close()