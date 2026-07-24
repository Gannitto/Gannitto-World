import re
from typing import List, Callable, Tuple, Any

class CommandSystem:

	def __init__(self):
		self.commands = {}
	
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

command_system = CommandSystem()
