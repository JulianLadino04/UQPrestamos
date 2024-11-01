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


## ----------- ESTADO ----------- ##

# Crear un nuevo estado
def crear_estado(nombre_estado):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''INSERT INTO ESTADO (NOMBRE_ESTADO) 
                 VALUES (:1)'''
        cursor.execute(sql, (nombre_estado,))
        connection.commit()
        print(f"Estado '{nombre_estado}' creado correctamente.")
    except Exception as e:
        print(f"Error al crear el estado: {e}")
    finally:
        cursor.close()
        connection.close()

# Leer todos los estados
def leer_estados():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM ESTADO")
        estados = cursor.fetchall()
        for estado in estados:
            print(estado)
    except Exception as e:
        print(f"Error al leer los estados: {e}")
    finally:
        cursor.close()
        connection.close()

# Actualizar un estado por nombre
def actualizar_estado(nombre_estado, nuevo_nombre_estado):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = '''UPDATE ESTADO 
                 SET NOMBRE_ESTADO = :1 
                 WHERE NOMBRE_ESTADO = :2'''
        cursor.execute(sql, (nuevo_nombre_estado, nombre_estado))
        connection.commit()
        print(f"Estado '{nombre_estado}' actualizado correctamente a '{nuevo_nombre_estado}'.")
    except Exception as e:
        print(f"Error al actualizar el estado: {e}")
    finally:
        cursor.close()
        connection.close()

# Eliminar un estado por nombre
def eliminar_estado(nombre_estado):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM ESTADO WHERE NOMBRE_ESTADO = :1"
        cursor.execute(sql, (nombre_estado,))
        connection.commit()
        print(f"Estado '{nombre_estado}' eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el estado: {e}")
    finally:
        cursor.close()
        connection.close()

# Buscar un estado por nombre
def buscar_estado_por_nombre(nombre_estado):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT * FROM ESTADO WHERE NOMBRE_ESTADO = :1"
        cursor.execute(sql, (nombre_estado,))
        estado = cursor.fetchone()
        if estado:
            print(f"Estado encontrado: {estado[0]}")
            return estado[0]
        else:
            print(f"No se encontró un estado con el nombre '{nombre_estado}'.")
            return None
    except Exception as e:
        print(f"Error al buscar el estado: {e}")
    finally:
        cursor.close()
        connection.close()

def obtener_estados():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT * FROM ESTADO"
        cursor.execute(sql)
        records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Error al mostrar estados: {e}")
    finally:
        cursor.close()
        connection.close()
