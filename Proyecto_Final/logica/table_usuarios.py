import random
import oracledb

niveles = ["Principal","Tesoreria","Empleado"]

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



## ------------ USUARIOS --------------- ##
def create_usuario(identificacion, nombre, username, password, nivel):
    connection = get_connection()  # Asume que tienes este método implementado
    cursor = connection.cursor()
    
    try:
        # Verificar si el ID_USUARIO ya existe
        cursor.execute("SELECT COUNT(*) FROM USUARIO WHERE ID_USUARIO = :1", (identificacion,))
        if cursor.fetchone()[0] > 0:
            print("El ID de usuario ya existe. Elija otro.")
            return

        # Verificar si el USERNAME ya existe
        cursor.execute("SELECT COUNT(*) FROM USUARIO WHERE USERNAME = :1", (username,))
        if cursor.fetchone()[0] > 0:
            print("El nombre de usuario ya existe. Elija otro.")
            return
        
        # Insertar el nuevo usuario en la tabla USUARIO
        sql_usuario = "INSERT INTO USUARIO (ID_USUARIO, USERNAME, PASSWORD, NIVEL, NOMBRE) VALUES (:1, :2, :3, :4, :5)"
        cursor.execute(sql_usuario, (identificacion, username, password, nivel, nombre))

        # Insertar las credenciales en la tabla CREDENCIALES
        sql_credenciales = "INSERT INTO CREDENCIALES (USERNAME, PASSWORD, USUARIO) VALUES (:1, :2, :3)"
        cursor.execute(sql_credenciales, (username, password, identificacion))

        # Confirmar ambas inserciones
        connection.commit()
        print("Usuario y credenciales creados correctamente")
            
    except Exception as e:
        print(f"Error al crear el usuario y sus credenciales: {e}")
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
        
def obtener_usuario_identificacion_y_user(identificacion: str, user: str):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Consulta para buscar el usuario por su IDENTIFICACIÓN y USERNAME
        sql = """
        SELECT USERNAME, PASSWORD, USUARIO
        FROM CREDENCIALES 
        WHERE IDENTIFICACION = :1 AND USERNAME = :2
        """
        cursor.execute(sql, (identificacion, user))  # Asegúrate de que esto sea una tupla

        # Obtener la fila completa de resultados
        fila = cursor.fetchone()

        if fila is None:
            print(f"No se encontró ningún usuario con la IDENTIFICACIÓN {identificacion} y el USERNAME {user}.")
            return None

        # Desempaquetar los resultados
        usuario, password, id_usuario = fila

        # Verificar las credenciales
        if usuario == user:
            print(f"Se encontró el usuario con la IDENTIFICACIÓN {identificacion} y el USERNAME {user}.")
            return id_usuario
        else:
            print(f"Credenciales incorrectas.")
            return None

    except Exception as e:
        print(f"Ocurrió un error al buscar el usuario: {str(e)}")

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
        cursor.execute(sql, (user,))

        # Obtener la fila completa de resultados
        fila = cursor.fetchone()

        if fila is None:
            print(f"No se encontró ningún usuario con el USERNAME {user}.")
            return None

        # Desempaquetar los resultados
        username_db, password_db, id_usuario = fila

        # Verificar las credenciales (puedes agregar un hash aquí si es necesario)
        if username_db == user and contrasena == password_db:
            print(f"Se encontró el usuario con el USERNAME {user}.")
            return id_usuario
        else:
            print(f"Credenciales incorrectas.")
            return None

    except Exception as e:
        print(f"Ocurrió un error al buscar el usuario: {str(e)}")
        return None  # Retorna None en caso de error

    finally:
        cursor.close()
        connection.close()


    
# Función para actualizar un usuario en la base de datos
def update_usuario(user_id, nuevo_username=None, nuevo_password=None, nuevo_nivel=None, nuevo_nombre=None):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Construimos dinámicamente la consulta SQL
        sql = "UPDATE USUARIO SET "
        updates = []
        params = []

        # Actualizar username si se proporciona
        if nuevo_username:
            updates.append("USERNAME = :1")
            params.append(nuevo_username)

        # Actualizar password si se proporciona
        if nuevo_password:
            updates.append("PASSWORD = :2")
            params.append(nuevo_password)

        # Validar y actualizar el nivel si se proporciona
        if nuevo_nivel:
            niveles_validos = ["Tesoreria", "Empleado", "Principal"]
            if nuevo_nivel not in niveles_validos:
                print("Nivel no válido. Debe ser uno de los siguientes:", niveles_validos)
                return
            updates.append("NIVEL = :3")
            params.append(nuevo_nivel)

        # Actualizar nombre si se proporciona
        if nuevo_nombre:
            updates.append("NOMBRE = :4")
            params.append(nuevo_nombre)

        # Asegurarse de que se ha especificado al menos un campo para actualizar
        if not updates:
            print("No se especificó ningún campo para actualizar.")
            return
        
        # Agregar la condición WHERE a la consulta
        sql += ", ".join(updates) + " WHERE ID_USUARIO = :5"
        params.append(user_id)

        # Ejecutar la consulta con los parámetros
        cursor.execute(sql, params)
        
        # Actualizar las credenciales en la tabla CREDENCIALES
        # Solo si se cambia el username o password
        if nuevo_username or nuevo_password:
            # Verificamos si ya existen credenciales para el usuario
            cursor.execute("SELECT COUNT(*) FROM CREDENCIALES WHERE USUARIO = :1", (user_id,))
            if cursor.fetchone()[0] > 0:
                # Actualizar las credenciales existentes
                sql_credenciales_update = """
                UPDATE CREDENCIALES 
                SET USERNAME = :1, PASSWORD = :2 
                WHERE USUARIO = :3
                """
                cursor.execute(sql_credenciales_update, (nuevo_username if nuevo_username else None,
                                                          nuevo_password if nuevo_password else None,
                                                          user_id))
            else:
                # Insertar nuevas credenciales si no existen
                sql_credenciales_insert = """
                INSERT INTO CREDENCIALES (USERNAME, PASSWORD, USUARIO)
                VALUES (:1, :2, :3)
                """
                cursor.execute(sql_credenciales_insert, (nuevo_username, nuevo_password, user_id))

        # Confirmar los cambios
        connection.commit()
        print(f"Usuario con ID '{user_id}' actualizado correctamente.")
    
    except Exception as e:
        print(f"Error al actualizar el usuario y sus credenciales: {str(e)}")
    
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
        