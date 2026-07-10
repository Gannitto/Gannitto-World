import json
import os
from Globals import path

class Translator:
	def __init__(self, lang="ru"):
		self.lang = lang
		self.load_language(lang)
	
	def load_language(self, lang):
		lang_path = path + f"Locales/{lang}.json"
		if os.path.exists(lang_path):
			with open(lang_path, "r", encoding="utf-8") as f:
				self.translations = json.load(f)
		else:
			self.translations = {}
	
	def get(self, key, default=None):
		return self.translations.get(key, default or key)

translator = Translator()
