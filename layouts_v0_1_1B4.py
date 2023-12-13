import PySimpleGUI as sg
import os
import datetime

from connect_mariadb_v0_1_1B4 import *

'''
Este archivo es para tener acomodados los layouts de las diferentes 
ventanas y menús.

PAra evitar andar creando conexiónes con la base de datos, sugiero que
si vas a crear una nueva ventana con algun layout que ocupe datos de
la BD, metas como parametro a las funciones la conexión a la BD
'''
	

	
def retry_connect_layout():
	'''
	Esta funcion hace que cuando no logres conectarte a la BD agregue 
	un Pop-Up con posibilidad de reconectarte a la BD
	'''
	return [
		[sg.T("Host: "), sg.P(), sg.I(s = (17, 1), k = "-HOST-")],
		[sg.T("User: "), sg.P(), sg.I(s = (17, 1), k = "-USER-")],
		[sg.T("Pass: "), sg.P(), sg.I(s = (17, 1), k = "-PASS-")],
		[sg.T("DB: ")  , sg.P(),   sg.I(s = (17, 1), k = "-DB-")],
		[sg.P(), sg.B("Salir", k = "-EXIT-"), sg.B("Connect", k = "-CONN-")]
	]

def menu_bar_layout():
	"""
	Este es el layout para la barra de tareas o pestañas que aparecen 
	en los menus principales del CEMV
	"""		
	return [
		['Acerca de...', ["About"]],
	]

def login_window():
	"""
	Este es el layout basico del inicio de sesión del CEMV
	"""
	return [
		[sg.Menu(menu_bar_layout())],
		[sg.T("ID: "), sg.P(), sg.I(k = "-ID_USER-", s = (10, 1))],
		[sg.T("Contraseña: "), sg.P(), sg.I(password_char = "*", k = "-PASS_USER-", s = (10, 1))],
		[sg.P(), sg.B("Cancelar", k = "-CANCEL-"), sg.B("Continuar >", k = "-CONTINUE-", bind_return_key = True)],
	]

def about_layout(mydb):
	'''
	Este layout es para la venana "About"
	'''
	return [
		[sg.P(), sg.Image(source = select_image_from_database(mydb)), sg.P()],
		[sg.P(), sg.T("CEMV"), sg.P()],
		[sg.P(), sg.T("Centro de Eventos y Monitoreo Virtual"), sg.P()],
		[sg.P(), sg.T("Registrado a Carlos Emilio Mejía Vázquez"), sg.P()],
		[sg.P(), sg.T(f"Copyright {datetime.datetime.now().year} • Fni Uvkhiv"), sg.P()],
		[sg.P(), sg.T("Version 0.1.1, Build 4"), sg.P()]
	]


def admin_menu():
	'''
	Este es el layout para el menu principal del rol Admin
	'''
	return [
		[sg.Menu(menu_bar_layout())],
		[sg.B("Agregar Registro", k = "-ADD_RECORD-")],
		[sg.B("Ver Registros", k = "-SEE_RECORDS-")],
		[sg.B("Administrar Registros", k = "-MAN_RECORDS-")],
		[sg.B("Administrar Usuarios", k = "-MAN_USERS-")],
		[sg.B("Configuración", k = "-CONFIG-")],
	]


def user_menu():
	'''
	Este es el layout para el menu principal del rol Usuario
	'''
	return [
		[sg.Menu(menu_bar_layout())],
		[sg.B("Agregar Registro", k = "-ADD_RECORD-")],
		[sg.B("Ver Registros", k = "-SEE_RECORDS-")],
	]


def viewer_menu():
	'''
	Este es el layout para el menu principal del rol Viewer
	'''
	return [
		[sg.Menu(menu_bar_layout())],
		[sg.B("Ver Registros", k = "-SEE_RECORDS-")],
	]


def add_records_window_layout(mydb):
	'''
	Este es el layout de la ventana para agregar registros
	'''

	col1 = [
		[sg.T("Tipo de llamado:"),
		 sg.P(),
		 sg.Combo(get_evento(mydb), k ="-CALL_TYPE-", readonly = True, s = (25, 1))
		],
		
		[sg.T("Ubicación:"),
		 sg.P(),
		 sg.Combo(get_plantel(mydb), k = "-UBICATION-", readonly = True, enable_events = True, s = (25, 1))
		],
		
		[sg.T("Maquina y/o Salón: "),
		 sg.P(),
		 sg.Combo(values = [],k = "-MACHINE-", readonly = True, s = (25, 1))
		],
		
		[sg.T("Quien levantó la solicitud: "),
		 sg.P(),
		 sg.I(k="-NAME_USER_MACHINE-")
		]
	]

	col2 = [
		[sg.T("Fecha de la llamada:")
		],
		
		[sg.I("##-##-##", k = "-DATE-", readonly = True, s = (10, 1)),
		 sg.CalendarButton("Calendar", format="%Y-%m-%d", k = "-DATE_BTN-")
		],
		
		[sg.T("Hora de la llamada (24H -> HH:MM):")
		],
		
		[sg.I(k = "-HOUR-", s = (4, 1), enable_events = True),
		 sg.T(":"),
		 sg.I(k = "-MINUTES-", s = (4, 1), enable_events = True)
		]
	]

	col3 = [
		[sg.T("Problema según quien levantó la solicitud: ")
		],
		
		[sg.Multiline(s=(None, 5), k = "-PROB_USER-")
		],
		
		[sg.T("Descripción del equipo de sistemas y pasos de resolución del problema: ")
		],
		
		[sg.Multiline(s=(None, 5), k = "-PROB_TI-")
		],
		
		[sg.T("Comentarios y/u Observaciones:")
		],
		
		[sg.Multiline(s=(None, 5), k = "-COMMENTS-")
		],
		
		[sg.T("Estatus:"), sg.Combo(get_estatus(mydb), k ="-STATUS_TYPE-", readonly = True)
		],
	]

	layout = [
		[sg.Column(col1),
		 sg.Column(col2)
		],
		
		[sg.Column(col3)
		],
		
		[
		 sg.B("Enviar", k = "-SAVE-"),
		 sg.B("Developer", k = "-DEV-", visible = False),
		 sg.P(),
		 sg.B("Limpiar", k = "-CLEAR-", button_color = ("#ffffff", "#ff0000"))
		]

	]

	return layout

