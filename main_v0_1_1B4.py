from windows_v0_1_1B4 import *

'''
Este es el archivo principal del CEMV, de aquí se llaman a todas las
otras ventanas (por medio de windows_vx_x_xBx.py)

Aquí se maneja el menú principal, teoricamente es facil modificar el
código para que cuando se quieran salir los regrese al inicio de
sesión.

Si quieren agregar un nuevo rol, aquí agregan la llamada para la nueva
ventana
'''

option = None

mydb = connect_to_database()
while mydb == None:
	mydb = retry_connect()
	if mydb == -1:
		break

if mydb != -1:
	while True:
		data = login_menu(mydb)
		if data != None: break

	if not data[0] == False and not data[1] == None:
		while True:	
			rol = data[1][2]
			if rol == 0:
				option = menu_window(mydb, rol)
			elif rol == 1:
				option = menu_window(mydb, rol)
			elif rol == 2:
				option = menu_window(mydb, rol)
			else:
				option = None

			if option == None:
				break
			
			if isinstance(option, int):
			
				if option == 1: add_records_window(mydb, data[1])
				if option == 2: see_data(mydb)
				if option == 6: about_window(mydb)
		
			del rol
			del option
	del data

	mydb.close()