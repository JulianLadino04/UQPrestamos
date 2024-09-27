import random
import oracledb

niveles = ["Principal","Tesoreria","Empleado"]

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



## ------------ USUARIOS --------------- ##
def create_usuario(identificacion, nombre, username, password, nivel):
    connection = get_connection()  # Asumo que ya tienes este método implementado
    cursor = connection.cursor()
    
    try:
        # Verificar si el ID_USUARIO ya existe
        cursor.execute("SELECT COUNT(*) FROM USUARIO WHERE ID_USUARIO = :1", (identificacion,))
        if cursor.fetchone()[0] > 0:
            print("El ID de usuario ya existe. Elija otro.")
            return

        # Verificar si el username ya existe
        cursor.execute("SELECT COUNT(*) FROM USUARIO WHERE USERNAME = :1", (username,))
        if cursor.fetchone()[0] > 0:
            print("El nombre de usuario ya existe. Elija otro.")
            return
        
        sql = "INSERT INTO USUARIO (ID_USUARIO, USERNAME, PASSWORD, NIVEL, NOMBRE) VALUES (:1, :2, :3, :4, :5)"
        cursor.execute(sql, (identificacion, username, password, nivel, nombre))  # Ahora la tupla es correcta
        connection.commit()
        print("Usuario creado correctamente")
            
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
    finally:
        cursor.close()
        connection.close()


def obtener_usuario(id: int):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Consulta para buscar el usuario por su ID
        sql = """
        SELECT * 
        FROM USUARIO 
        WHERE ID_USUARIO = :1
        """
        cursor.execute(sql, (id,))  # Asegúrate de que esto sea una tupla

        usuario = cursor.fetchone()

        if usuario:
            # Asumimos que los campos son (ID_usuario, NOMBRE, PASSWORD, NIVEL)
            print(f"Usuario encontrado: ID={usuario[0]}, Nombre={usuario[1]}, Nivel={usuario[3]}")
            return usuario
        else:
            print(f"No se encontró ningún usuario con el ID {id}.")
            return None

    except Exception as e:
        print(f"Ocurrió un error al buscar el usuario: {str(e)}")

    finally:
        cursor.close()
        connection.close()

def obtener_tipo_user(user: str):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Consulta para buscar el usuario por su ID
        sql = """
        SELECT NIVEL 
        FROM USUARIO 
        WHERE USERNAME = :1
        """
        cursor.execute(sql, (user,))  # Asegúrate de que esto sea una tupla

        usuario = cursor.fetchone()

        if usuario is None:
            print(f"No se encontró ningún usuario con el USERNAME {user}.")
            return None
        else:
            # Devuelve los valores específicos (USERNAME y PASSWORD)
            usuario_data = {
                "tipo": usuario[0],  # Primer valor es tipo de usuario
            }
            print("Usuario encontrado: Tipo de Usuario={usuario_data['tipo']")
            return usuario_data

    except Exception as e:
        print(f"Ocurrió un error al buscar el usuario: {str(e)}")

    finally:
        cursor.close()
        connection.close()
        
def obtener_tipo_user_ID(id_user: str) -> str:
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Consulta para buscar el usuario por su ID
        sql = """
        SELECT NIVEL 
        FROM USUARIO 
        WHERE ID_USUARIO = :1
        """
        cursor.execute(sql, (id_user,))  # Asegúrate de que esto sea una tupla

        usuario = cursor.fetchone()

        if usuario is None:
            print(f"No se encontró ningún usuario con la id {id_user}.")
            return None
        else:
            # Extraer el valor de la consulta y retornarlo como string
            tipo_usuario = usuario[0]  # Primer valor es tipo de usuario
            print(f"Usuario encontrado: Tipo de Usuario={tipo_usuario}")
            return str(tipo_usuario)

    except Exception as e:
        print(f"Ocurrió un error al buscar el usuario: {str(e)}")
        return None

    finally:
        cursor.close()
        connection.close()
        
        
def obtener_usuario_user(user: str, contrasena: str):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Consulta para buscar el usuario por su USERNAME
        sql = """
        SELECT USERNAME, PASSWORD, USUARIO
        FROM CREDENCIALES 
        WHERE USERNAME = :1
        """
        cursor.execute(sql, (user,))  # Asegúrate de que esto sea una tupla

        # Obtener la fila completa de resultados
        fila = cursor.fetchone()

        if fila is None:
            print(f"No se encontró ningún usuario con el USERNAME {user}.")
            return None

        # Desempaquetar los resultados
        usuario, password, id_usuario = fila

        # Verificar las credenciales
        if usuario == user and contrasena == password:
            print(f"Se encontró el usuario con el USERNAME {user}.")
            return id_usuario
        else:
            print(f"Credenciales incorrectas.")
            return None

    except Exception as e:
        print(f"Ocurrió un error al buscar el usuario: {str(e)}")

    finally:
        cursor.close()
        connection.close()
    
def update_usuario(user_id, username, password, nivel : str):
    if nivel not in niveles:
        print("Nivel no valido")
        return  # Salimos de la función si el nivel no es válido

    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "UPDATE USUARIO SET USERNAME = :1, PASSWORD = :2, NIVEL = :3 WHERE ID_USUARIO = :4"
        cursor.execute(sql, (username, password, nivel, user_id))
        connection.commit()
        print("Usuario actualizado correctamente")
    except Exception as e:
        print(f"Error al actualizar el usuario: {str(e)}")
    finally:
        cursor.close()
        connection.close()

def delete_usuario(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM USUARIO WHERE ID_USUARIO = :1"
        cursor.execute(sql, (user_id,))
        connection.commit()
        if cursor.rowcount > 0:
            print("Usuario eliminado correctamente")
        else:
            print(f"No se encontró usuario con ID {user_id}")
    except Exception as e:
        print(f"Error al eliminar el usuario: {str(e)}")
    finally:
        cursor.close()
        connection.close()

        
def mostrarUsuarios():
    connection = get_connection()
    cursor = connection.cursor()
    SQL = '''
        select *
        from system.USUARIO
    '''
    cursor.execute(SQL)
    records = cursor.fetchall()
    for x in records:
        print(x)

def get_last_usuario_id():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Consulta para obtener el último ID_usuario
        cursor.execute("""
            SELECT ID_USUARIO 
            FROM USUARIO
            ORDER BY ID_USUARIO DESC 
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
        