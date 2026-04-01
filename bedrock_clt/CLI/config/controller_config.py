import json
from pathlib import Path

from visualt.prints import exception_error
from config.load_config import Return_Content_Config

LOAD_CONFIG = Return_Content_Config()


class Controller_Config_Local:
    def __init__(self):
        self.ruta_file_config_ = Path(LOAD_CONFIG.get_ruts_configuracion) / 'config.json'

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