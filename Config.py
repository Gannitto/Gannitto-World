import Saver
from Globals import default_settings, default_hot_keys, path

try:
	Settings = Saver.load_objects(path + "Saves/Settings/Settings.save")
except FileNotFoundError:
	Settings = default_settings
	Saver.save_objects(path + "Saves/Settings/Settings.save", Settings)

try:
	hot_keys = Saver.load_objects(path + "Saves/Settings/Hot keys.save")
except FileNotFoundError:
	hot_keys = default_hot_keys
	Saver.save_objects(path + "Saves/Settings/Hot keys.save", hot_keys)

try:
	statistics = Saver.load_objects(path + "Saves/Settings/Statistics.save")
except FileNotFoundError:
	statistics = [0, 0, 0]

