import socket
import threading
import json
import time
import hashlib
from typing import Dict, List, Optional

# Версия протокола для совместимости
PROTOCOL_VERSION = 1

# @dataclass
# class PeerInfo:
# 	id: str
# 	address: tuple
# 	name: str
# 	last_seen: float
# 	position: tuple = (0, 0)  # (x, y)

class NetworkManager:
	"""Основной класс для управления сетевым взаимодействием"""
	
	def __init__(self, PeerInfo):
		self.role = "Disconnected"
		self.socket: Optional[socket.socket] = None
		self.running = False
		self.peers = {}  # id -> PeerInfo
		self.player_id = self._generate_id()
		self.encryption_key = b"gannitto_world_secret_key_123456"  # Простой ключ шифрования (временно)
		self.PeerInfo = PeerInfo
		
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
			print(f"[Network] Failed to start host: {e}")
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
			
			print(f"[Network] Connected to host at {host_ip}:{port}")
			return True
			
		except Exception as e:
			print(f"[Network] Failed to connect to host: {e}")
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
					print(f"[Network] Receive error: {e}")
					break
	
	def _handle_packet_as_host(self, packet: Dict, addr: tuple):
		"""Обработка пакетов на стороне хоста"""
		packet_type = packet.get("type")
		player_id = packet.get("player_id")
		
		if packet_type == "handshake":
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
					print(f"[Network] New peer joined: {player_id} from {addr}")
			
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
			
			# Вызываем коллбэк
			if self.callbacks["on_peer_joined"]:
				self.callbacks["on_peer_joined"](peer)
				
		elif packet_type == "move":
			# Обновление позиции игрока
			with self.lock:
				if player_id in self.peers:
					self.peers[player_id].position = tuple(packet.get("position", (0, 0)))
					self.peers[player_id].last_seen = time.time()
					position = self.peers[player_id].position
			
			# Пересылаем движение всем остальным (вне блокировки)
			self._broadcast({
				"type": "peer_moved",
				"player_id": player_id,
				"position": position
			}, player_id)
			
			if self.callbacks["on_peer_moved"]:
				self.callbacks["on_peer_moved"](player_id, position)
				
		elif packet_type == "disconnect":
			# Игрок отключается
			self._remove_peer(player_id)

	def _handle_packet_as_client(self, packet: Dict, addr: tuple):
		"""Обработка пакетов на стороне клиента"""
		packet_type = packet.get("type")
		
		if packet_type == "peer_list":
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
				
		elif packet_type == "peer_joined":
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
				
				if self.callbacks["on_peer_joined"]:
					self.callbacks["on_peer_joined"](peer)
					
		elif packet_type == "peer_moved":
			# Кто-то двинулся
			pid = packet.get("player_id")
			pos = tuple(packet.get("position", (0, 0)))
			if pid and pid != self.player_id and pid in self.peers:
				self.peers[pid].position = pos
				self.peers[pid].last_seen = time.time()
				
				if self.callbacks["on_peer_moved"]:
					self.callbacks["on_peer_moved"](pid, pos)
					
		elif packet_type == "peer_left":
			# Кто-то отключился
			pid = packet.get("player_id")
			self._remove_peer(pid)
	
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
			print(f"[Network] Send error: {e}")
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
	
	def send_data(self, events: tuple):
		"""Отправка данных всем остальным"""
		packet = {
			"player_id": self.player_id,
			"events": events
		}
		
		if self.role == "Host":
			# Хост отправляет всем, кроме себя
			self._broadcast_except(packet, self.player_id)
		elif self.role == "Client" and self.host_address:
			# Клиент отправляет только хосту
			self._send_packet(packet, self.host_address)
	
	def disconnect(self):
		"""Отключение от сети"""
		self.running = False
		
		# Отправляем сообщение о выходе
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
			
		if self.socket:
			try:
				self.socket.close()
			except:
				pass
			self.socket = None
			
		# Очищаем список пиров с блокировкой
		with self.lock:
			self.peers.clear()
			
		self.role = "Disconnected"
		print("[Network] Disconnected from network")

	def _remove_peer(self, player_id: str):
		"""Удаление пира из списка"""
		with self.lock:
			if player_id in self.peers:
				del self.peers[player_id]
				print(f"[Network] Peer left: {player_id}")
		
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
			
			# Используем блокировку для безопасного чтения
			with self.lock:
				for pid, peer in self.peers.items():
					if pid != self.player_id:
						if current_time - peer.last_seen > 15:
							to_remove.append(pid)
			
			# Удаляем вне блокировки, но каждый вызов _remove_peer использует свою блокировку
			for pid in to_remove:
				self._remove_peer(pid)

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
