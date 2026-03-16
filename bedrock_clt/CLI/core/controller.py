import sys

import os
import sys
import questionary
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

#from visualt.prints import print_error, printt


def controller_Servers(accion):
    if (accion == "create"):
        #printt("[!] Creando nuevo espacio de servidor BDS [!]")
        
        name = input(f"{' '*2}[B-CTL] Ingrese el nombre => ")
        ruta_de_servidor = input(f"")
    else:
        sys.exit(127)