def save_records_popup_layout():
	'''
	Este es el layout de confirmación de guardar datos
	'''
	return [
		[sg.T("Está seguro de que quiere guardar los datos?")],
		[sg.Cancel(), sg.Yes()]
	]

def popup_Error_layout():
	'''
	Este es el layout del Pop-Up cuando ingresas un dato erroneo en 
	add_records_window_layout()
	'''
	return [
		[sg.T("Error: ")],
		[sg.I(Error, readonly = True)],
		[sg.OK()]
	]

"""
TODO:
	- Acomodar layouts de see_data()
"""

def col_ubi_layout(mydb):
	'''
	Este es parte del Layout de la tabla de filtros, aquí está la
	columna de plantel/ubicación
	'''
	return  [
		[sg.T("Plantel:"), sg.Combo(k = "-PLANTEL-", values = seleccionar_plantel(mydb), enable_events = True)],
		[sg.T("Ubicacion:"), sg.Combo(k = "-UBI-", values = [], s = (15, 1))]
	]



def table_filter_bar_layout(mydb):
	'''
	Este es el layout del menu superior de la tabla de filtros, con
	las acciones de borrar y copiar
	'''
	return [
		["Limpiar", 
			["Limpiar Tabla", "Limpiar Filtros", "Limpiar Consultas", "Limpiar Todo"]
		],
		["Copiar",
			["Consulta base", "Condiciones", "Query Actual"]
		]
	]

def filters_layout(mydb, custom_name, operadores, col_ubi):
	'''
	Este es parte del layout de la tabla de filtros, principalmente,
	aquí está el layout del filtro de fechas de la tabla
	'''
	return [
		[
			sg.Combo(custom_name, key='columna1', enable_events=True),
			# sg.Combo(operadores, key='operador1', visible=True),
			sg.Combo([], key='valor1', visible=True, s = (10, 1)),
			sg.Column(col_ubi, visible = False, k = "-UBI_COL-"),
			sg.Column(
				layout = 
	 			[
	 				[
						sg.CalendarButton('Fecha Desde', k="-FECHA_DESDE_BTN-", format="%Y-%m-%d", s=(12, 1)),
		  				sg.I(k="-FECHA_DESDE-", s=(12, 1))
		  			],
		 			[
		 				sg.CalendarButton('Fecha Hasta', k="-FECHA_HASTA_BTN-", format="%Y-%m-%d", s=(12, 1)),
		  				sg.I(k="-FECHA_HASTA-", s=(12, 1))
		  			]
				],
				visible = False, 
				k = "-DATE_COL-")
	 		]
	]

def main_filter_layout(mydb, custom_name, operadores, col_ubi, consulta):
	'''
	Layout principal de la tabla de filtros, aqui se juntan todos los
	layout relacionados a la tabla de filtros
	'''
	return [
		[sg.Menu(table_filter_bar_layout(mydb))],
		[sg.Text('Filtrar por:')],
		[sg.Column(filters_layout(mydb, custom_name, operadores, col_ubi), k = "-FILTERS-",	visible = True)],
		[sg.Checkbox('Seleccionar Todos', key='seleccionar_todos', enable_events = True)],
		[sg.Button(' + Agregar condición', k = " + ")],
		[sg.Button('Ejecutar Consultas', button_color = ("#000000", "#33ff33"))],
		[sg.Table(headings=custom_name, values=[], auto_size_columns=False, justification='right', key='tabla', enable_events = True)],
		[sg.Column(
			[
			 [sg.T("Query:"), sg.P(), sg.Multiline(consulta, disabled = True, s = (50, 4))],
			 [sg.T("Condiciones:"), sg.P(), sg.Listbox(values=[], size=(50, 4), key='lista_querys')],
			]
		)],
		
		[sg.P(), sg.B("< Regresar", k = "-EXIT-", button_color = ("#ffffff", "#ff0000"))]
	]