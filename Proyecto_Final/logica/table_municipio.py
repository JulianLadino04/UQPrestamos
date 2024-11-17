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

# Crear un nuevo registro en la tabla con columna NOMBRE
def create_nombre(nombre):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Verificar si el nombre ya existe
        cursor.execute("SELECT COUNT(*) FROM MUNICIPIO WHERE NOMBRE = :1", (nombre,))
        if cursor.fetchone()[0] > 0:
            print(f"El nombre '{nombre}' ya existe.")
            return
        
        # Insertar nuevo nombre
        sql = "INSERT INTO MUNICIPIO NOMBRE VALUES (:1)"
        cursor.execute(sql, (nombre,))
        connection.commit()
        print("Nombre creado correctamente.")
    except Exception as e:
        print(f"Error al crear el nombre: {e}")
    finally:
        cursor.close()
        connection.close()

def obtener_nombres_municipios():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "SELECT NOMBRE FROM MUNICIPIO"  # Reemplaza "MUNICIPIOS" por el nombre real de tu tabla
        cursor.execute(sql)
        
        # Obtener todos los nombres en una lista
        nombres = [row[0] for row in cursor.fetchall()]
        return nombres
    
    except Exception as e:
        print(f"Error al obtener los nombres de municipios: {e}")
        return []
    
    finally:
        cursor.close()
        connection.close()

# Obtener un nombre por su valor
def obtener_nombre(nombre):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "SELECT * FROM MUNICIPIO WHERE NOMBRE = :1"
        cursor.execute(sql, (nombre,))
        
        registro = cursor.fetchone()
        if registro:
            print(f"Nombre encontrado: {registro[0]}")
            return registro
        else:
            print(f"No se encontró ningún registro con el nombre '{nombre}'.")
            return None
    except Exception as e:
        print(f"Error al obtener el nombre: {e}")
    finally:
        cursor.close()
        connection.close()

# Actualizar un nombre existente
def update_nombre(nombre_viejo, nombre_nuevo):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Verificar si el nombre existe
        cursor.execute("SELECT COUNT(*) FROM MUNICIPIO WHERE NOMBRE = :1", (nombre_viejo,))
        if cursor.fetchone()[0] == 0:
            print(f"No se encontró el nombre '{nombre_viejo}'.")
            return
        
        # Actualizar el nombre
        sql = "UPDATE MUNICIPIO SET NOMBRE = :1 WHERE NOMBRE = :2"
        cursor.execute(sql, (nombre_nuevo, nombre_viejo))
        connection.commit()
        print(f"Nombre actualizado de '{nombre_viejo}' a '{nombre_nuevo}'.")
    except Exception as e:
        print(f"Error al actualizar el nombre: {e}")
    finally:
        cursor.close()
        connection.close()

# Eliminar un nombre por su valor
def delete_nombre(nombre):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "DELETE FROM MUNICIPIO WHERE NOMBRE = :1"
        cursor.execute(sql, (nombre,))
        connection.commit()
        if cursor.rowcount > 0:
            print(f"Nombre '{nombre}' eliminado correctamente.")
        else:
            print(f"No se encontró el registro con el nombre '{nombre}'.")
    except Exception as e:
        print(f"Error al eliminar el nombre: {e}")
    finally:
        cursor.close()
        connection.close()

# Mostrar todos los registros
def mostrar_nombres():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        sql = "SELECT * FROM MUNICIPIO"
        cursor.execute(sql)
        nombres = cursor.fetchall()
        for nombre in nombres:
            print(nombre[0])
    except Exception as e:
        print(f"Error al mostrar los nombres: {e}")
    finally:
        cursor.close()
        connection.close()
