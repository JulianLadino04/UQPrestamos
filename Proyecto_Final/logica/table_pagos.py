import oracledb
from datetime import datetime

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

def registrar_pago(numero_prestamo, numero_pago, fecha_pago, valor):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Verificar que la fecha de pago sea antes del 10 de cada mes
        if fecha_pago.day > 10:
            moroso = 'Y'
        else:
            moroso = 'N'
        
        sql = '''INSERT INTO PAGO (ID_PRESTAMO, NUMERO_CUOTA, FECHA_PAGO, VALOR_PAGO, MOROSO) 
                 VALUES (:1, :2, :3, :4, :5)'''
        cursor.execute(sql, (numero_prestamo, numero_pago, fecha_pago, valor, moroso))
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