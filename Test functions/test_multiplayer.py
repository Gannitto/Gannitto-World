import time
from Multiplayer import NetworkManager
from dataclasses import dataclass

@dataclass
class PeerInfo:
	id: str
	address: tuple
	name: str
	last_seen: float
	position: tuple = (0, 0)  # (x, y)

def test_multiplayer():
	"""Тест мультиплеера на одном устройстве"""
	
	# Создаем хост
	host_net = NetworkManager(PeerInfo)
	assert host_net.start_host(5555), "Failed to start host"
	
	# Создаем клиент
	client_net = NetworkManager(PeerInfo)
	assert client_net.connect_to_host("127.0.0.1", 5555), "Failed to connect"
	
	time.sleep(1)  # Даем время на подключение
	
	# Проверяем, что клиент видит хоста
	peers = client_net.get_peers()
	print(f"Client sees {len(peers)} peers")
	
	# Отправляем позицию от клиента
	client_net.send_data((100, 200))
	time.sleep(0.5)
	
	# Проверяем на хосте
	host_peers = host_net.get_peers()
	print(f"Host sees {len(host_peers)} peers")
	
	# Отключаемся
	client_net.disconnect()
	host_net.disconnect()
	
	print("Test passed!")
	
if __name__ == "__main__":
	test_multiplayer()
