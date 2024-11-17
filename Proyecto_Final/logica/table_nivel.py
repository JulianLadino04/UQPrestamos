import oracledb

# Función para conectarse a la base de datos
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

## ----------- NIVEL ----------- ##

def crear_nivel(nombre):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Verificar si el nivel ya existe
        cursor.execute("SELECT COUNT(*) FROM NIVEL WHERE NOMBRE = :1", (nombre,))
        if cursor.fetchone()[0] > 0:
            print("El nombre del nivel ya existe. Elija otro.")
            return

        sql = '''INSERT INTO NIVEL (NOMBRE) 
                 VALUES (:1)'''
        cursor.execute(sql, (nombre,))
        connection.commit()
        print(f"Nivel '{nombre}' creado correctamente.")
    except Exception as e:
        print(f"Error al crear el nivel: {e}")
    finally:
        cursor.close()
        connection.close()


def leer_niveles():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM NIVEL")
        niveles = cursor.fetchall()
        for nivel in niveles:
            print(nivel)
    except Exception as e:
        print(f"Error al leer niveles: {e}")
    finally:
        cursor.close()
        connection.close()


def actualizar_nivel(nombre_actual, nuevo_nombre):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        if nuevo_nombre:
            sql = "UPDATE NIVEL SET NOMBRE = :1 WHERE NOMBRE = :2"
            cursor.execute(sql, (nuevo_nombre, nombre_actual))
            connection.commit()
            print(f"Nivel '{nombre_actual}' actualizado correctamente a '{nuevo_nombre}'.")
        else:
            print("No se ha proporcionado un nuevo nombre para actualizar.")
    except Exception as e:
        print(f"Error al actualizar el nivel: {e}")
    finally:
        cursor.close()
        connection.close()


def eliminar_nivel(nombre):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM NIVEL WHERE NOMBRE = :1"
        cursor.execute(sql, (nombre,))
        connection.commit()
        print(f"Nivel '{nombre}' eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el nivel: {e}")
    finally:
        cursor.close()
        connection.close()


def mostrar_niveles():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT * FROM NIVEL"
        cursor.execute(sql)
        records = cursor.fetchall()
        for x in records:
            print(x)
    except Exception as e:
        print(f"Error al mostrar niveles: {e}")
    finally:
        cursor.close()
        connection.close()
    
def obtener_niveles():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT * FROM NIVEL WHERE nombre != 'Principal'"
        cursor.execute(sql)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error al mostrar niveles: {e}")
    finally:
        cursor.close()
        connection.close()
    
