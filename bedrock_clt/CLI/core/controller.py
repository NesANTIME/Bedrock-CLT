import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

#  Modulos internos de B-CLT -----------------------------------
from config.manager_user import connect_file_for_user
from core.modules.manager_file import navegador_directorios
from core.modules.check_BDS import check_files_and_folders_BDS, return_version_for_BDS
from visualt.prints import print_title, exception_error, exception_alert



def controller_Servers(accion):
    if (accion == "create"):
        print_title("Creando nuevo espacio de servidor BDS")

        name_bds = input(f"{' '*2}• {Fore.BLUE}[B-CTL]{Style.RESET_ALL} Ingrese Nombre => {Style.DIM + Fore.GREEN}")

        input(f"\n{Style.RESET_ALL}{' '*2}Ingresa la ruta a el BDS...{Style.DIM} Presione enter para abrir el gestor!{Style.RESET_ALL}")

        while True:      
            ruta = navegador_directorios(".")

            if (ruta):
                print(f"{' '*2}• {Fore.BLUE}[B-CTL]{Fore.RESET} Ruta seleccionada: {Style.DIM}{ruta}{Style.RESET_ALL}")
                break

            exception_alert("No se ha especificado la ruta")
            time.sleep(3)

        confirm, not_files = check_files_and_folders_BDS(ruta)

        if (not confirm):
            print(f"{' '*4}Recursos no encontrados: {not_files}")
            exception_error("El directorio seleccionado no cumple con los requisitos de un BDS.", 1)
            
        version = return_version_for_BDS(ruta)

        connect_file_for_user( {'mode': 'create_bds', 'name': name_bds, 'version': version, 'ruta': ruta} )
            
            

    else:
        sys.exit(127)