import socket

class Server:
	def __init__(self):
		self.host = socket.gethostbyname(socket.gethostname())
		print(socket.gethostbyname(socket.gethostname()))
		self.port = 9090
		self.clients = []
		self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.s.bind((self.host, self.port))
	def main(self):
		try:
			data, addr = self.s.recvfrom(1024)

			if addr not in self.clients:
				self.clients.append(addr)
			
			for client in self.clients:
				if addr != client:
					self.s.sendto(data,client)
			return addr
		except:
			self.s.close()
			return "Close"

server = Server()
