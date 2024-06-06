import PySimpleGUI as sg
import os
import json
import datetime

from connect_mariadb_v0_1_1B4 import *
from layouts_v0_1_1B4 import *
from functions_v0_1_1B4 import *

'''
Este es el CSS del CEMV, aqui están todas las ventanas de la GUI, si
quieren agregar una nueva venatna, aquí la agregan para que esté todo
acomodado.

Generalmente lo que tenga relación a la BD, vas a tener que meter la
conexión como parametro
'''


sg.theme('DarkGreen1')




def retry_connect():
	'''
	Esta ventana es para reintentar la conexión a la BD
	'''
	layout = [retry_connect_layout()]

	window = sg.Window("Reintentar conexión • CEMV", layout)

	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, "-EXIT-"):
			window.close()
			return -1
		elif event == "-CONN-":
			credentials = (values["-HOST-"], values["-USER-"], values["-PASS-"], values["-DB-"])
			mydb = connect_to_database(*credentials)
			if mydb:
				window.close()
				return mydb
			else:
				sg.PopupError("No se ha podido conectar a la base de datos, reintentalo")
				window["-HOST-"].update("")
				window["-USER-"].update("")
				window["-PASS-"].update("")
				window["-DB-"].update("")



# window
def login_menu(mydb):
	"""
	Esta es la primer parte que se ejecuta en el CEMV, es la ventana
	del LOGIN, aqui se busca que el usuario exista con la funcion ``,
	y si existe, devuelve sus datos con la funcion
	`get_full_data(db_connection, id_usuario)`
	"""
	layout = login_window()
	window = sg.Window("Log In • CEMV", layout)

	cont = 0


	# Obtener los datos de configuración desde la base de datos
	retries = get_retries(mydb) # int


	while True:
		if cont >= retries - 1:
			sg.PopupError("Error", "Demasiados intentos, cerrando el programa")
			window.close()
			return (False,None)

		event, values = window.read()

		if event in (sg.WIN_CLOSED, "-CANCEL-", "Exit"):
			window.close()
			return (False, None)

		if event == "-CONTINUE-":
			try:
				id_user = int(values["-ID_USER-"])
				pass_user = values["-PASS_USER-"]
				cred = (id_user, pass_user)
			except Exception as Error:
				sg.PopupError("Error", "Usuario y/o contraseña incorrectos, Intentalo de nuevo")
				cont += 1
				continue
			# Checa que las credenciales que ingresó el usuario existan, si existen, devuelve los datos del usuario
			results = check_credentials(mydb, cred)

			if results:
				# Obtiene los datos del usuario que se encontró
				data = get_full_data(mydb, cred[0])
				
				window.close()
				return (True, data)
			else:
				sg.PopupError("Error", "Usuario y/o contraseña incorrectos, Intentalo de nuevo")
				cont += 1
		if event == "About":
			window.close()
			about_window(mydb)


def menu_window(mydb, rol):
	'''
	Este es el menú principal, es dinamico con el rol, solo tienen que
	crear un layout especial del nuevo rol que quieran agregar y queda
	dinamico
	'''

	layout = []

	if rol == 0:
		layout = [[sg.P(), sg.Frame("Menu", admin_menu() ), sg.P()]]
	elif rol == 1:
		layout = [[sg.P(), sg.Frame("Menu", user_menu() )], sg.P()]
	elif rol == 2:
		layout = [[sg.P(), sg.Frame("Menu", viewer_menu() , sg.P())]]

	layout.append([sg.P(), sg.B("Salir", k = "-EXIT-", button_color = ("#ffffff", "#ff0000"))])

	window = sg.Window("Main menu • CEMV", layout, size = (300, 230))

	while True:
		event, values = window.read()

		if event in (sg.WIN_CLOSED, "-EXIT-"):
			window.close()
			return None

		elif event == "-ADD_RECORD-":
			window.close()
			return 1
		elif event == "-SEE_RECORDS-":
			window.close()
			return 2
		elif event == "-MAN_RECORDS-":
			window.close()
			return 3
		elif event == "-MAN_USERS-":
			window.close()
			return 4
		elif event == "-CONFIG-":
			window.close()
			return 5
		elif event == "About":
			window.close()
			return 6
		else:
			window.close()
			return None


