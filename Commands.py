import re
from typing import List, Tuple
from Translator import t

class CommandSystem:

	def __init__(self, game):

		self.game = game
		self.player = game.player
		self.init_commands()
	
	def parse_command(self, command_text: str) -> Tuple[str, List[str]]:

		"""
		Разобрать строку команды на имя и аргументы.
		Поддерживает кавычки для аргументов с пробелами
		и экранирование через \\ (как в терминале).
		"""
		text = command_text.strip()
		if not text:
			return "", []

		args: List[str] = []
		current: List[str] = []
		in_quotes = False
		has_content = False  # был ли хоть один символ в текущем аргументе
		i = 0
		n = len(text)

		while i < n:
			ch = text[i]

			if ch == '\\' and i + 1 < n:
				# Экранирование: следующий символ — обычный символ
				current.append(text[i + 1])
				has_content = True
				i += 2
				continue

			if in_quotes:
				if ch == '"':
					in_quotes = False
					# Закрывающая кавычка завершает "кавычковую" часть,
					# но аргумент может продолжаться (например: "a b"c)
					has_content = True
				else:
					current.append(ch)
				i += 1
				continue

			if ch == '"':
				in_quotes = True
				has_content = True	# пустые кавычки "" тоже дают аргумент
				i += 1
				continue

			if ch.isspace():
				if has_content:
					args.append(''.join(current))
					current = []
					has_content = False
				i += 1
				continue

			current.append(ch)
			has_content = True
			i += 1

		if has_content:
			args.append(''.join(current))

		if not args:
			return "", []

		command_name = args[0].lower()
		return command_name, args[1:]

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
			return result if result is not None else t("The command has been executed.")
		except TypeError as e:
			return f"Ошибка в аргументах команды {cmd_name}: {e}"
		except SyntaxError as e:
			return f"Ошибка в синтаксисе команды {cmd_name}: {e}"
		except Exception as e:
			return f"Ошибка выполнения команды {cmd_name}: {e}"

	# Далее идтт игровые команды, которые можно ввести в чате

	def tp(self, x, y, player=None):
		"""Телепортация игрока на указанные координаты"""
		if player is None:
			player = self.player
		player.x = int(x)
		player.y = int(y)
		player.update_rect()
		if self.game.multiplayer:
			self.game.events.append({"event_type": "player_tp", "x": player.x, "y": player.y, "direction": player.direction})
			self.game.net.peers[self.game.net.player_id].x = player.x
			self.game.net.peers[self.game.net.player_id].y = player.y
			self.game.net.peers[self.game.net.player_id].direction = player.direction

	def chat_message(self, message: str, send_to_peers: bool = False):
		"""Отправляет сообщение в чат"""
		self.game.chat.append(message)
		self.game.main_chat.append(message)
		self.game.chat_tick = 10
		if self.game.multiplayer and bool(send_to_peers):
			self.game.events.append({"event_type": "chat_message", "message_text": message})

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
				"give": (self.game.inventory.increate, "Выдача предмета в инвентарь\n give ПРЕДМЕТ КОЛИЧЕСТВО=1"),
				"get_brightness": (self.game.time_system.get_brightness, "Получение текущей яркости днейвного цикла\n/get_brightness"),
				"get_time_of_day": (self.game.time_system.get_time_of_day, "Получение текущего времени в 24-часовом формате\n/get_time_of_day"),
				"set_time_speed": (self.game.time_system.set_time_speed, "Изменить скорость времени\n/time_scale МНОЖИТЕЛЬ"),
				"reset_to_day": (self.game.time_system.reset_to_day, "Обнулить время до дня\n/reset_to_day"),
				"skip_time": (self.game.time_system.skip_time, "Перемотать время вперёд\n/skip_time СЕКУНДЫ"),
				"chat_message": (self.chat_message, "Вывести сообщение в чат\n/chat_message ТЕКСТ")

				}

