import shutil
from pathlib import Path

from config.controller_config import Controller_Config_Local

CONTROLLER_CONFIG = Controller_Config_Local()
CONTROLLER_CONFIG.file_exist()

class Functions_For_BDS:
    def __init__(self):
        self.content_file_ = CONTROLLER_CONFIG.read_file_config()


    def save_space_bds(self, name, ruta, version, code_uuid):
        if (self.content_file_.get("spaces").get(code_uuid)):
            return False
        else:
            self.content_file_["spaces"][code_uuid] = { "name": name, "version": version, "ruta": ruta }
            CONTROLLER_CONFIG.write_file_config(self.content_file_)
            return True

    def load_spaces_bds(self):
        return self.content_file_.get("spaces", {})
    
    def deleted_space_bds(self, name):
        if not isinstance(self.content_file_, dict):
            return False, None

        spaces = self.content_file_.get("spaces", {})
        uuid_key = None
        ruta = None

        for key, info in spaces.items():
            if isinstance(info, dict) and info.get("name") == name.strip():
                uuid_key = key
                ruta = info.get("ruta")
                break

        if (not uuid_key):
            return False, None
        
        self.content_file_["spaces"].pop(uuid_key)
        CONTROLLER_CONFIG.write_file_config(self.content_file_)

        return True, {"uuid": uuid_key, "ruta": ruta}
        


class Controller_Enlace_Space_Bds:
    def __init__(self, ruta, code):
        self.ruta_carpeta = Path(ruta) / ".b-clt"
        self.ruta_file_enlace = self.ruta_carpeta / ".connections_spaces"
        self.code_uuid = code


    def create_enlace(self):
        if (not self.ruta_carpeta.exists()):
            self.ruta_carpeta.mkdir(parents=True)
        
        with open(self.ruta_file_enlace, "w", encoding="utf-8") as f:
            f.write(self.code_uuid)


    def deleted_enlace(self):
        with open(self.ruta_file_enlace, "r", encoding="utf-8") as f:
            uuid_file = f.read()

        if (uuid_file.strip() != self.code_uuid):
            return False
        
        shutil.rmtree(self.ruta_carpeta)
        return True