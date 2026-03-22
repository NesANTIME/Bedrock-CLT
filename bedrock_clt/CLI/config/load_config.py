import os
import io
import sys
import json
import hashlib
import requests
from pathlib import Path
from functools import lru_cache

from visualt.prints import exception_error, print_information



#  Funcion LOAD_FILECONTROLLER ~~~
# funciones auxiliares ~~
def aux_fileController__extractSha256(content_file):
    Hash_SHA256 = hashlib.sha256()
    if isinstance(content_file, dict):
        content_file = json.dumps(content_file, sort_keys=True)

    content_file_binary = io.BytesIO(content_file.encode('utf-8'))

    for bloque in iter(lambda: content_file_binary.read(4096), b""):
        Hash_SHA256.update(bloque)

    return str(Hash_SHA256.hexdigest())


def aux_fileController__Connections_Github() -> bool:
    try:
        response = requests.head("https://github.com", timeout=3, allow_redirects=True)
        return response.ok
    except (requests.ConnectionError, requests.Timeout):
        return False
    

def aux_fileController__readFileBinary(rut_file):
    try:
        with open(rut_file, 'rb') as f:
            contenido_binario = f.read()            
            return json.loads(contenido_binario.decode('utf-8'))
    except Exception as e:
        exception_error(f"Error al cargar: {e}", 2)


def aux_fileController__connectFileGithub():
    try:
        json_file = requests.get(
            "https://gist.githubusercontent.com/NesANTIME/002b0796f6ced3901df85c7f94e76e7d/raw/bedrock_clt(CodesSegurity)"
        )
        
        json_file.raise_for_status()
        return json_file.json()
    
    except Exception:
        exception_error("No se puedo obtener acceso a los archivos de configuracion remotos!", 1)



@lru_cache(maxsize=1)
def load_fileController():
    NOT_USER = True 
    ruta_at_config_file = Path(__file__).parent / "file_controller.json"

    if (not os.path.isfile(ruta_at_config_file)):
        exception_error("Archivos de configuracion faltantes!", 2)

    with open(ruta_at_config_file, "r", encoding="utf-8") as f:
        content_file = json.load(f)

    connections_internet = aux_fileController__Connections_Github()
    if (connections_internet) and (NOT_USER):
        code_Sha256_for_file = aux_fileController__extractSha256(content_file)
        ruta_at_cache_file = Path(os.getenv('XDG_CACHE_HOME', '~/.cache')).expanduser() / "bedrock-clt" / "0xB-CTL8654"

        if (os.path.isfile(ruta_at_cache_file)):
            content_json = aux_fileController__readFileBinary(ruta_at_cache_file)
        else:
            content_json = aux_fileController__connectFileGithub()

        if (code_Sha256_for_file != content_json.get("file_controller_SHA256")):
            exception_error("Archivos de configuracion corruptos!", 2)

    elif (not connections_internet) and (NOT_USER):
            exception_error("No se realizo correctamente la verificacion!", 2)

    else:
        print_information("Autoverificacion desactivada, el programa es sensible a fallos!")

    return content_file

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




def get_content(delivery):
    FILE_JSON = load_fileController()

    # Version del programa
    if (delivery == "version"):
        return FILE_JSON.get("information").get("Version_Program")
    
    # Lista de logos
    elif (delivery == "logotipo"):
        return FILE_JSON.get("information").get("logos")
    
    # Nombre del programa
    elif (delivery == "name_program"):
        return FILE_JSON.get("information").get("Program")
    
    # Repository Oficial
    elif (delivery == "repository"):
        return FILE_JSON.get("information").get("Repository")
    
    # Perfil Creador
    elif (delivery == "github_autor"):
        return FILE_JSON.get("information").get("Developer")
    
    # Modulo check_BDS
    elif (delivery == "resources_checkBDS"):
        content = FILE_JSON.get("resources-modules").get("check_BDS")
        return content.get("files", []), content.get("folders", [])
    
    # ruta de "for_user"
    elif (delivery == "ruta_forUser"):
        return FILE_JSON.get("ruts").get("standar_controller_files_linux").get("directorio_archivo_configuracion")
    
    # Ruta de cache
    elif (delivery == "cache_file_githubuser_sha256"):
        return FILE_JSON.get("ruts").get("standar_controller_files_linux").get("cache")