import os
import sys
import json
import shutil
import zipfile
import tempfile
import subprocess
import urllib.request
import urllib.error
from Globals import path

REPO_OWNER = "Gannitto"
REPO_NAME = "Gannitto-World"
BRANCH = "master"

# Файлы и папки, которые НИКОГДА не перезаписываются и не удаляются при обновлении
PROTECTED_PATHS = {"Saves", ".git", "__pycache__"}

class Updater:
	def __init__(self, channel: str = "dev"):
		"""
		channel:
		  - "stable": скачивает последний официальный релиз (Releases)
		  - "dev": скачивает последний коммит из ветки master
		"""
		self.channel = channel
		self.version_file = os.path.join(path, "version.json")
		self.local_info = self._load_local_info()

	def _load_local_info(self) -> dict:
		if os.path.exists(self.version_file):
			try:
				with open(self.version_file, "r", encoding="utf-8") as f:
					return json.load(f)
			except Exception:
				pass
		return {"channel": self.channel, "version": None, "commit_sha": None}

	def _save_local_info(self, data: dict):
		with open(self.version_file, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=4, ensure_ascii=False)

	def _api_request(self, endpoint: str) -> dict | None:
		url = f"https://github.com{REPO_OWNER}/{REPO_NAME}/{endpoint}"
		req = urllib.request.Request(
			url,
			headers={"User-Agent": "Gannitto-World-Updater"}
		)
		try:
			with urllib.request.urlopen(req, timeout=5) as response:
				return json.loads(response.read().decode("utf-8"))
		except urllib.error.HTTPError as e:
			# 404 возникает, если релизов еще нет
			if e.code == 404:
				return None
			print(f"[Updater] HTTP ошибка: {e.code}")
			return None
		except Exception as e:
			print(f"[Updater] Нет соединения или ошибка сети: {e}")
			return None

	def check_for_updates(self) -> dict | None:
		"""
		Проверяет наличие обновлений.
		Возвращает словарь с данными для скачивания или None, если обновление не требуется.
		"""
		if self.channel == "stable":
			release = self._api_request("releases/latest")
			# Если релизов еще нет (404), мягко откатываемся на проверку ветки master
			if not release:
				print("[Updater] Релизы не найдены, проверка ветки master...")
				return self._check_dev_update()

			latest_tag = release.get("tag_name")
			if latest_tag and latest_tag != self.local_info.get("version"):
				# Ищем прикрепленный zip-архив билда (если игра скомпилирована в exe), иначе берем исходники релиза
				download_url = release.get("zipball_url")
				is_compiled = getattr(sys, "frozen", False)

				if is_compiled:
					for asset in release.get("assets", []):
						if asset["name"].endswith(".zip"):
							download_url = asset["browser_download_url"]
							break

				return {
					"type": "stable",
					"id": latest_tag,
					"url": download_url
				}

		elif self.channel == "dev":
			return self._check_dev_update()

		return None

	def _check_dev_update(self) -> dict | None:
		branch_data = self._api_request(f"branches/{BRANCH}")
		if not branch_data:
			return None

		latest_sha = branch_data["commit"]["sha"]
		if latest_sha != self.local_info.get("commit_sha"):
			return {
				"type": "dev",
				"id": latest_sha,
				"url": f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/heads/{BRANCH}.zip"
			}
		return None

	def install_update(self, update_data: dict) -> bool:
		"""Скачивает и устанавливает обновление, сохраняя папку Saves."""
		temp_dir = tempfile.mkdtemp(prefix="gannitto_update_")
		zip_path = os.path.join(temp_dir, "update.zip")

		try:
			print(f"[Updater] Скачивание обновления ({update_data['id']})...")
			req = urllib.request.Request(
				update_data["url"],
				headers={"User-Agent": "Gannitto-World-Updater"}
			)
			with urllib.request.urlopen(req, timeout=30) as response, open(zip_path, "wb") as out_file:
				shutil.copyfileobj(response, out_file)

			extract_dir = os.path.join(temp_dir, "extracted")
			with zipfile.ZipFile(zip_path, "r") as zip_ref:
				zip_ref.extractall(extract_dir)

			# GitHub архивирует проект внутри корневой папки (например, Gannitto-World-master)
			extracted_items = os.listdir(extract_dir)
			source_root = extract_dir
			if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_dir, extracted_items[0])):
				source_root = os.path.join(extract_dir, extracted_items[0])

			self._replace_game_files(source_root, path)

			# Обновляем локальный маркер версии
			new_info = {
				"channel": update_data["type"],
				"version": update_data["id"] if update_data["type"] == "stable" else self.local_info.get("version"),
				"commit_sha": update_data["id"] if update_data["type"] == "dev" else None
			}
			self._save_local_info(new_info)
			print("[Updater] Обновление успешно установлено!")
			return True

		except Exception as e:
			print(f"[Updater] Ошибка при установке обновления: {e}")
			return False
		finally:
			shutil.rmtree(temp_dir, ignore_errors=True)

	def _replace_game_files(self, src_dir: str, dst_dir: str):
		"""Копирует новые файлы поверх старых и удаляет устаревшие, не трогая PROTECTED_PATHS."""
		# 1. Удаляем старые файлы, которых больше нет в репозитории (кроме защищенных)
		for item in os.listdir(dst_dir):
			if item in PROTECTED_PATHS:
				continue
			dst_item = os.path.join(dst_dir, item)
			src_item = os.path.join(src_dir, item)

			if not os.path.exists(src_item):
				if os.path.isdir(dst_item):
					shutil.rmtree(dst_item)
				else:
					os.remove(dst_item)

		# 2. Копируем новые и обновленные файлы
		for item in os.listdir(src_dir):
			if item in PROTECTED_PATHS:
				continue
			src_item = os.path.join(src_dir, item)
			dst_item = os.path.join(dst_dir, item)

			if os.path.isdir(src_item):
				if os.path.exists(dst_item):
					shutil.rmtree(dst_item)
				shutil.copytree(src_item, dst_item)
			else:
				shutil.copy2(src_item, dst_item)

	@staticmethod
	def restart_game():
		"""Перезапускает игру после обновления."""
		python = sys.executable
		os.execl(python, python, *sys.argv)

