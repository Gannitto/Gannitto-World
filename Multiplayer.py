import socket
import threading
import json
import time
import uuid
import upnpclient
from typing import Dict, List, Optional
from Sound import play_sound
from Functions import destroy_object
from Classes import Object, Particle, Farmland, Wall, Projectile

# Версия протокола для совместимости
PROTOCOL_VERSION = 1

class NetworkManager:
	"""Основной класс для управления сетевым взаимодействием"""
	
	def __init__(self, Peer, chat_message, view_distance):
		self.role = "Disconnected"
		self.socket: Optional[socket.socket] = None
		self.running = False
		self.peers = {}  # id -> Peer
		self.player_id = self._generate_id()
		self.encryption_key = b"gannitto_world_secret_key_123456"  # Простой ключ шифрования (временно)
		self.Peer = Peer
		self.chat_message = chat_message
		self.view_distance = view_distance
		self.last_heartbeat = time.time()
		self.server_events = {"Game": []}
		self.port = 5555
		self.external_port = self.port
		self.host_ip = ""
		self.host_port = 5555
		
		# Потоки
		self.receive_thread: Optional[threading.Thread] = None
		self.send_queue: List[Dict] = []
		self.lock = threading.Lock()
		
		# Информация о хосте для подключения
		self.host_address = None
		
	def _generate_id(self) -> str:
		"""Генерирует уникальный ID для игрока"""
		return str(uuid.uuid4())[:8]
	
	def _encrypt_data(self, data: bytes) -> bytes:
		"""Простое XOR шифрование для защиты от случайного перехвата"""
		key = self.encryption_key
		return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
	
	def _decrypt_data(self, data: bytes) -> bytes:
		"""Расшифровка данных"""
		return self._encrypt_data(data)  # XOR симметричен

	def _get_local_ip(self) -> str:
		"""Получение локального IP адреса"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			ip = s.getsockname()[0]
			s.close()
			return ip
		except:
			return "127.0.0.1"

	def _get_public_ip(self) -> str:
		"""Получение публичного IP через STUN (упрощенная версия)"""
		try:
			# Простой способ - через запрос к внешнему серверу
			import urllib.request
			with urllib.request.urlopen('https://api.ipify.org', timeout=2) as response:
				return response.read().decode('utf-8')
		except:
			return self._get_local_ip()

	def get_exclude_ids(self, X, Y, sended_peer=None):
		"""Получение списка пиров, которым не нужно присылать пакет данных"""
		exclude_ids = []
		if sended_peer is not None:
			exclude_ids.append(sended_peer)
		for pid, peer in self.peers.items():
			center_chunk_x = int(peer.x // 2048) * 2048
			center_chunk_y = int(peer.y // 2048) * 2048
			if not (center_chunk_x - 2048 * peer.view_distance <= X <= center_chunk_x + 2048 * (peer.view_distance + 1) and center_chunk_y - 2048 * peer.view_distance <= Y <= center_chunk_y + 2048 * (peer.view_distance + 1)):
				exclude_ids.append(pid)
		return exclude_ids

	def setup_upnp(self, port: int = 5555) -> bool:
		"""Автоматический проброс портов через UPnP"""
		try:
			# Ищем UPnP устройства в сети
			devices = upnpclient.discover()
			
			if not devices:
				self.chat_message("UPnP не поддерживается роутером")
				return False
			
			for device in devices:
				try:
					# Пробрасываем порт
					result = device.WANIPConn1.AddPortMapping(
						NewRemoteHost="",
						NewExternalPort=port,
						NewProtocol="UDP",
						NewInternalPort=port,
						NewInternalClient=self._get_local_ip(),
						NewEnabled="1",
						NewPortMappingDescription="GannittoWorld",
						NewLeaseDuration=3600
					)
					self.chat_message(f"Порт {port} проброшен через UPnP")
					return True
				except:
					continue
			
			return False
		except Exception as e:
			self.chat_message(f"Ошибка UPnP: {e}")
			return False

	def start_host(self, port: int = 5555, external_port: int = None) -> bool:
		"""Запуск как хоста (сервера)"""
		try:
			self.setup_upnp(port)
			# Используем UDP
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.settimeout(0.1)
			
			# Привязываемся ко всем интерфейсам
			self.socket.bind(("0.0.0.0", port))
			self.role = "Host"
			self.running = True
			
			# Получаем реальный IP
			local_ip = self._get_local_ip()
			
			# ПЫТАЕМСЯ ПОЛУЧИТЬ ПУБЛИЧНЫЙ IP
			public_ip = None
			try:
				public_ip = self._get_public_ip()
				self.chat_message(f"Ваш публичный IP: {public_ip}")
			except:
				self.chat_message("Не удалось определить публичный IP")
			
			# Используем публичный IP для внешних подключений
			# Но для локальных подключений оставляем локальный IP
			host_ip = public_ip if public_ip else local_ip
			
			# Добавляем себя как первого пира
			self.peers[self.player_id] = self.Peer(
				id=self.player_id,
				address=(host_ip, external_port if external_port else port),  # Используем external_port если указан
				name=f"Host_{self.player_id[:4]}",
				last_seen=time.time(),
				view_distance=self.view_distance
			)
			
			# Запускаем потоки
			self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
			self.receive_thread.start()
			
			self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
			self.heartbeat_thread.start()
			
			# ПОКАЗЫВАЕМ ИНФОРМАЦИЮ ДЛЯ ПОДКЛЮЧЕНИЯ
			self.chat_message("=" * 50)
			self.chat_message("СЕРВЕР ЗАПУЩЕН!")
			self.chat_message(f"Локальный IP: {local_ip}:{port}")
			if public_ip:
				self.chat_message(f"ПУБЛИЧНЫЙ IP: {public_ip}:{external_port if external_port else port}")
				self.chat_message("Для подключения по интернету используйте публичный IP")
			else:
				self.chat_message("ВНИМАНИЕ: Публичный IP не определен!")
				self.chat_message("Попробуйте узнать свой IP на сайте 2ip.ru")
			
			if external_port and external_port != port:
				self.chat_message(f"Внешний порт: {external_port} (отличается от внутреннего)")
			
			self.chat_message("=" * 50)
			
			return True
			
		except Exception as e:
			self.chat_message(f"Не удалось запустить хост: {e}")
			return False

	def connect_to_host(self, host_ip: str, port: int = 5555) -> bool:
		"""Подключение к хосту"""
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socket.settimeout(5.0)  # Увеличиваем таймаут для интернета
			self.role = "Client"
			self.running = True
			self.host_address = (host_ip, port)
			
			self.chat_message(f"Подключаюсь к {host_ip}:{port}...")
			
			# Отправляем несколько раз для надежности (UDP может терять пакеты)
			for i in range(5):
				self._send_packet({
					"type": "handshake",
					"player_id": self.player_id,
					"name": f"Player_{self.player_id[:4]}",
					"view_distance": self.view_distance,
					"timestamp": time.time()
				}, self.host_address)
				time.sleep(0.2)
			
			# Запускаем потоки
			self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
			self.receive_thread.start()
			
			self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
			self.heartbeat_thread.start()
			
			self.chat_message(f"Отправлены запросы на подключение к {host_ip}:{port}")
			return True
			
		except Exception as e:
			self.chat_message(f"Не удалось подключиться к хосту: {e}")
			return False

	def start_local_host(self, port: int = 5555) -> bool:
		"""Запуск как хоста (сервера)"""
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# UDP протокол
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind(("0.0.0.0", port))
			self.socket.settimeout(1.0)  # Таймаут для проверки соединения
			self.role = "Host"
			self.running = True
			
			# Добавляем себя как первого пира
			self.peers[self.player_id] = self.Peer(
				id=self.player_id,
				address=("127.0.0.1", port),
				name=f"Host_{self.player_id[:4]}",
				last_seen=time.time(),
				view_distance=self.view_distance
			)
			
			# Запускаем поток получения
			self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
			self.receive_thread.start()
			
			# Запускаем поток проверки соединений
			threading.Thread(target=self._heartbeat_loop, daemon=True).start()
			
			self.chat_message(f"Хост запущен на IP {self._get_local_ip()} и порту {port}")
			self.chat_message(f"Твой ID игрока: {self.player_id}")
			return True
			
		except Exception as e:
			self.chat_message(f"Не удалось запустить хост: {e}")
			return False
	
	def connect_to_local_host(self, host_ip: str, port: int = 5555) -> bool:
		"""Подключение к хосту"""
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.socket.settimeout(1.0)
			self.role = "Client"
			self.running = True
			self.host_address = (host_ip, port)
			
			# Отправляем приветственное сообщение хосту
			self._send_packet({
				"type": "handshake",
				"player_id": self.player_id,
				"name": f"Player_{self.player_id[:4]}",
				"view_distance": self.view_distance
			}, self.host_address)
			
			# Запускаем поток получения
			self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
			self.receive_thread.start()
			
			self.chat_message(f"Подключено к хосту {host_ip}:{port}")
			return True
			
		except Exception as e:
			self.chat_message(f"Не удалось подключиться к хосту: {e}")
			return False
	
	def _receive_loop(self):
		"""Основной цикл получения сообщений"""
		while self.running and self.socket:
			try:
				data, addr = self.socket.recvfrom(65535)
				
				if not data:
					continue
				
				# Расшифровываем и парсим
				decrypted = self._decrypt_data(data)
				try:
					packet = json.loads(decrypted.decode("utf-8"))
				except json.JSONDecodeError:
					continue
				
				# Обрабатываем пакет в зависимости от роли
				if self.role == "Host":
					self._handle_packet_as_host(packet, addr)
				else:
					self._handle_packet_as_client(packet, addr)
					
			except socket.timeout:
				continue
			except Exception as e:
				if self.running:
					self.chat_message(f"Ошибка получения: {e}")
					break
	
	def _handle_packet_as_host(self, packet: Dict, addr: tuple):
		"""Обработка пакетов на стороне хоста"""
		print("Получен пакет:", packet)
		packet_type = packet.get("type")
		player_id = packet.get("player_id")
		with self.lock:
			if player_id in self.peers:
				self.peers[player_id].last_seen = time.time()

		match packet_type:
			case "handshake":
				# Новый игрок подключается
				# Используем блокировку при добавлении
				with self.lock:
					if player_id not in self.peers:
						peer = self.Peer(
							id=player_id,
							address=addr,
							name=packet.get("name", f"Player_{player_id[:4]}"),
							last_seen=time.time(),
							view_distance=packet.get("view_distance")
						)
						self.peers[player_id] = peer
						self.server_events[player_id] = []
						self.chat_message(f">>> Подключился игрок {player_id} с {addr}")
				
				# Отправляем список (вне блокировки, чтобы не блокировать надолго)
				self._send_peer_list_to(player_id)
				
				# Оповещаем всех остальных
				self._broadcast({
					"type": "peer_joined",
					"peer": {
						"id": player_id,
						"name": peer.name,
						"x": peer.x,
						"y": peer.y,
						"direction": peer.direction,
						"changed_item": peer.changed_item
					}
				}, player_id)

				self.server_events["Game"].append({"type": "event", "event_type": "peer_joined", "address": addr})

			case "disconnect":
				# Игрок отключается
				self._remove_peer(player_id)

			case "get_chunk":
				self.server_events["Game"].append({
					"type": "event",
					"event_type": "get_chunk",
					"player_id": packet.get("player_id"),
					"chunk_key": packet.get("chunk_key")
					})
				
			case "event":

				for event in packet.get("events"):
					match event.get("event_type"):
						case "player_moved":
							# Обновление позиции игрока
							# with self.lock:
							#	if player_id in self.peers:
							#		self.peers[player_id].move(event.get("x"), event.get("dy"), 40)
							#		self.peers[player_id].last_seen = time.time()
							
							# Пересылаем движение всем остальным (вне блокировки)
							self.server_events[player_id].append(event)
							exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "player_moved",
								"player_id": player_id,
								"x": event.get("x"),
								"y": event.get("y"),
								"direction": event.get("direction")
							}, exclude_ids)

						case "player_tp":
							self.server_events[player_id].append(event)
							exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "player_tp",
								"player_id": player_id,
								"x": event.get("x"),
								"y": event.get("y"),
								"direction": event.get("direction")
							}, exclude_ids)

						case "player_stopped":
							self.server_events[player_id].append(event)
							exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "player_stopped",
								"player_id": player_id
							}, exclude_ids)

						case "object_added":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("object").get("x"), event.get("object").get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "object_added",
								"player_id": "Game",
								"object": event.get("object")
							}, exclude_ids)

						case "object_removed":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "object_removed",
								"player_id": "Game",
								"x": event.get("x"),
								"y": event.get("y"),
								"name": event.get("name")
							}, exclude_ids)

						case "object_started_breaking":
							self.server_events[player_id].append(event)
							exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "object_started_breaking",
								"player_id": player_id,
								"x": event.get("x"),
								"y": event.get("y"),
								"name": event.get("name")
							}, exclude_ids)

						case "object_stopped_breaking":
							self.server_events[player_id].append(event)
							exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "object_stopped_breaking",
								"player_id": player_id,
								"x": event.get("x"),
								"y": event.get("y"),
								"name": event.get("name")
							}, exclude_ids)

						case "item_added":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("item").get("x"), event.get("item").get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "item_added",
								"player_id": "Game",
								"item": event.get("item")
							}, exclude_ids)

						case "item_removed":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "item_removed",
								"player_id": "Game",
								"x": event.get("x"),
								"y": event.get("y"),
								"name": event.get("name")
							}, exclude_ids)

						case "wall_added":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("wall").get("x"), event.get("wall").get("y"), player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "wall_added",
								"player_id": "Game",
								"wall": event.get("wall")
							}, exclude_ids)

						case "wall_removed":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("break_pos")[0], event.get("break_pos")[1], player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "wall_removed",
								"player_id": "Game",
								"break_pos": event.get("break_pos")
							}, exclude_ids)
					
						case "wall_interaction":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("wall_pos")[0], event.get("wall_pos")[1], player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "wall_interaction",
								"player_id": "Game",
								"wall_pos": event.get("wall_pos")
							}, exclude_ids)
					
						case "farmland_added":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							exclude_ids = self.get_exclude_ids(event.get("farmland_pos")[0], event.get("farmland_pos")[1], player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "farmland_added",
								"player_id": "Game",
								"farmland_pos": event.get("farmland_pos")
							}, exclude_ids)
					
						case "projectile_added":
							event["player_id"] = "Game"
							self.server_events["Game"].append(event)
							self._broadcast({
								"type": "server_event",
								"event_type": "projectile_added",
								"player_id": "Game",
								"x": event.get("x"),
								"y": event.get("y"),
								"mouse_x": event.get("mouse_x"),
								"mouse_y": event.get("mouse_y"),
								"projectile_type": event.get("projectile_type")
							}, player_id)
					
						case "changed_item":
							self.server_events[player_id].append(event)
							exclude_ids = self.get_exclude_ids(self.peers[player_id].x, self.peers[player_id].y, player_id)
							self._broadcast({
								"type": "server_event",
								"event_type": "changed_item",
								"player_id": player_id,
								"changed_item": event.get("changed_item")
							}, exclude_ids),
					
						case "chat_message":
							self.chat_message(event.get("message_text"))
							self.server_events[player_id].append(event)
							self._broadcast({
								"type": "server_event",
								"event_type": "chat_message",
								"player_id": "Game",
								"message_text": event.get("message_text")
							}, player_id)

	def _handle_packet_as_client(self, packet: Dict, addr: tuple):
		"""Обработка пакетов на стороне клиента"""
		print("Получен пакет:", packet)
		packet_type = packet.get("type")
		match packet_type:
			case "peer_list":
				# Получение списка всех игроков от хоста
				peers_data = packet.get("peers", {})
				for pid, pdata in peers_data.items():
					self.peers[pid] = self.Peer(
						id=pid,
						address=addr,
						name=pdata.get("name", f"Player_{pid[:4]}"),
						last_seen=time.time(),
						X=pdata.get("x"),
						Y=pdata.get("y"),
						view_distance=pdata.get("view_distance")
					)
					self.peers[pid].direction = pdata.get("direction")
					self.peers[pid].changed_item = pdata.get("changed_item")

			case "peer_joined":
				# Новый игрок присоединился
				pdata = packet.get("peer", {})
				pid = pdata.get("id")
				if pid and pid != self.player_id:
					peer = self.Peer(
						id=pid,
						address=addr,
						name=pdata.get("name", f"Player_{pid[:4]}"),
						last_seen=time.time(),
						X=pdata.get("x", 0),
						Y=pdata.get("y", 0),
						view_distance=pdata.get("view_distance")
					)
					self.peers[pid] = peer
					self.peers[pid].direction = pdata.get("direction")
					self.peers[pid].changed_item = pdata.get("changed_item")
					self.server_events[pid] = []
						
			case "peer_left":
				# Кто-то отключился
				pid = packet.get("player_id")
				self._remove_peer(pid)
				
			case "server_event":
				pid = packet.get("player_id")
				if pid and pid != self.player_id and (pid in self.peers or pid == "Game"):
					if pid not in self.server_events:
						self.server_events[pid] = []
					self.server_events[pid].append(packet)
					if pid != "Game":
						self.peers[pid].last_seen = time.time()
	
	def _send_packet(self, packet: Dict, address: tuple):
		"""Отправка зашифрованного пакета"""
		if not self.socket:
			return False
			
		try:
			data = json.dumps(packet).encode("utf-8")
			encrypted = self._encrypt_data(data)
			self.socket.sendto(encrypted, address)
			print(f"Отправлен пакет: {packet}")
			return True
		except Exception as e:
			self.chat_message(f"Ошибка отправки: {e}")
			return False
	
	def _broadcast(self, packet: Dict, exclude_ids: List[str] = None):
		"""Отправка пакета всем известным пирам (только хост)"""
		if self.role != "Host":
			return
			
		exclude_ids = exclude_ids or []
		
		# Важно: создаем копию словаря для итерации, чтобы не изменять оригинал
		with self.lock:
			peers_copy = dict(self.peers.items())  # Создаем копию
		
		# Итерируемся по копии
		for pid, peer in peers_copy.items():
			if pid not in exclude_ids:
				self._send_packet(packet, peer.address)	
	def _broadcast_except(self, packet: Dict, exclude_id: str):
		"""Отправка пакета всем, кроме указанного игрока"""
		self._broadcast(packet, [exclude_id])
	
	def _send_peer_list_to(self, player_id: str):
		"""Отправляет список всех игроков конкретному игроку"""
		if self.role != "Host":
			return
			
		if player_id not in self.peers:
			return
			
		peers_data = {}
		for pid, peer in self.peers.items():
			peers_data[pid] = {
				"name": peer.name,
				"x": peer.x,
				"y": peer.y,
				"direction": peer.direction,
				"changed_item": peer.changed_item,
				"view_distance": peer.view_distance
			}
			
		self._send_packet({
			"type": "peer_list",
			"peers": peers_data
		}, self.peers[player_id].address)
	
	def send_heartbeat(self):
		"""Отправка ритма"""
		self.last_heartbeat = time.time()
		packet = {
			"type": "idle",
			"player_id": self.player_id,
		}
		
		if self.role == "Host":
			# Хост отправляет всем, кроме себя
			self._broadcast_except(packet, self.player_id)
		elif self.role == "Client" and self.host_address:
			# Клиент отправляет только хосту
			self._send_packet(packet, self.host_address)
	
	def send_events(self, events: tuple):
		"""Отправка событий"""
		if self.role == "Host":
			packet = None
			for event in events:
				match event.get("event_type"):
					case "player_moved":
						exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"))
						packet = {
							"type": "server_event",
							"event_type": "player_moved",
							"player_id": self.player_id,
							"x": event.get("x"),
							"y": event.get("y"),
							"direction": event.get("direction")
						}
					case "player_tp":
						exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"))
						packet = {
							"type": "server_event",
							"event_type": "player_tp",
							"player_id": self.player_id,
							"x": event.get("x"),
							"y": event.get("y"),
							"direction": event.get("direction")
						}
					case "player_stopped":
						exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"))
						packet = {
							"type": "server_event",
							"event_type": "player_stopped",
							"player_id": self.player_id,
							"x": event.get("x"),
							"y": event.get("y"),
						}
					case "ron_moved":
						packet = {
							"type": "server_event",
							"event_type": "ron_moved",
							"player_id": "Game",
							"x": event.get("x"),
							"y": event.get("y"),
							"direction": event.get("direction")
						}

					case "object_added":
						exclude_ids = self.get_exclude_ids(event.get("object").get("x"), event.get("object").get("y"), self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "object_added",
							"player_id": "Game",
							"object": event.get("object")
						}

					case "object_removed":
						exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "object_removed",
							"player_id": "Game",
							"x": event.get("x"),
							"y": event.get("y"),
							"name": event.get("name")
						}

					case "object_started_breaking":
						exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "object_started_breaking",
							"player_id": self.player_id,
							"x": event.get("x"),
							"y": event.get("y"),
							"name": event.get("name")
						}

					case "object_stopped_breaking":
						exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "object_stopped_breaking",
							"player_id": self.player_id,
							"x": event.get("x"),
							"y": event.get("y"),
							"name": event.get("name")
						}

					case "item_added":
						exclude_ids = self.get_exclude_ids(event.get("item").get("x"), event.get("item").get("y"), self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "item_added",
							"player_id": "Game",
							"item": event.get("item")
						}

					case "item_removed":
						exclude_ids = self.get_exclude_ids(event.get("x"), event.get("y"), self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "item_removed",
							"player_id": "Game",
							"x": event.get("x"),
							"y": event.get("y"),
							"name": event.get("name")
						}

					case "wall_added":
						exclude_ids = self.get_exclude_ids(event.get("wall").get("x"), event.get("wall").get("y"), self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "wall_added",
							"player_id": "Game",
							"wall": event.get("wall")
						}

					case "wall_removed":
						exclude_ids = self.get_exclude_ids(event.get("break_pos")[0], event.get("break_pos")[1], self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "wall_removed",
							"player_id": "Game",
							"break_pos": event.get("break_pos")
						}

					case "wall_interaction":
						exclude_ids = self.get_exclude_ids(event.get("wall_pos")[0], event.get("wall_pos")[1], self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "wall_interaction",
							"player_id": "Game",
							"wall_pos": event.get("wall_pos")
						}

					case "farmland_added":
						exclude_ids = self.get_exclude_ids(event.get("farmland_pos")[0], event.get("farmland_pos")[1], self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "farmland_added",
							"player_id": "Game",
							"farmland_pos": event.get("farmland_pos")
						}

					case "projectile_added":
						exclude_ids = [self.player_id]
						packet = {
							"type": "server_event",
							"event_type": "projectile_added",
							"player_id": "Game",
							"x": event.get("x"),
							"y": event.get("y"),
							"mouse_x": event.get("mouse_x"),
							"mouse_y": event.get("mouse_y"),
							"projectile_type": event.get("projectile_type")
						}

					case "changed_item":
						exclude_ids = self.get_exclude_ids(self.peers[self.player_id].x, self.peers[self.player_id].y, self.player_id)
						packet = {
							"type": "server_event",
							"event_type": "changed_item",
							"player_id": self.player_id,
							"changed_item": event.get("changed_item")
						}

					case "chat_message":
						packet = {
							"type": "server_event",
							"event_type": "chat_message",
							"player_id": "Game",
							"message_text": event.get("message_text")
						}

				# Хост отправляет всем, кроме себя
				if packet is None:
					self.chat_message("Ошибка отправки: неизвестный тип пакета")
				else:
					self._broadcast(packet, exclude_ids)
		else:
			packet = {
				"type": "event",
				"player_id": self.player_id,
				"events": events
			}
			
			# Клиент отправляет только хосту
			self._send_packet(packet, self.host_address)

	def disconnect(self):
		"""Отключение от сети с безопасной остановкой потоков"""
		self.running = False  # Сначала останавливаем флаг
		
		# Отправляем сообщение о выходе (если сокет еще жив)
		if self.socket:
			try:
				if self.role == "Host":
					self._broadcast({
						"type": "peer_left",
						"player_id": self.player_id
					})
				elif self.role == "Client" and self.host_address:
					self._send_packet({
						"type": "disconnect",
						"player_id": self.player_id
					}, self.host_address)
			except Exception as e:
				self.chat_message(f"Ошибка отключения: {e}")
		
		# Закрываем сокет
		if self.socket:
			try:
				self.socket.shutdown(socket.SHUT_RDWR)	# Прерываем все операции
			except:
				pass
			try:
				self.socket.close()
			except:
				pass
			self.socket = None
		
		# Ждем завершения потоков (с таймаутом)
		threads_to_join = []
		if self.receive_thread and self.receive_thread.is_alive():
			threads_to_join.append(self.receive_thread)
		
		for thread in threads_to_join:
			try:
				thread.join(timeout=1.0)  # Ждем максимум 1 секунду
			except Exception as e:
				self.chat_message(f"Ошибка завершения потоков: {e}")
		
		# Очищаем данные
		with self.lock:
			self.peers.clear()
			self.server_events.clear()
		
		self.role = "Disconnected"
		self.host_address = None
		self.chat_message("Отключено от сети")

	def _remove_peer(self, player_id: str, time_out: bool = False):
		"""Удаление пира из списка"""
		with self.lock:
			if player_id in self.peers:
				del self.peers[player_id]
				self.chat_message(f"<<< Игрок {player_id} вышел{' (тайм-аут)' if time_out else ''}")
		
		# Если мы хост, оповещаем всех
		if self.role == "Host":
			self._broadcast({
				"type": "peer_left",
				"player_id": player_id
			})

	def _heartbeat_loop(self):
		"""Проверка активности пиров (только хост)"""
		if self.role != "Host":
			return
			
		while self.running:
			time.sleep(5)  # Проверяем каждые 5 секунд
			
			current_time = time.time()
			to_remove = []
			
			# Блокировка для безопасного чтения
			with self.lock:
				for pid, peer in self.peers.items():
					if pid != self.player_id:
						if current_time - peer.last_seen > 15:
							to_remove.append(pid)
			
			# Удаляем вне блокировки, но каждый вызов _remove_peer использует свою блокировку
			for pid in to_remove:
				self._remove_peer(pid, True)

	def get_peers(self) -> List:
		"""Получение списка всех известных пиров"""
		with self.lock:
			return list(self.peers.values())

	def get_peer_by_id(self, player_id: str):
		"""Получение информации о пире по ID"""
		with self.lock:
			return self.peers.get(player_id)
	def is_host(self) -> bool:
		"""Является ли этот игрок хостом"""
		return self.role == "Host"
	
	def is_connected(self) -> bool:
		"""Подключен ли к сети"""
		return self.role != "Disconnected"

	def handle_multiplayer(self, game):

		if game.inventory.check_new_items():
			if game.inventory.whole_inventory[game.inventory.changed_slot] is None:
				game.player.changed_item = None
			else:
				game.player.changed_item = game.inventory.whole_inventory[game.inventory.changed_slot].name
			game.events.append({"event_type": "changed_item", "changed_item": game.player.changed_item})
		if game.events:
			self.send_events(tuple(game.events))
		with self.lock:
			game_events = self.server_events.get("Game", []).copy()
			self.server_events["Game"] = []

		for event in self.server_events["Game"]:
			remove_event = True

			match event["event_type"]:

				case "object_added":
					object = event["object"]
					chunk = game.world.chunk_manager.get_chunk_at(object["x"], object["y"])
					if chunk is not None:
						object["scale"] = tuple(object["scale"])
						chunk.objects.append(Object(object["name"], object["x"], object["y"], object["image_path"], object["scale"], None, object["special_flags"], object["add_path"], object["start_time"], object["is_solid"], object["rect"], object["is_solid"], object["breakable"], object["max_break"], object["breakable_by_hammer"], object["drop_items"]))
						chunk.objects[-1].__setstate__(object)

				case "object_removed":
					for object in game.world.visible_objects:
						if (object.x, object.y, object.name) == (event["x"], event["y"], event["name"]):
							destroy_object(object.image, object.x, object.y, game.world, Particle)
							game.world.chunk_manager.get_chunk_at(object.x, object.y).objects.remove(object)
							break

				case "item_added":
					item = event["item"]
					chunk = game.world.chunk_manager.get_chunk_at(item["x"], item["y"])
					if chunk is not None:
						item["scale"] = tuple(item["scale"])
						chunk.items.append(Object(item["name"], item["x"], item["y"], item["image_path"], item["scale"], None, item["special_flags"], item["add_path"], item["start_time"], item["is_solid"], item["rect"], item["is_solid"], item["breakable"], item["max_break"], item["breakable_by_hammer"], item["drop_items"]))
						chunk.items[-1].__setstate__(item)

				case "item_removed":
					for item in game.world.visible_items:
						if (item.x, item.y, item.name) == (event["x"], event["y"], event["name"]):
							game.world.chunk_manager.get_chunk_at(item.x, item.y).items.remove(item)
							break

				case "wall_added":
					wall = event["wall"]
					chunk = game.world.chunk_manager.get_chunk_at(wall["x"], wall["y"])
					if chunk is not None:
						wall_pos = (wall["x"], wall["y"])
						chunk.walls[wall_pos] = Wall(game.world, wall["wall_type"], wall["x"], wall["y"], wall["is_door"])
						chunk.walls[wall_pos].__setstate__(wall)
						for wall in (((wall_pos[0] - 256, wall_pos[1]), (wall_pos[0] + 256, wall_pos[1]), (wall_pos[0], wall_pos[1] - 256), (wall_pos[0], wall_pos[1] + 256))):
							if wall in game.world.visible_walls:
								game.world.visible_walls[wall].update_neigboors(game.world)

				case "wall_removed":
					break_pos = tuple(event["break_pos"])
					chunk = game.world.chunk_manager.get_chunk_at(*break_pos)
					if chunk is not None and break_pos in chunk.walls:
						del chunk.walls[break_pos]
						for wall in (((break_pos[0] - 256, break_pos[1]), (break_pos[0] + 256, break_pos[1]), (break_pos[0], break_pos[1] - 256), (break_pos[0], break_pos[1] + 256))):
							if wall in game.world.visible_walls:
								game.world.visible_walls[wall].update_neigboors(game.world)

				case "wall_interaction":
					wall_pos = tuple(event["wall_pos"])
					chunk = game.world.chunk_manager.get_chunk_at(*wall_pos)
					if chunk is not None and wall_pos in chunk.walls:
						chunk.walls[wall_pos].open = not chunk.walls[wall_pos].open
						chunk.walls[wall_pos].update_neigboors(game.world)

				case "farmland_added":
					farmland_pos = tuple(event["farmland_pos"])
					chunk = game.world.chunk_manager.get_chunk_at(*farmland_pos)
					if chunk is not None:
						chunk.farmlands[farmland_pos] = Farmland(*farmland_pos)
						play_sound("Dirt")

				case "projectile_added":
					game.world.projectiles.append(Projectile(event["x"], event["y"], event["mouse_x"], event["mouse_y"], event["projectile_type"]))

				case "chat_message":
					game.command_system.chat_message(event["message_text"])

				case _:
					remove_event = False

			if remove_event:
				self.server_events["Game"].remove(event)

		if game.multiplayer_role == "Host":
			for event in self.server_events["Game"]:
				match event["event_type"]:
					case "peer_joined":
						self._send_packet({"type": "server_event", "player_id": "Game", "event_type": "world_info", "world_info": (
							0, 0, False, 0, None, game.player.speed, game.player.HP, game.start_time, game.ron.x, game.ron.y, game.ron.home, game.ron.inventory, game.world.chunk_manager.generator.seed, game.time_system.current_time, game.difficulty
							)}, event["address"])
					case "get_chunk":
						chunk_key = tuple(event["chunk_key"])
						if chunk_key in game.world.chunk_manager.chunks:
							chunk = game.world.chunk_manager.chunks[chunk_key]
						else:
							chunk = game.world.chunk_manager._load_chunk_from_disk(*chunk_key)
							if chunk is None:
								game.world.chunk_manager.chunks[chunk_key] = game.world.chunk_manager.Chunk(*chunk_key)
								chunk = game.world.chunk_manager.chunks[chunk_key]
								game.world.chunk_manager.generate_chunk(chunk)
								chunk.is_loaded = True
						state = chunk.__getstate__()
						state["mobs"] = []
						state["particles"] = []
						state["caves"] = []

						new_objects = [object.__getstate__() for object in state["objects"]]
						state["objects"] = new_objects
						new_items = [item.__getstate__() for item in state["items"]]
						state["items"] = new_items
						new_walls = [wall.__getstate__() for _, wall in state["walls"].items()]
						state["walls"] = new_walls
						new_farmlands = [farmland.__getstate__() for _, farmland in state["farmlands"].items()]
						state["farmlands"] = new_farmlands
						if event["player_id"] in self.peers:
							self._send_packet({"type": "server_event", "event_type": "chunk", "player_id": "Game", "chunk_key": chunk_key, "chunk_state": state}, self.peers[event["player_id"]].address)

				self.server_events["Game"].remove(event)
		else:
			if time.time() - self.last_heartbeat > 3:
				self.send_heartbeat()
			for event in self.server_events["Game"]:
				match event["event_type"]:
					case "world_info":
						game.player.x, game.player.y, game.Backrooms.InBackrooms, game.Backrooms.Level, game.world.current_cave, game.player.speed, game.player.HP, game.start_time, game.ron.x, game.ron.y, game.ron.home, game.ron.inventory, game.world.chunk_manager.generator.seed, game.time_system.current_time, game.difficulty = event["world_info"]
						game.world.chunk_manager.update_seed()

					case "ron_moved":
						game.ron.x = event["x"]
						game.ron.y = event["y"]
						game.ron.direction = event["direction"]

					case "chunk":
						chunk_key = tuple(event["chunk_key"])
						game.world.chunk_manager.chunks[chunk_key] = game.world.chunk_manager.Chunk(*chunk_key)
						chunk = game.world.chunk_manager.chunks[chunk_key]
						chunk.__setstate__(event["chunk_state"])
						chunk.is_loaded = True

						new_objects = []
						for object in chunk.objects:
							object["scale"] = tuple(object["scale"])
							new_objects.append(Object(object["name"], object["x"], object["y"], object["image_path"], object["scale"], None, object["special_flags"], object["add_path"], object["start_time"], object["is_solid"], object["rect"], object["is_solid"], object["breakable"], object["max_break"], object["breakable_by_hammer"], object["drop_items"]))
							new_objects[-1].__setstate__(object)
						chunk.objects = new_objects
						
						new_items = []
						for item in chunk.items:
							item["scale"] = tuple(item["scale"])
							new_items = [Object(item["name"], item["x"], item["y"], item["image_path"], item["scale"], None, item["special_flags"], item["add_path"], item["start_time"], item["is_solid"], item["rect"], item["is_solid"], item["breakable"], item["max_break"], item["breakable_by_hammer"], item["drop_items"]) for item in chunk.items]
							new_items[-1].__setstate__(item)
						chunk.items = new_items
						
						new_walls = {}
						for wall in chunk.walls:
							new_walls[(wall["x"], wall["y"])] = Wall(game.world, wall["wall_type"], wall["x"], wall["y"])
							new_walls[(wall["x"], wall["y"])].__setstate__(wall)
						chunk.walls = new_walls

						new_farmlands = {}
						for farmland in chunk.farmlands:
							new_farmlands[(farmland["x"], farmland["y"])] = Farmland(farmland["x"], farmland["y"])
							new_farmlands[(farmland["x"], farmland["y"])].__setstate__(farmland)
						chunk.farmlands = new_farmlands
						game.world.chunk_manager.chunks_to_get.remove(chunk_key)

				self.server_events["Game"].remove(event)

