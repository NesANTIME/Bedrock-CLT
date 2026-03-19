import os
import sys
import json
import hashlib
import requests
from pathlib import Path
from functools import lru_cache

from visualt.prints import print_error


@lru_cache(maxsize=1)
def load_fileController():
    hash_sha256 = hashlib.sha256()
    ruta_at_config_file = Path(__file__).parent / "file_controller.json"

    if (not os.path.isfile(ruta_at_config_file)):
        print_error("Archivos de configuracion faltantes o corruptos!") 
        sys.exit(2)

    with open(ruta_at_config_file, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloque)


    try:
        respuesta = requests.get("https://gist.githubusercontent.com/NesANTIME/002b0796f6ced3901df85c7f94e76e7d/raw/bedrock_clt(CodesSegurity)")
        respuesta.raise_for_status()
        hash_sha256_content = respuesta.json()
    except Exception:
        print_error("No se puedo obtener acceso a los archivos de configuracion remotos!")
        sys.exit(1)


    if (hash_sha256.hexdigest() != hash_sha256_content.get("file_controller_SHA256")):
        print_error("Archivos de configuracion faltantes o corruptos!") 
        sys.exit(2)

    with open(ruta_at_config_file, "r", encoding="utf-8") as f:
        return json.load(f)




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
        return FILE_JSON.get("ruts").get("standar_controller_files_linux").get("file_for_user")