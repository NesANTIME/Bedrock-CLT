import os
import json

from config.load_config import get_content
from visualt.prints import exception_error


FILE_USER_CONFIG = os.path.join(get_content("ruta_forUser"), 'config.json')


# File_Content del usuario existe? ---
def read_file_for_user():
    if (not os.path.isfile(FILE_USER_CONFIG)):
        with open(FILE_USER_CONFIG, 'w', encoding='utf-8') as f:
            json.dump({"spaces": {}}, f, indent=4, ensure_ascii=False)

    with open(FILE_USER_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)
    

def write_file_for_user(data):
    try:
        with open(FILE_USER_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)   

    except (FileNotFoundError, PermissionError, TypeError) as e:
        exception_error(f"Error al escribir el archivo: {e}", 2)
    except Exception as e:
        exception_error(f"Error inesperado: {e}", 2)




def connect_file_for_user(content):
    mode = content.get("mode")

    if (mode == "create_bds"):
        name = content.get("name")
        ruta = str(content.get("ruta"))
        version = content.get("version")
        del content

        content_file = read_file_for_user()
        content_file["spaces"][name] = { "version_BDS": version, "ruta_at_BDS": ruta }

        write_file_for_user(content_file)

    elif (mode == "read_bds"):
        return read_file_for_user()
