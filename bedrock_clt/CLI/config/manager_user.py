import os
import json

from config.load_config import get_content
from visualt.prints import exception_error


# File_Content del usuario existe? ---
def read_file_for_user():
    file = os.path.join(get_content("ruta_forUser"), 'config.json')

    if (not os.path.isfile(file)):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump({"spaces": {}}, f, indent=4, ensure_ascii=False)

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)
    

def write_file_for_user(data):
    try:
        file = os.path.join(get_content("ruta_forUser"), 'config.json')

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)   

    except (FileNotFoundError, PermissionError, TypeError) as e:
        exception_error(f"Error al escribir el archivo: {e}", 2)
    except Exception as e:
        exception_error(f"Error inesperado: {e}", 2)




def connect_file_for_user(content):
    mode = content.get("mode")

    if (mode == "create_bds"):
        name = content.get("name")
        ruta = content.get("ruta")
        version = content.get("version")
        del content

        content_file = read_file_for_user()
        content_file["spaces"][name] = { "version_BDS": version, "ruta_at_BDS": ruta }

        write_file_for_user(content_file)