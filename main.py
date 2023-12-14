import src.Libs.autoupdate as ap
from sys import platform
import os

try:
    if platform == "linux":
        ap.update(os.path.dirname(os.path.abspath(__file__)))
except:
    raise SystemError


#last test i hope it wasn't
    

