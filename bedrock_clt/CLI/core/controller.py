import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

from config.manager_user import connect_file_for_user
from visualt.prints import printt, print_alert, print_error
from core.modules.manager_file import navegador_directorios
from core.modules.check_BDS import check_files_and_folders_BDS


def controller_Servers(accion):
    if (accion == "create"):

        printt(f"{Fore.YELLOW + Style.BRIGHT}[!]{Style.NORMAL} Creando nuevo espacio de servidor BDS {Style.BRIGHT}[!] {Style.RESET_ALL}")

        name_bds = input(f"{' '*2}• {Style.BRIGHT}[B-CTL]{Style.NORMAL} Ingrese Nombre => {Style.DIM + Fore.GREEN}")

        input(f"{Style.RESET_ALL}{' '*2}Ingresa la ruta a el BDS...{Style.DIM} Presione enter para abrir el gestor!{Style.RESET_ALL}")

        while True:         
            ruta = navegador_directorios(".")

            if ruta:
                print(f" {Fore.GREEN}[B-CTL]{Fore.RESET} Ruta seleccionada: {Style.DIM}{ruta}{Style.RESET_ALL}")
                break

            print_alert(f"No se ha especificado la ruta")

        if (not check_files_and_folders_BDS(ruta)):
            print_error("El directorio seleccionado no cumple con los requisitos de un BDS.")
            sys.exit(1)

        connect_file_for_user( {'mode': 'create_bds', 'name': name_bds, 'ruta': ruta} )
    else:
        sys.exit(127)