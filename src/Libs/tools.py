import json

class DebugLEDHandler():
    def __init__(self) -> None:
        with open("Flightcontroller-\src\settings\debug_led.json") as data:
            self.settings = json.load(data.read())
        self.dataLed = self.settings["debugLEDStrip"]["dataLED"]
        self.healthLed = self.settings["debugLEDStrip"]["healthLED"]
        self.progLed = self.settings["debugLEDStrip"]["progLed"]


    def progLed