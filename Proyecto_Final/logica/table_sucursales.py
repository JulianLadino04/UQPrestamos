import random
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


## ----------- SUCURSALES ----------- ##

def create_sucursal(nombre, municipio):
    connection = get_connection()
    cursor = connection.cursor()
    
    id = get_last_sucursal_id() + 1    
    sql = """
    INSERT INTO SUCURSAL (ID_SUCURSAL, NOMBRE, MUNICIPIO)
    VALUES (:1, :2, :3)
    """  
    cursor.execute(sql, (id, nombre, municipio))
    connection.commit()
    print("Sucursal creada correctamente")
    cursor.close()
    connection.close()

def obtener_sucursal(id : int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Consulta para buscar la sucursal por su ID
        sql = """
        SELECT * 
        FROM SUCURSAL 
        WHERE ID_SUCURSAL = :1
        """
        cursor.execute(sql, (id,))
        
        sucursal = cursor.fetchone()
        
        if sucursal:
            # Asumimos que los campos son (ID_SUCURSAL, NOMBRE, MUNICIPIO)
            print(f"Sucursal encontrada: ID={sucursal[0]}, Nombre={sucursal[1]}, Municipio={sucursal[2]}")
            return sucursal
        else:
            print(f"No se encontró ninguna sucursal con el ID {id}.")
            return None
    
    except Exception as e:
        print(f"Ocurrió un error al buscar la sucursal: {str(e)}")
    
    finally:
        cursor.close()
        connection.close()

def update_sucursal(sucursal_id, nombre, direccion):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "UPDATE SUCURSAL SET NOMBRE = :1, MUNICIPIO = :2 WHERE ID_SUCURSAL = :3"
    cursor.execute(sql, (nombre, direccion, sucursal_id))
    connection.commit()
    cursor.close()
    connection.close()

def delete_sucursal(sucursal_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM SUCURSAL WHERE ID_SUCURSAL = :1"
    cursor.execute(sql, (sucursal_id,))
    connection.commit()
    cursor.close()
    connection.close()
   
def mostrarSucursales():
    connection = get_connection()
    cursor = connection.cursor()
    SQL = '''
        select *
        from system.SUCURSAL
    '''
    cursor.execute(SQL)
    records = cursor.fetchall()
    for x in records:
        print(x)

def get_last_sucursal_id():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Consulta para obtener el último ID_SUCURSAL
        cursor.execute("""
            SELECT ID_SUCURSAL 
            FROM SUCURSAL 
            ORDER BY ID_SUCURSAL DESC 
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