import PySimpleGUI as sg
import os
import datetime
from icecream import ic
import pyperclip as clipboard

'''
Este archivo es para poder alamcenar funciones genericas que no son 
ni ventanas, layouts o queries, si no simples funciones.

en las funciones donde se limpian los filtros, tienes que meter como
parametro la ventana que creaste y que quieres que se obtengan los 
datos
'''


# function
def clear(window):
	"""
	Limpia los inputs de la ventana add_records_window() de
	[windows_v0_1_1B4]
	"""
	window['-CALL_TYPE-'].update('')
	window['-UBICATION-'].update('')
	window['-MACHINE-'].update('')
	window['-NAME_USER_MACHINE-'].update('')
	window['-DATE-'].update("##-##-##")
	# window['-DATE_BTN-'].update('')
	window['-HOUR-'].update('')
	window['-MINUTES-'].update('')
	window['-PROB_USER-'].update('')
	window['-PROB_TI-'].update('')
	window['-COMMENTS-'].update('')
	window['-STATUS_TYPE-'].update('')


# function
def es_hora_valida(horas, minutos):
	"""
	Checa si la hora ingresada está en formato 24 y además es un
	formato valido
	"""
	try:
		# Convierte las entradas a enteros
		horas = int(horas)
		minutos = int(minutos)

		# Verifica si las horas y los minutos están en los rangos válidos
		if 0 <= horas <= 23 and 0 <= minutos <= 59:
			return True
		else:
			return False
	except ValueError:
		return False

def copy_str(text):
	'''
	¿Te suena "Crtl + C"?
	'''
	clipboard.copy(text)



def limpiar_default_filtros(window):
	'''
	Limpia los filtros
	'''
	window["-DATE_COL-"].update(visible=False)
	window["-UBI_COL-"].update(visible = False)
	# window["operador1"].update(visible=True)
	window["valor1"].update(visible=True)