import os
import sys

def parse_path(name):
    if os.name == "nt":
        relative_path = "assets\\" + name
    else:
        relative_path = "assets/" + name
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)