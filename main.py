import src.Libs.autoupdate as ap
from sys import platform
import os

try:
    if platform == "linux":
        ap.update(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    raise e


#I don't know
    

