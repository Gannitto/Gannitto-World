cd ~/Projects/
cp -r Gannitto\ world/files Gannitto_world_build
cd Gannitto_world_build
sed -i "1i import\ sys\nimport\ types\nimport\ importlib.metadata\nif\ \"pkg_resources\"\ not\ in\ sys.modules:\n    pkg_res\ =\ types.ModuleType(\"pkg_resources\")\n    pkg_res.get_distribution\ =\ lambda\ name:\ types.SimpleNamespace(\n        version=importlib.metadata.version(name)\n    )\n    sys.modules[\"pkg_resources\"]\ =\ pkg_res" Gannitto_world.py
rm -rf doc/ __pycache__/ README.md README.ru.md Saves/ Test\ functions/ .git/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pyinstaller setuptools
pyinstaller --clean --noconfirm --onedir --windowed \
  --name "GannittoWorld" \
  --add-data "Images:Images" \
  --add-data "Locales:Locales" \
  --add-data "Sounds:Sounds" \
  --add-data "Soundtracks:Soundtracks" \
  --add-data "Font.ttf:." \
  --add-data "Items.json:." \
  --hidden-import=pkg_resources \
  --copy-metadata vnoise \
  --collect-all upnpclient \
  --collect-all vnoise \
  Gannitto_world.py
cd dist/GannittoWorld
mkdir _internal/Saves _internal/Saves/Cache _internal/Saves/Mods _internal/Saves/Settings _internal/Saves/Worlds

