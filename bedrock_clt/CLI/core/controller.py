import sys
import time
import uuid
import random
from colorama import Fore, Style, init

init(autoreset=True)

#  Modulos internos de B-CLT -----------------------------------
from core.modulesglobal.funcs_bds import Functions_For_BDS, Controller_Enlace_Space_Bds

from visualt.aesthetics import generar_recuadro_para_listar
from core.modulesglobal.explorer import navegador_directorios
from visualt.prints import print_title, exception_error, exception_alert, print_normal
from core.modulesglobal.verify_server import verificar_integridad_servidor_bds, obtener_version_servidor_bds

CONTROLLER_INTERNAL_BDS = Functions_For_BDS()



class Controller_Functions_Bclt:
    def __init__(self):
        pass


    def create(self):
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
        code_uuid = str(uuid.uuid4())


        while True:
            control_bds = CONTROLLER_INTERNAL_BDS.save_space_bds(name_bds, str(ruta), version, code_uuid)

            if (control_bds):
                break
            
            name_bds = f"{name_bds}{random.randrange(10, 100)}"

        CONTROLLER_SPACES = Controller_Enlace_Space_Bds(ruta, code_uuid)
        CONTROLLER_SPACES.create_enlace()

        print_normal(f'(Spaces: {name_bds}) - (Version: {version}) guardado con exito!')

    
    def lists(self):
        print_title("Listando los espacios guardados")

        lista_bds = CONTROLLER_INTERNAL_BDS.load_spaces_bds()
        if not isinstance(lista_bds, dict):
            return False, None

        for key, datos in lista_bds.items():            
            generar_recuadro_para_listar(str(datos.get("name")), str(datos.get("version")), str(datos.get("ruta")))

    
    def remove(self, name_space):
        print_title("Eliminando espacios")
        print_normal(f"Buscando: {name_space}")

        exit_, content = CONTROLLER_INTERNAL_BDS.deleted_space_bds(name_space)

        if (not exit_):
            exception_error("El 'spaces' no existe, compruebe el nombre ingresado e intentenlo nuevamente.", 2)


        CONTROLLER_SPACES = Controller_Enlace_Space_Bds(content.get("ruta"), content.get("uuid"))
        resolv = CONTROLLER_SPACES.deleted_enlace()

        if (not resolv):
            exception_error("El 'code_spaces' no corresponde al BDS registrado, es posible la manipulacion de archivos.", 2)

        print_normal("Eliminado correctamente!")