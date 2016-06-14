import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","bs4","urllib.request","requests","lxml"], "excludes": ["tkinter"], "include_files":["style.css"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
##if sys.platform == "win32":
##    base = "Win32GUI"

setup(  name = "Pretty Parser",
        version = "1.0",
        description = "Bare-minimum RSS Feed Aggregator",
        options = {"build_exe": build_exe_options},
        executables = [Executable("PrettyParser.py", base=base)])
