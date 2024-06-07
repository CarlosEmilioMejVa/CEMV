import mariadb
from icecream import ic

'''
Este archivo es para tener acomodados los queries de la BD.

Para poder modificar la conexión con la BD vas a tener que modificar
la función `connect_to_database()` con las credenciales que sean
necesarias.

Recomiendo tener los queries separados para que incluso, si quiere
tener otros archivos relacionados a la base de datos del CEMV pueda
llamar las funciones.

Seguí una nomenclatura simple en pseudo-inglés para poder entender de
forma facil el qué hace cada función.

Principalmente para generalizar todo, el objeto de conexión de la BD
es `mydb`, corto de "my database", es mas facil llamar ese objeto en
cualquier otra funcion
'''

# Funciona
def connect_to_database(
		host="192.168.13.133",
		user="csistemas",
		password="U3cat3p3c",
		database="cemv"
):
	"""
	Devuelve la conexión base con la base de datos.
	Nota que en los parametros de la conexión ya tiene valores 
	preestablecidos, esto es para que pueda "Sobreescribir" las
	credenciales sin ningun problema o preocupación de que se pierdan.
	"""
	try:
		'''
		Los prints comentados son para tener debug, si los quiere
		activar para poder verlos solo descomente los print y en el 
		comando de creación del CEMV cambie para que sea Windowed
		(checa documentación de pyinstaller)
		'''
		# print(f">> Conectando a `{host}`...")
		mydb = mariadb.connect(
			host=host,
			user=user,
			password=password,
			database=database
		)
		# print(f">> Se estableció conexión con `{host}` a `{database}`")
		return mydb

	except mariadb.Error as err:
		# print(f">> No se pudo conectar con `{host}`:\t`{err}`")
		return None


def check_credentials(mydb, data):
	"""
	Se checa que el usuario que se ingresa en la variable "data"
	exista, si si existe, va a devolver toda la información, si no, va
	a devolver 0
	"""
	try:
		cursor = mydb.cursor()
		query = 'SELECT IF(EXISTS (SELECT 1 FROM cemv.usuarios WHERE ID_USUARIO = %s AND PASS = %s), 1, 0);'
		cursor.execute(query, data)
		results = cursor.fetchone()[0]
		return results

	except mariadb.ProgrammingError as err:
		print(f"Error en check_credentials: {err}")
		return 0

	finally:
		cursor.close()


def get_full_data(mydb, id_usuario):
	"""
	Se obtiene el ID_USUARIO, USUARIO_NAME, ID_ROL de la tabla
	usuarios donde el ID_USUARIO sea el quel el usuario ingresó.
	"""
	cursor = mydb.cursor()
	query = "SELECT ID_USUARIO, USUARIO_NAME, ID_ROL FROM usuarios WHERE ID_USUARIO = %s;"
	cursor.execute(query, (id_usuario,))
	results = cursor.fetchone()
	cursor.close()
	return results


def get_retries(mydb):
	"""
	Obtiene los valores de la configuración de reintentos desde la
	base de datos guardados en la tabla `config`.
	"""
	cursor = mydb.cursor()
	query = "SELECT CONFIG_VALUE_INT FROM config WHERE ID_CONFIG = 1;"
	cursor.execute(query)
	results = cursor.fetchone()[0]
	cursor.close()
	return results


def get_evento(mydb):
	"""
	Obtiene EVENTO_NAME de la tabla cat_evento
	"""
	cursor = mydb.cursor()
	query = "SELECT EVENTO_NAME FROM cat_evento;"
	cursor.execute(query)
	results = cursor.fetchall()
	for i, result in enumerate(results):
		results[i] = result[0]
	cursor.close()
	return results


def get_plantel(mydb):
	"""
	Obtiene PLANTEL_NAME de cat_plantel
	"""
	cursor = mydb.cursor()
	query = "SELECT PLANTEL_NAME FROM cat_plantel;"
	cursor.execute(query)
	results = cursor.fetchall()
	for i, result in enumerate(results):
		results[i] = result[0]
	cursor.close()
	return results


def get_estatus(mydb):
	"""
	Obtiene ESTATUS_NAME de cat_estatus
	"""
	cursor = mydb.cursor()
	query = "SELECT ESTATUS_NAME FROM cat_estatus"
	cursor.execute(query)
	results = cursor.fetchall()
	for i, result in enumerate(results):
		results[i] = result[0]
	cursor.close()
	return results


