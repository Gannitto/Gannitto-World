class Player:

	def __init__(self, connection_socket, addr, x, y, nickname):
		
		self.connection_socket = connection_socket
		self.addr = addr

		self.x = x
		self.y = y
		self.nickname = nickname

		self.errors = 0

		self.run = "Down"
		self.costum = 1
		self.changed_item = None

players = []