def add_records_window(mydb, data):
	'''
	Esta es la ventana principal de agregar un nuevo registro al CEMV
	'''
	layout = add_records_window_layout(mydb)

	window = sg.Window("Agregar registro • CEMV", layout)


	while True:
		event, values = window.read()
		if event in (sg.WIN_CLOSED, "Exit", "-GO_BACK-"):
			window.close()
			break
		
		if event == "-UBICATION-":
			window["-MACHINE-"].update(values = get_machines(mydb, values["-UBICATION-"]))

		if event == "-CLEAR-":
			clear(window)

		if event == "-DEV-":
			pass

		if event == "-SAVE-":
			if es_hora_valida(values["-HOUR-"], values["-MINUTES-"]):
				if save_records_popup():
					try:
						record_data = []
						# Tipo de evento
						record_data.append(get_evento_from_name(mydb, (values["-CALL_TYPE-"],)))
						# Plantel
						record_data.append(get_plantel_from_name(mydb, (values["-UBICATION-"],)))
						# Salón o maquina
						record_data.append(get_ubi_from_name( mydb, (values["-MACHINE-"], values["-UBICATION-"]) ))
						# Quejoso
						record_data.append(values["-NAME_USER_MACHINE-"])
						# Quejoso_desc
						record_data.append(values["-PROB_USER-"])
						# Quejoros_date
						record_data.append(values["-DATE-"])
						# Quejoso_time
						# record_data.append(f"{values["-HOUR-"]}:{values["-MINUTES-"]}")
						record_data.append(f"{values["-HOUR-"]}:{values["-MINUTES-"]}")
						# ID_USUARIO
						record_data.append(data[0])
						# TI_SOL
						record_data.append(values["-PROB_TI-"])
						# TI_COM
						record_data.append(values["-COMMENTS-"])
						# ESTATUS
						record_data.append(get_estatus_from_name(mydb, (values["-STATUS_TYPE-"],)))

						record_data = tuple(record_data)

						data_as_strings = [str(x) if isinstance(x, int) else x for x in record_data]

						result, last_id = add_records(mydb, data_as_strings)

						if result:
							sg.popup(f"Se guardaron los datos!\nFolio:\t{last_id}")
							clear(window)
						else:
							sg.popup("Hubo un error...")
							clear(window)
					except Exception as Error:
						popup_Error()
			else:
				sg.PopupError("Ingresa una hora Valida en formato 24H")

	


def about_window(mydb):
	'''
	Esta es la ventana de About
	'''
	layout = about_layout(mydb)
	window = sg.Window("CEMV • About", layout)
	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED:
			window.close()
			return None


def save_records_popup():
	'''
	Este es el Pop-Up de confirmación para guardar los datos del
	registro
	'''
	layout = save_records_popup_layout()
	window = sg.Window("CEMV • ALERT", layout)
	while True:
		event, _ = window.read()
		if event in ("Cancel", sg.WIN_CLOSED):
			result = False
			break
		if event == "Yes":
			result = True
			break
	window.close()
	return result


def popup_Error():
	'''
	Si llega a haber un error en el registro de datos, esta ventana va
	a aparer con el error
	'''
	layout = popup_Error_layout()
	with sg.Window("Error", layout) as window:
		while True:
			event, _ = window.read()
			if event in (sg.WIN_CLOSED, "-EXIT-", "OK"):
				break

"""
TODO:
	- Acomodar codigo de see_data() en sus respectivos archivos
"""

