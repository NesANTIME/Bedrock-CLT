import json
from pathlib import Path

from visualt.prints import exception_error
from config.load_config import Return_Content_Config

FILE_USER_CONFIG = Path(Return_Content_Config.get_ruts_configuracion) / 'config.json'



class Controller_Config_Local:
    def __init__(self):
        self.ruta_file_config_ = Path(Return_Content_Config.get_ruts_configuracion) / 'config.json'

    def file_exist(self):
        if (not self.ruta_file_config_.is_file()):
            self.write_file_config({"spaces": {}})
    
    def read_file_config(self):
        with open(self.ruta_file_config_, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def write_file_config(self, data_):
        try:
            with open(self.ruta_file_config_, 'w', encoding='utf-8') as f:
                json.dump(data_, f, indent=4, ensure_ascii=False)   

        except (FileNotFoundError, PermissionError, TypeError) as e:
            exception_error(f"Error al escribir el archivo: {e}", 2)
        except Exception as e:
            exception_error(f"Error inesperado: {e}", 2)





def controlador_configuracion_local(content):
    mode = content.get("mode")

    if (mode == "create_bds"):
        name = content.get("name")
        ruta = str(content.get("ruta"))
        version = content.get("version")
        del content

        content_file = Controller_Config_Local.read_file_config()
        content_file["spaces"][name] = { "version_BDS": version, "ruta_at_BDS": ruta }

        Controller_Config_Local.write_file_config(content_file)

    elif (mode == "read_bds"):
        return Controller_Config_Local.read_file_config()