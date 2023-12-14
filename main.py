import src.Libs.autoupdate as ap
from sys import platform
import os

if platform == "linux":
    ap.update(os.path.dirname(os.path.abspath(__file__)))


    

