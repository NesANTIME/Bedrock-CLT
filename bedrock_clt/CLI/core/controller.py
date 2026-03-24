import sys
import time
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

#  Modulos internos de B-CLT -----------------------------------
from visualt.aesthetics import generar_recuadro_para_listar
from core.modulesglobal.explorer import navegador_directorios
from config.controller_config import controlador_configuracion_local
from visualt.prints import print_title, exception_error, exception_alert, print_normal
from core.modulesglobal.verify_server import verificar_integridad_servidor_bds, obtener_version_servidor_bds



def controller_functions_bclt(delivery):
    accion = delivery.get("func")

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

        files_and_folders_not_exist, repeat = verificar_integridad_servidor_bds(ruta)

        if (repeat):
            exception_error("El directorio seleccionado ya contiene un 'spaces' enlazado!", 2)

        if (files_and_folders_not_exist):
            print_normal(f"Recursos no encontrados: {files_and_folders_not_exist}")
            exception_error("El directorio seleccionado no cumple con los requisitos de un BDS.", 1)
            
        version = obtener_version_servidor_bds(ruta)

        controlador_configuracion_local( {'mode': 'create_bds', 'name': name_bds, 'version': version, 'ruta': ruta} )

        carpeta_bclt_bds = Path(ruta) / './b-clt'
        carpeta_bclt_bds.mkdir(parents=True)

        ruta_archivo_bclt = Path(carpeta_bclt_bds) / ".connections_spaces"
        
        del carpeta_bclt_bds
        
        with open(ruta_archivo_bclt, "w", encoding="utf-8") as f:
            f.write("Este BDS ya esta enlazado!")

        print_normal(f'(Spaces: {name_bds}) - (Version: {version}) guardado con exito!')

    
    elif (accion == "list"):
        print_title("Listando los espacios guardados")

        lista_bds = controlador_configuracion_local({'mode': 'read_bds'})
        for name, datos in lista_bds.get("spaces", {}).items():
            generar_recuadro_para_listar(name, datos.get('version_BDS'), datos.get('ruta_at_BDS'))



    elif (accion == "remove"):
        complements = delivery.get("complements")

        print_title("Eliminar espacios")



    else:
        sys.exit(127)