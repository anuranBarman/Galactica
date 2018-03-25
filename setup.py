import sys
from cx_Freeze import setup, Executable

includefiles=['img/']

setup(
    name = "Galactica",
    version = "1.0",
    description = "Simple Space Shooter Game Developed By Anuran Barman",
    options = {'build_exe': {'include_files':includefiles}},
    executables = [Executable("shmup.py")])



# import sys
# from cx_Freeze import setup, Executable

# build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files":["C:\Documents and Settings\boot_1.bmp", "C:\Documents and Settings\boot_2.bmp", 'C:\Documents and Settings\boot_3.bmp', 'C:\Documents and Settings\boot_4.bmp', 'C:\Documents and Settings\fish1.bmp', 'C:\Documents and Settings\fish2.bmp', 'C:\Documents and Settings\fish3.bmp', 'C:\Documents and Settings\fish4.bmp', 'C:\Documents and Settings\goldenfish_1.bmp', 'C:\Documents and Settings\goldenfish_2.bmp']}

# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# exe=Executable(
#      script="game.py",
#      base=base
#      )

# setup(  name = "Game name",
#         version = "1.0",
#         description = "My GUI application!",
#         options = {"build_exe": build_exe_options},
#         executables = [exe])

