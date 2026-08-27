import socket
import threading
import json
import time
import hashlib
from typing import Dict, List, Optional

# Версия протокола для совместимости
PROTOCOL_VERSION = 1

class NetworkManager:
	"""Основной класс для управления сетевым взаимодействием"""
	
	def __init__(self, PeerInfo, chat_message):
		self.role = "Disconnected"
		self.socket: Optional[socket.socket] = None
		self.running = False
		self.peers = {}  # id -> PeerInfo
		self.player_id = self._generate_id()
		self.encryption_key = b"gannitto_world_secret_key_123456"  # Простой ключ шифрования (временно)
		self.PeerInfo = PeerInfo
		self.chat_message = chat_message
		self.last_heartbeat = time.time()
		self.server_events = {"Game": []}
		
		# Коллбэки для событий
		self.callbacks = {
			"on_peer_joined": None,
			"on_peer_left": None,
			"on_peer_moved": None,
			"on_game_state": None
		}
		
		# Потоки
		self.receive_thread: Optional[threading.Thread] = None
		self.send_queue: List[Dict] = []
		self.lock = threading.Lock()
		
		# Информация о хосте для подключения
		self.host_address = None
		
	def _generate_id(self) -> str:
		"""Генерирует уникальный ID для игрока"""
		import uuid
		return str(uuid.uuid4())[:8]
	
	def _encrypt_data(self, data: bytes) -> bytes:
		"""Простое XOR шифрование для защиты от случайного перехвата"""
		key = self.encryption_key
		return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
	
	def _decrypt_data(self, data: bytes) -> bytes:
		"""Расшифровка данных"""
		return self._encrypt_data(data)  # XOR симметричен
	
	def start_host(self, port: int = 5555) -> bool:
		"""Запуск как хоста (сервера)"""
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	# UDP протокол
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind(("0.0.0.0", port))
			self.socket.settimeout(1.0)  # Таймаут для проверки соединения
			self.role = "Host"
			self.running = True
			
			# Добавляем себя как первого пира
			self.peers[self.player_id] = self.PeerInfo(
				id=self.player_id,
				address=("127.0.0.1", port),
				name=f"Host_{self.player_id[:4]}",
				last_seen=time.time()
			)
			
			# Запускаем поток получения
			self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
			self.receive_thread.start()
			
			# Запускаем поток проверки соединений
			threading.Thread(target=self._heartbeat_loop, daemon=True).start()
			
			print(f"[Network] Host started on port {port}")
			print(f"[Network] Your player ID: {self.player_id}")
			return True
			
		except Exception as e:
			self.chat_message(f"Не удалось запустить хост: {e}")
			return False
	
	def connect_to_host(self, host_ip: str, port: int = 5555) -> bool:
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
		print(packet)
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
						peer = self.PeerInfo(
							id=player_id,
							address=addr,
							name=packet.get("name", f"Player_{player_id[:4]}"),
							last_seen=time.time(),
							position=packet.get("position", (0, 0))
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
						"position": peer.position
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
							self._broadcast({
								"type": "server_event",
								"event_type": "player_moved",
								"player_id": player_id,
								"x": event.get("x"),
								"y": event.get("y"),
								"direction": event.get("direction")
							}, player_id)

						case "object_removed":
							event["player_id"] = "Game"
							self.server_events[player_id].append(event)
							self._broadcast({
								"type": "server_event",
								"event_type": "object_removed",
								"player_id": "Game",
								"x": event.get("x"),
								"y": event.get("y"),
								"name": event.get("name")
							}, player_id)

						case "object_added":
							event["player_id"] = "Game"
							self.server_events[player_id].append(event)
							self._broadcast({
								"type": "server_event",
								"event_type": "object_added",
								"player_id": "Game",
								"object": event.get("object")
							}, player_id)
					
	def _handle_packet_as_client(self, packet: Dict, addr: tuple):
		"""Обработка пакетов на стороне клиента"""
		print(packet)
		packet_type = packet.get("type")
		match packet_type:
			case "peer_list":
				# Получение списка всех игроков от хоста
				peers_data = packet.get("peers", {})
				for pid, pdata in peers_data.items():
					if pid != self.player_id:  # Не добавляем себя
						self.peers[pid] = self.PeerInfo(
							id=pid,
							address=addr,
							name=pdata.get("name", f"Player_{pid[:4]}"),
							last_seen=time.time(),
							position=tuple(pdata.get("position", (0, 0)))
						)
				print(f"[Network] Received peer list: {len(self.peers)} peers")
				
				# Вызываем коллбэк
				if self.callbacks["on_game_state"]:
					self.callbacks["on_game_state"]()
					
			case "peer_joined":
				# Новый игрок присоединился
				pdata = packet.get("peer", {})
				pid = pdata.get("id")
				if pid and pid != self.player_id:
					peer = self.PeerInfo(
						id=pid,
						address=addr,
						name=pdata.get("name", f"Player_{pid[:4]}"),
						last_seen=time.time(),
						position=tuple(pdata.get("position", (0, 0)))
					)
					self.peers[pid] = peer
					self.server_events[pid] = []
					
					if self.callbacks["on_peer_joined"]:
						self.callbacks["on_peer_joined"](peer)
						
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
				"position": peer.position
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
						packet = {
							"type": "server_event",
							"event_type": "player_moved",
							"player_id": self.player_id,
							"x": event.get("x"),
							"y": event.get("y"),
							"direction": event.get("direction")
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

					case "object_removed":
						packet = {
							"type": "server_event",
							"event_type": "object_removed",
							"player_id": "Game",
							"x": event.get("x"),
							"y": event.get("y"),
							"name": event.get("name")
						}

					case "object_added":
						packet = {
							"type": "server_event",
							"event_type": "object_added",
							"player_id": "Game",
							"object": event.get("object")
						}
				# Хост отправляет всем, кроме себя
				if packet is None:
					self.chat_message("Ошибка отправки: неизвестный тип пакета")
				else:
					self._broadcast_except(packet, self.player_id)
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
				print(f"[Network] Error sending disconnect: {e}")
		
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
				print(f"[Network] Error joining thread: {e}")
		
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
		
		# Вызываем коллбэк вне блокировки
		if self.callbacks["on_peer_left"]:
			self.callbacks["on_peer_left"](player_id)
			
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
