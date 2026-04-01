import os
import io
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
    NOT_USER = False
    ruta_at_config_file = Path(__file__).parent / "file_controller.json"

    if (not ruta_at_config_file.is_file()):
        exception_error("Archivos de configuracion faltantes!", 2)

    with open(ruta_at_config_file, "r", encoding="utf-8") as f:
        content_file = json.load(f)

    connections_internet = aux_fileController__Connections_Github()
    if (connections_internet) and (NOT_USER):
        code_Sha256_for_file = aux_fileController__extractSha256(content_file)
        ruta_at_cache_file = Path(os.getenv('XDG_CACHE_HOME', '~/.cache')).expanduser() / "bedrock-clt" / "0xB-CTL8654"

        if (ruta_at_cache_file.is_file()):
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



class Return_Content_Config:
    def __init__(self):
        self._data_json = load_fileController()
        
        self.data_information = self._data_json.get("information")
        self.data_ruts = self._data_json.get("ruts")

    @property
    def get_name(self):
        return self.data_information.get("Program")
    
    @property
    def get_version(self):
        return self.data_information.get("Version")
    
    @property
    def get_repository(self):
        return self.data_information.get("Repository")
    
    @property
    def get_author(self):
        return self.data_information.get("Developer")
    

    def return_list_logos(self):
        return self.data_information.get("logos", {})
    

    def return_list_filesfolders(self):
        content = self._data_json.get("resources-modules").get("check_BDS")
        return (content.get("files", [])) + (content.get("folders", []))
    
    @property
    def get_ruts_configuracion(self):
        return self.data_ruts.get("standar_controller_files_linux").get("directorio_archivo_configuracion")
    
    @property
    def get_ruts_cache(self):
        return self.data_ruts.get("standar_controller_files_linux").get("cache")