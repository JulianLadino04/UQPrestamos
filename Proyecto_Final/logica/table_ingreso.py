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

## ------------ INGRESO --------------- ##

def create_ingreso(usuario_id, entrada, salida):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Obtener el nuevo ID de ingreso como un NUMBER
    id = get_last_ingreso_id() + 1
    
    # Verificar si el ingreso ya existe
    cursor.execute("SELECT COUNT(*) FROM INGRESO_SISTEMA WHERE ID_USUARIO = :1 AND ENTRADA = :2", (usuario_id, entrada))
    if cursor.fetchone()[0] > 0:
        print("Ya existe un ingreso con el mismo ID de usuario y entrada.")
        cursor.close()
        connection.close()
        return

    sql = "INSERT INTO INGRESO_SISTEMA (ID_INGRESO, ID_USUARIO, ENTRADA, SALIDA) VALUES (:1, :2, :3, :4)"
    cursor.execute(sql, (id, usuario_id, entrada, salida))  # Usar `id` aquí
    connection.commit()
    print("Ingreso creado correctamente")
    cursor.close()
    connection.close()


def read_ingreso():
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM INGRESO_SISTEMA"
    cursor.execute(sql)
    INGRESOs = cursor.fetchall()
    cursor.close()
    connection.close()
    return INGRESOs

def delete_ingreso(INGRESO_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Verificar si el ingreso existe
    cursor.execute("SELECT COUNT(*) FROM INGRESO_SISTEMA WHERE ID_INGRESO = :1", (INGRESO_id,))
    if cursor.fetchone()[0] == 0:
        print(f"No se encontró ningún ingreso con ID {INGRESO_id}.")
        cursor.close()
        connection.close()
        return

    sql = "DELETE FROM INGRESO_SISTEMA WHERE ID_INGRESO = :1"
    cursor.execute(sql, (INGRESO_id,))
    connection.commit()
    print("Ingreso eliminado correctamente")
    cursor.close()
    connection.close()

def mostrar_ingresos():
    connection = get_connection()
    cursor = connection.cursor()
    SQL = '''
        SELECT *
        FROM INGRESO_SISTEMA
    '''
    cursor.execute(SQL)
    records = cursor.fetchall()
    for x in records:
        print(x)
        
def get_last_ingreso_id():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Consulta para obtener el último ID_INGRESO
        cursor.execute("""
            SELECT ID_INGRESO 
            FROM INGRESO_SISTEMA 
            ORDER BY ID_INGRESO DESC 
            FETCH FIRST 1 ROWS ONLY
        """)
        
        last_id = cursor.fetchone()
        
        if last_id is not None:
            return last_id[0]
        else:
            return 0
    
    except Exception as e:
        print(f"Ocurrió un error al obtener el último ID: {str(e)}")
    
    finally:
        cursor.close()
        connection.close()

def get_last_ingreso_id():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT ID_INGRESO 
            FROM INGRESO_SISTEMA 
            ORDER BY ID_INGRESO DESC 
            FETCH FIRST 1 ROWS ONLY
        """)
        
        last_id = cursor.fetchone()
        
        if last_id is not None and last_id[0] is not None:
            return int(last_id[0])  # Asegúrate de que sea un número entero
        else:
            return 0  # Si no hay registros, comienza en 0
    
    except Exception as e:
        print(f"Ocurrió un error al obtener el último ID: {str(e)}")
    
    finally:
        cursor.close()
        connection.close()