# window
def see_data(mydb):
	'''
	Esta es la ventana para la tabla filtro

	Es la función más grande que he hecho en mi vida,
	231 lineas de código...(O_O)
	'''

	# Obtener los nombres de las columnas de la tabla records_raw
	custom_name, real_name, table = obtener_columnas(mydb)

	# Definir operadores condicionales
	operadores = ['=', '>', '<', '>=', '<=', '<>', 'LIKE', 'BETWEEN']

	# Lista para almacenar las consultas y sus parámetros
	cola_querys = []

	col_ubi = col_ubi_layout(mydb)

	cond = "TRUE"

	consulta = """SELECT
    R.FOLIO AS 'Folio',
    CE.EVENTO_NAME AS 'Solicitud',
    R.Q_NAME AS 'Solicitante',
    CP.PLANTEL_NAME AS 'Plantel',
    CU.UBI_NAME AS 'Ubicación',
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
WHERE """

	window = sg.Window('Filtros de Tabla',  main_filter_layout(mydb, custom_name, operadores, col_ubi, consulta))

	# Event Loop
	while True:
		event, values = window.read()
		if event == sg.WINDOW_CLOSED or event == "-EXIT-":
			window.close()
			break

		
		if event == "seleccionar_todos":
			window["-FILTERS-"].update(visible = not values["seleccionar_todos"])
		else:
			window["-FILTERS-"].update(visible = not values["seleccionar_todos"])



		if event == "-PLANTEL-":
			window["-UBI-"].update(values = seleccionar_ubi_plantel(mydb, values["-PLANTEL-"]))

		elif event == "columna1":
			index_col = custom_name.index(values["columna1"])

			# Cambiar visibilidad de frame "Ubicacion"	
			if values["columna1"] == 'Ubicación':
				limpiar_default_filtros(window)

				window["-UBI_COL-"].update(visible = True)
				# window["operador1"].update(visible=False)
				window["valor1"].update(visible=False)

			# Cambiar visibilidad de frame "Fecha"
			elif values["columna1"] == "Fecha":
				limpiar_default_filtros(window)

				window["-DATE_COL-"].update(visible=True)
				window["-UBI_COL-"].update(visible = False)
				# window["operador1"].update(visible=False)
				window["valor1"].update(visible=False)

			# Cambiar visibilidad default
			else:
				limpiar_default_filtros(window)
				try:
					window["valor1"].update(values = seleccionar_valores_de_combos(mydb, real_name[index_col], table[index_col]))
				except:
					window["valor1"].update(values = [])

		elif event == ' + ':
			try:
				if values["seleccionar_todos"] == False:
					columna1 = values["columna1"]
					if columna1 == "Fecha":
						cond += f" AND R.DATE BETWEEN \"{values["-FECHA_DESDE-"]}\" AND \"{values["-FECHA_HASTA-"]}\""
					elif columna1 == "Ubicación":
						id_ubi = seleccionar_ID_UBI_X_UBI_NAME(mydb, values["-UBI-"])
						cond += f" AND R.ID_UBI = {id_ubi}"
					else:
						columna1 = values["columna1"]
						# operador1 = values["operador1"]
						valor1 = values["valor1"]
						index_col = custom_name.index(columna1)
						cond += f" AND {real_name[index_col]} = \"{valor1}\""

				cola_querys.append(cond)
				sg.popup(f"Consulta agregada a la cola:\nParametros: {cond}")
				
				
				cond = ""
			except Exception as err:
				sg.PopupError(f"Error en actualizar los filtros:\n{err}")

		elif event == 'Ejecutar Consultas':
			# Ejecutar todas las consultas acumuladas en la cola y actualizar la tabla
			try:
				resultados = []
				for parametros in cola_querys:
					consulta += parametros
				resultados.extend(ejecutar_consulta(mydb, consulta))

				window['tabla'].update(values=resultados)
				sg.popup("Consultas ejecutadas y tabla actualizada")
			except Exception as err:
				sg.PopupError(f"Error en la consulta:\n{err}")

		elif event == 'Limpiar Todo':
			# Limpiar valores de los controles de filtro y la lista de consultas en cola
			window['columna1'].update(value='')
			# window['operador1'].update(value='')
			window['valor1'].update(value='')
			window['-FECHA_DESDE-'].update(value='')
			window['-FECHA_HASTA-'].update(value='')
			window['seleccionar_todos'].update(value=False)
			window['lista_querys'].update(values=[])
			window['tabla'].update(values=[])

			window["-FILTERS-"].update(visible = True)

			window["-DATE_COL-"].update(visible=False)
			window["-UBI_COL-"].update(visible = False)
			# window["operador1"].update(visible=True)
			window["valor1"].update(visible=True)
			cond = "TRUE"
			cola_querys = []
			consulta = """SELECT
    R.FOLIO AS 'Folio',
    CE.EVENTO_NAME AS 'Solicitud',
    R.Q_NAME AS 'Solicitante',
    CP.PLANTEL_NAME AS 'Plantel',
    CU.UBI_NAME AS 'Ubicación',
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
WHERE """


		# pestañas limpiar
		elif event == 'Limpiar Tabla':
			window['tabla'].update(values=[])

		elif event == 'Limpiar Filtros':
			window['columna1'].update(value='')
			# window['operador1'].update(value='')
			window['valor1'].update(value='')
			window['seleccionar_todos'].update(value=False)
			window['-FECHA_DESDE-'].update(value='')
			window['-FECHA_HASTA-'].update(value='')

			window["-FILTERS-"].update(visible = True)

			window["-DATE_COL-"].update(visible=False)
			window["-UBI_COL-"].update(visible = False)
			# window["operador1"].update(visible=True)
			window["valor1"].update(visible=True)

		elif event == 'Limpiar Consultas':
			cola_querys = []
			window['lista_querys'].update(values=[])
			cond = "TRUE"

		
		# pestañas copiar
		elif event == "Consulta base":
			clipboard.copy(consulta)
			sg.Popup("Consulta copiada con exito!")

		elif event == "Condiciones":
			temp = ""
			for c in cola_querys:
				temp += "".join(c)
			clipboard.copy(temp)
			sg.Popup("Consulta copiada con exito!")
			del temp

		elif event == "Query Actual":
			temp = ""
			for c in cola_querys:
				temp += "".join(c)
			clipboard.copy(c_temp)
			sg.Popup("Consulta copiada con exito!")
			del c_temp
			del temp



		elif event == "tabla":
			datos = window["tabla"].get()
			ic(datos)



		# Actualizar la lista de queries en cola
		window['lista_querys'].update(
			values=[f"{cond}" for cond in cola_querys])