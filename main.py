import src.Libs.autoupdate as ap
from sys import platform
import os

try:
    if platform == "linux":
        ap.update(os.path.dirname(os.path.abspath(__file__)))
except:
    pass


#last test i hope
    

