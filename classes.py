class User:
	def __init__(self, *data):
		print(f'DATA:\t',end='')
		print(*data)
		self.id_usuario=int(data[0])
		self.usuario_name=data[1]
		self.id_rol=bool(int(data[2]))