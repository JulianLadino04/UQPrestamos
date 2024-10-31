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

# ----------- CARGO ----------- #

# Método para crear un nuevo cargo
def crear_cargo(nombre, monto_maximo):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Verificar si el nombre del cargo ya existe
        cursor.execute("SELECT COUNT(*) FROM CARGO WHERE NOMBRE = :1", (nombre,))
        if cursor.fetchone()[0] > 0:
            print("El cargo ya existe. Elija otro nombre.")
            return

        sql = '''INSERT INTO CARGO (NOMBRE, MONTO_MAXIMO) 
                 VALUES (:1, :2)'''
        cursor.execute(sql, (nombre, monto_maximo))
        connection.commit()
        print(f"Cargo '{nombre}' creado correctamente con un monto máximo de '{monto_maximo}'.")
    except Exception as e:
        print(f"Error al crear el cargo: {e}")
    finally:
        cursor.close()
        connection.close()

# Método para leer todos los cargos
def leer_cargos():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT NOMBRE, MONTO_MAXIMO FROM CARGO")
        cargos = cursor.fetchall()
        for cargo in cargos:
            print(f"Cargo: {cargo[0]}, Monto Máximo: {cargo[1]}")
    except Exception as e:
        print(f"Error al leer los cargos: {e}")
    finally:
        cursor.close()
        connection.close()

# Método para buscar un cargo por su nombre
def buscar_cargo_por_nombre(nombre):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT NOMBRE, MONTO_MAXIMO FROM CARGO WHERE NOMBRE = :1"
        cursor.execute(sql, (nombre,))
        cargo = cursor.fetchone()
        if cargo:
            print(f"Cargo: {cargo[0]}, Monto Máximo: {cargo[1]}")
        else:
            print(f"No se encontró el cargo con nombre '{nombre}'.")
    except Exception as e:
        print(f"Error al buscar el cargo: {e}")
    finally:
        cursor.close()
        connection.close()

# Método para retornar todos los cargos y su monto máximo
def retornar_cargos_y_monto_maximo():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT NOMBRE, MONTO_MAXIMO FROM CARGO"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return [(cargo[0], cargo[1]) for cargo in resultados]
    except Exception as e:
        print(f"Error al retornar los cargos y montos máximos: {e}")
    finally:
        cursor.close()
        connection.close()

def retornar_nombres_cargos():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "SELECT NOMBRE FROM CARGO"
        cursor.execute(sql)
        nombres_cargos = cursor.fetchall()
        return [cargo[0] for cargo in nombres_cargos]
    except Exception as e:
        print(f"Error al retornar los nombres de los cargos: {e}")
    finally:
        cursor.close()
        connection.close()
