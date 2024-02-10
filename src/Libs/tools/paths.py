import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.parent
CONTROLLER_SETTINGS_PATH = ROOT_DIR+"src/settings/controller.json"
DATA_SETTINGS_PATH = ROOT_DIR+"src/settings/data.json"
DEBUG_LED_PATH = ROOT_DIR+"src/settings/debug.json"
MOTORS_SETTINGS_PATH = ROOT_DIR+"src/settings/motors.json"
TRANSMITT_SETTINGS_PATH = ROOT_DIR+"src/settings/transmitt.json"
VIDEO_SETTINGS_PATH = ROOT_DIR+"src/settings/video.json"
SETTINGS_PATH = ROOT_DIR+"src/settings"
print(ROOT_DIR)