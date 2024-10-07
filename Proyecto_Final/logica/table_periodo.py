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

## ----------- PERIODO ----------- ##

def crear_periodo(cuotas, tasa_interes):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''INSERT INTO PERIODO (CUOTAS, TASA_INTERES) 
                 VALUES (:1, :2)'''
        cursor.execute(sql, (cuotas, tasa_interes))
        connection.commit()
        print(f"Periodo de '{cuotas}' cuotas con interés de '{tasa_interes}' creado correctamente.")
    except Exception as e:
        print(f"Error al crear el periodo: {e}")
    finally:
        cursor.close()
        connection.close()


def leer_periodos():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PERIODO")
        periodos = cursor.fetchall()
        for periodo in periodos:
            print(periodo)
    except Exception as e:
        print(f"Error al leer periodos: {e}")
    finally:
        cursor.close()
        connection.close()


def actualizar_periodo(cuotas, nuevo_tasa_interes=None):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        if nuevo_tasa_interes is not None:
            sql = "UPDATE PERIODO SET TASA_INTERES = :1 WHERE CUOTAS = :2"
            cursor.execute(sql, (nuevo_tasa_interes, cuotas))
            connection.commit()
            print(f"Periodo de '{cuotas}' cuotas actualizado con nuevo interés de '{nuevo_tasa_interes}'.")
    except Exception as e:
        print(f"Error al actualizar el periodo: {e}")
    finally:
        cursor.close()
        connection.close()


def eliminar_periodo(cuotas):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM PERIODO WHERE CUOTAS = :1"
        cursor.execute(sql, (cuotas,))
        connection.commit()
        print(f"Periodo de '{cuotas}' cuotas eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el periodo: {e}")
    finally:
        cursor.close()
        connection.close()


def buscar_por_cuotas(cuotas):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT TASA_INTERES FROM PERIODO WHERE CUOTAS = :1"
        cursor.execute(sql, (cuotas,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return "No se encontró un periodo con esas cuotas."
    except Exception as e:
        print(f"Error al buscar por cuotas: {e}")
    finally:
        cursor.close()
        connection.close()
