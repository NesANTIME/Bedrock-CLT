import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

#  Modulos internos de B-CLT -----------------------------------
from visualt.animations import recuadro_information
from config.manager_user import connect_file_for_user
from core.modules.manager_file import navegador_directorios
from core.modules.check_BDS import check_files_and_folders_BDS, return_version_for_BDS, enlace_spaces
from visualt.prints import print_title, exception_error, exception_alert, print_normal



def controller_Servers(accion):
    if (accion == "create"):
        print_title("Creando nuevo espacio de servidor BDS")

        while True:
            name_bds = input(f"{' '*2}• {Fore.BLUE}[B-CTL]{Style.RESET_ALL} Ingrese Nombre => {Style.DIM + Fore.GREEN}")

            caracteres_ = len(name_bds)
            if (caracteres_ >= 10):
                exception_alert("El nombre no puede superar los 10 caracteres.")
            elif (caracteres_ <= 0):
                exception_alert("No se puede continuar sin nombre.")
            else:
                break
        
        del caracteres_

        input(f"\n{Style.RESET_ALL}{' '*2}Ingresa la ruta a el BDS...{Style.DIM} Presione enter para abrir el gestor!{Style.RESET_ALL}")

        while True:      
            ruta = navegador_directorios(".")

            if (ruta):
                print_normal(f"Ruta seleccionada: {Style.DIM}{ruta}{Style.RESET_ALL}")
                break

            exception_alert("No se ha especificado la ruta")
            time.sleep(3)

        confirm, not_files, repeat = check_files_and_folders_BDS(ruta)

        if (repeat):
            exception_error("El directorio seleccionado ya contiene un 'spaces' enlazado!", 2)

        if (not confirm):
            print_normal(f"Recursos no encontrados: {not_files}")
            exception_error("El directorio seleccionado no cumple con los requisitos de un BDS.", 1)
            
        version = return_version_for_BDS(ruta)

        connect_file_for_user( {'mode': 'create_bds', 'name': name_bds, 'version': version, 'ruta': ruta} )

        enlace_spaces(ruta)
        print_normal(f'(Spaces: {name_bds}) - (Version: {version}) guardado con exito!')

    
    elif (accion == "list"):
        print_title("Listando los espacios guardados")

        lista_bds = connect_file_for_user({'mode': 'read_bds'})
        for name, datos in lista_bds.get("spaces", {}).items():
            recuadro_information(name, datos.get('version_BDS'), datos.get('ruta_at_BDS'))

    else:
        sys.exit(127)