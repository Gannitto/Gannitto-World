import socket, threading, time

class Client:
	def __init__(self):
		self.key = 8194
		self.shutdown = False
		self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.host = socket.gethostbyname(socket.gethostname())
		self.port = 0
		self.s.bind((self.host, self.port))
		self.s.setblocking(0)
		self.rT = threading.Thread(target = self.receving, args = ("RecvThread",self.s))
		self.rT.start()
	def receving (self, name, sock):
		while not self.shutdown:
			try:
				while True:
					data, addr = sock.recvfrom(1024)
					#print(data.decode("utf-8"))

					# Begin
					decrypt = ""; k = False
					for i in data.decode("utf-8"):
						if i == ":":
							k = True
							decrypt += i
						elif k == False or i == " ":
							decrypt += i
						else:
							decrypt += chr(ord(i)^self.key)
					print(decrypt)
					# End

					time.sleep(0.2)
			except:
				pass
	def main(self, nickname: str, server: str, x, y, creater=False):
		join = False
		server = (self.host, 9090)
		
		alias = nickname
		
		if join == False:
			self.s.sendto(("["+alias + "] => join").encode("utf-8"),server)
			join = True
		else:
			try:
				message = str(creater) + "¤" + str(x) + "¤" + str(y) + "¤" + nickname

				# Begin
				crypt = ""
				for i in message:
					crypt += chr(ord(i)^self.key)
				message = crypt
				# End

				if message != "":
					self.s.sendto(("["+alias + "] :: " + message).encode("utf-8"),server)
		
				time.sleep(0.2)
			except:
				self.s.sendto(("["+alias + "] <= left").encode("utf-8"),server)
				self.shutdown = True
				self.rT.join()
				self.s.close()
				return "Exit"

client = Client()
