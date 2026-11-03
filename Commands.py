import re
from typing import List, Tuple

class CommandSystem:

	def __init__(self, player, multiplayer, game_events, net, chat, main_chat, FPS, inventory, time_system, chat_tick):
		self.player = player
		self.multiplayer = multiplayer
		self.game_events = game_events
		self.net = net
		self.chat = chat
		self.main_chat = main_chat
		self.FPS = FPS
		self.inventory = inventory
		self.time_system = time_system
		self.chat_tick = chat_tick
		self.init_commands()
	
	def parse_command(self, command_text: str) -> Tuple[str, List[str]]:
		"""
		Разобрать строку команды на имя и аргументы
		Поддерживает кавычки для аргументов с пробелами
		"""
		# Разбиваем с учётом кавычек
		args = re.findall(r'(?:[^\s"]+|"[^"]*")+', command_text.strip())
		if not args:
			return "", []
		
		command_name = args[0].lower()
		# Убираем кавычки у аргументов
		parsed_args = []
		for arg in args[1:]:
			if arg.startswith('"') and arg.endswith('"'): 
				parsed_args.append(arg[1:-1])
			else:
				# Пробуем преобразовать в число
				try:
					if "." in arg:
						parsed_args.append(float(arg))
					else:
						parsed_args.append(int(arg))
				except ValueError:
					parsed_args.append(arg)
		
		return command_name, parsed_args
	
	def execute(self, command_text: str) -> str:
		"""Выполнить команду и вернуть результат/сообщение"""
		if not command_text.startswith("/"):
			return "Команда должна начинаться с /"
		
		command_text = command_text[1:]  # Убираем /
		cmd_name, args = self.parse_command(command_text)
		
		if cmd_name not in self.commands:
			return f"Нет такой команды: {cmd_name}. Используйте /help"
		
		try:
			result = self.commands[cmd_name][0](*args)
			return result if result is not None else "Команда выполнена"
		except TypeError as e:
			return f"Ошибка в аргументах команды {cmd_name}: {e}"
		except Exception as e:
			return f"Ошибка выполнения команды {cmd_name}: {e}"

	# Далее идтт игровые команды, которые можно ввести в чате

	def tp(self, x, y, player=None):
		"""Телепортация игрока на указанные координаты"""
		if player is None:
			player = self.player
		player.x = x
		player.y = y
		if self.multiplayer:
			self.game_events.append({"event_type": "player_tp", "x": player.x, "y": player.y, "direction": player.direction})
			self.net.peers[self.net.player_id].x = player.x
			self.net.peers[self.net.player_id].y = player.y
			self.net.peers[self.net.player_id].direction = player.direction

	def chat_message(self, message: str, send_to_peers: bool = False):
		"""Отправляет сообщение в чат"""
		self.chat.append(message)
		self.main_chat.append(message)
		self.chat_tick = len(message) // 1.5 * self.FPS #TODO заменить FPS на dt
		if self.multiplayer and send_to_peers:
			self.game_events.append({"event_type": "chat_message", "message_text": message})

	def command_help(self, command: str=""):
		if command == "":
			self.chat_message("Команды можно использовать, если у вас включён режим бога или вы взломали код вселенной. Для ознакомления со списком команд введите /command_list")
		elif command in self.commands:
			self.chat_message(self.commands[command][1])
		else:
			self.chat_message("Нет такой команды: " + command)

	def command_list(self):
		for command in self.commands.keys():
			self.chat_message(command)

	def kukusiki_hack(self):
		hack_list = ("рожи дыбильные", "лысый кал", "хитрожопые скоты", "спина и дождь", "маслодонное кино", "помидорный чай", "пьяный хлеб", "флюрография гуся")
		self.chat_message("Смори, Ришный Мцэць взломал код вселенной и скинул нам этот шифрованный список:")
		for i in hack_list:
			self.chat_message(i)
	
	def init_commands(self):

		self.commands = {

				"help": (self.command_help, "Выдаёт справку\n/help КОМАНДА"),
				"command_list": (self.command_list, "Выдаёт список команд\n/command_list"),
				"kukusiki_hack": (self.kukusiki_hack, "Раскрывает код вселенной\n/kukusiki_hack"),
				"tp": (self.tp, "Телепортация игрока на указанные координаты\n tp X Y"),
				"give": (self.inventory.increate, "Выдача предмета в инвентарь\n give ПРЕДМЕТ КОЛИЧЕСТВО=1"),
				"get_brightness": (self.time_system.get_brightness, "Получение текущей яркости днейвного цикла\n/get_brightness"),
				"get_time_of_day": (self.time_system.get_time_of_day, "Получение текущего времени в 24-часовом формате\n/get_time_of_day"),
				"set_time_speed": (self.time_system.set_time_speed, "Изменить скорость времени\n/time_scale МНОЖИТЕЛЬ"),
				"reset_to_day": (self.time_system.reset_to_day, "Обнулить время до дня\n/reset_to_day"),
				"skip_time": (self.time_system.skip_time, "Перемотать время вперёд\n/skip_time СЕКУНДЫ"),
				"chat_message": (self.chat_message, "Вывести сообщение в чат\n/chat_message ТЕКСТ")

				}