def get_machines(mydb, PLANTEL_NAME):
	"""
	Obtiene el UBI_NAME de cat_ubi dependiendo del PLANTEL_NAME
	"""
	cursor = mydb.cursor()
	query = "SELECT UBI_NAME FROM cat_ubi AS CU INNER JOIN cat_plantel AS CP ON CU.ID_PLANTEL = CP.ID_PLANTEL WHERE CP.PLANTEL_NAME = %s ORDER BY UBI_NAME ASC;"
	cursor.execute(query, (PLANTEL_NAME,))
	results = cursor.fetchall()
	for i, result in enumerate(results):
		results[i] = result[0]
	cursor.close()
	return results


def get_evento_from_name(mydb, evento_name):
	'''
    Esta función realiza una consulta a la base de datos para obtener
    el ID de un evento dado su nombre.
    '''
	cursor = mydb.cursor()
	query = "SELECT ID_EVENTO FROM cat_evento WHERE EVENTO_NAME = %s;"
	cursor.execute(query, evento_name)
	results = cursor.fetchone()
	cursor.close()
	return results[0]


def get_plantel_from_name(mydb, plantel_name):
	'''
	Esta función obtiene el ID_PLANTEL de cat_plantel por el nombre
	del plantel
	'''
	cursor = mydb.cursor()
	query = "SELECT ID_PLANTEL FROM cat_plantel WHERE PLANTEL_NAME = %s;"
	cursor.execute(query, plantel_name)
	results = cursor.fetchone()
	cursor.close()
	return results[0]


def get_ubi_from_name(mydb, data):
	'''
	Se obtiene el ID_UBI, UBI_NAME y ID_PLANTEL dependeindo de su
	UBI_NAME y PLANTEL_NAME
	'''
	cursor = mydb.cursor()
	query = "SELECT CU.ID_UBI, CU.UBI_NAME, CP.ID_PLANTEL FROM cat_ubi AS CU INNER JOIN cat_plantel AS CP ON CU.ID_PLANTEL = CP.ID_PLANTEL WHERE CU.UBI_NAME = %s AND CP.PLANTEL_NAME = %s;"
	cursor.execute(query, data)
	results = cursor.fetchone()
	cursor.close()
	return results[0]


def get_estatus_from_name(mydb, estatus_name):
	'''
	Se obtiene el ID_ESTATUS dependiendo de su ESTATUS_NAME
	'''
	cursor = mydb.cursor()
	query = "SELECT ID_ESTATUS FROM cat_estatus WHERE ESTATUS_NAME = %s;"
	cursor.execute(query, estatus_name)
	results = cursor.fetchone()
	cursor.close()
	return results[0]

def select_last_id(mydb):
	with mydb.cursor() as cursor:
		query = 'SELECT LAST_INSERT_ID();'
		cursor.execute(query)
		results = cursor.fetchone()[0]
	return results

def add_records(mydb, data):
	"""
	Añade registros a la tabla 'records_raw'.
	"""
	try:
		cursor = mydb.cursor()
		query = "INSERT INTO `cemv`.`records_raw` VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(query, data)
		mydb.commit()

		return [True, select_last_id(mydb)]

	except mariadb.Error as err:
		print(f"Error en add_records: {err}")
		return [False, None]

	finally:
		cursor.close()

# CONSULTAS PARA LA TABLA DE FILTROS
'''
Honestamente sufrí mucho con esta parte del código
'''

