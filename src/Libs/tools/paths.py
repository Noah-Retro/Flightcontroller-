import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
CONTROLLER_SETTINGS_PATH = os.path.abspath("src/settings/controller.json")
DATA_SETTINGS_PATH = os.path.abspath("src/settings/data.json")
DEBUG_LED_PATH = os.path.abspath("src/settings/debug.json")
MOTORS_SETTINGS_PATH = os.path.abspath("src/settings/motors.json")
TRANSMITT_SETTINGS_PATH = os.path.abspath("src/settings/transmitt.json")
VIDEO_SETTINGS_PATH = os.path.abspath("src/settings/video.json")
SETTINGS_PATH = os.path.abspath("src/settings")
print(ROOT_DIR)