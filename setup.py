import sys
from cx_Freeze import setup, Executable

includefiles=['img/','sounds/','imp.txt']

setup(
    name = "Galactica",
    version = "1.0",
    description = "Simple Space Shooter Game Developed By Anuran Barman",
    options = {'build_exe': {'include_files':includefiles}},
    executables = [Executable("Galactica.py")])

# setup(
#     name = "Galactica",
#     version = "1.0",
#     description = "Simple Space Shooter Game Developed By Anuran Barman",
#     options = {'build_exe': {'include_files':includefiles}},
#     executables = [Executable("Galactica.py"),base="Win32GUI"])