def obtener_columnas(mydb):
	"""
	se obtienen los headers de las columnas para la tabla de filtros
	se obtienen 3 valores:
		custom_names: es el como se ven las columnas en la consulta
			ej: R.FOLIO AS 'Folio' se obtiene "Folio"
		real_names: es el nombre real de la columna
			ej: R.FOLIO AS 'Folio' se obtiene "FOLIO"
		table: es el nombre de la tabla de donde está el JOIN
			ej: R.FOLIO AS 'Folio' se obtiene "R"
	"""
	try:
		cursor = mydb.cursor()
		cursor.execute("""
			SELECT
			    R.FOLIO AS 'Folio',
			    CE.EVENTO_NAME AS 'Solicitud',
			    R.Q_NAME AS 'Solicitante',
			    CP.PLANTEL_NAME AS "Plantel",
			    CU.UBI_NAME AS "Ubicación",
			    R.DATE AS 'Fecha',
			    CES.ESTATUS_NAME AS 'Estatus'
			FROM
    			`records_raw` AS R
			INNER JOIN `cat_evento` AS CE
			ON
			    R.ID_EVENTO = CE.ID_EVENTO
			INNER JOIN `cat_estatus` AS CES
			ON
			    R.ID_ESTATUS = CES.ID_ESTATUS
			INNER JOIN `cat_plantel` AS CP
			ON
			    R.ID_PLANTEL = CP.ID_PLANTEL
			LEFT JOIN `cat_ubi` AS CU
			ON
			    R.ID_UBI = CU.ID_UBI
			WHERE
			    TRUE;
		""")
		# Obtener la información sobre las columnas
		columns_info = cursor.description
		# Obtener los nombres de las columnas
		custom_names = [column_info[0] for column_info in columns_info]
		real_name = [column_info[-2] for column_info in columns_info]
		table = [column_info[-1] for column_info in columns_info]

		return [custom_names, real_name, table]

	except mariadb.Error as err:
		print(f"Error de Mariadb: {err}")

	finally:
		cursor.close()

def ejecutar_consulta(mydb, consulta):
	"""
	funcion simple, solo ejecuta la consulta que se le ingresa
	"""
	cursor = mydb.cursor()
	cursor.execute(consulta)
	results = cursor.fetchall()
	cursor.close()
	return results


def seleccionar_valores_de_combos(mydb, columna, tabla):
	'''
	se obtienen los valores de una columna de una tabla para ocuparse
	en un combo
	'''
	with mydb.cursor() as cursor:
		query = f"SELECT {columna} FROM {tabla}"
		cursor.execute(query)
		
		results = [valor[0] for valor in cursor.fetchall()]
		
	return results

def seleccionar_ubi_plantel(mydb, plantel_name):
	'''
	Selecciona el UBI_NAME dependiendo del PLANTEL_NAME
	'''
	with mydb.cursor() as cursor:
		query = f"SELECT CU.UBI_NAME FROM cat_ubi AS CU INNER JOIN cat_plantel as CP ON CP.ID_PLANTEL = CU.ID_PLANTEL WHERE CP.PLANTEL_NAME = \"{plantel_name}\" ORDER BY UBI_NAME ASC;"
		cursor.execute(query)
		results = [valor[0] for valor in cursor.fetchall()]	
	return results

def seleccionar_ID_UBI_X_UBI_NAME(mydb, ubi_name):
	'''
	selecciona el ID_UBI dependiendo del UBI_NAME
	'''
	with mydb.cursor() as cursor:
		query = f"SELECT CU.ID_UBI FROM cat_ubi AS CU WHERE CU.UBI_NAME = \"{ubi_name}\";"
		cursor.execute(query)
		results = cursor.fetchone()
	return results[0]



def seleccionar_plantel(mydb):
	'''
	Selecciona todos los PLANTEL_NAME
	'''
	with mydb.cursor() as cursor:
		query = "SELECT CP.PLANTEL_NAME FROM cat_plantel AS CP WHERE 1; "
		
		cursor.execute(query)
		results = [valor[0] for valor in cursor.fetchall()]
		
	return results


# Imagen ventana "About"
def select_image_from_database(mydb):
	'''
	obtiene la información en binario de la imagen del logo del CEMV
	para la ventana "About"

	Esta es la base para poder almacenar imagenes en la base de datos
	se tendrian que almacenar en forma de Binario (no 0 y 1)
	'''
	try:
		# Crear un objeto cursor
		cursor = mydb.cursor()

		# Ejemplo de selección: seleccionar el campo LONGBLOB de tu tabla
		select_query = "SELECT CONFIG_VALUE_LBLOB FROM config WHERE ID_CONFIG = %s"
		record_id = 1  # Cambiar según tu necesidad
		cursor.execute(select_query, (2,))

		# Obtener los datos binarios
		image_binary_data = cursor.fetchone()

		return image_binary_data[0]

	except mariadb.Error as error:
		print(f"Error al seleccionar la imagen: {error}")

	finally:
		# Cerrar la conexión
		cursor.close()
