import os
import json
from pathlib import Path

from config.load_config import get_content


# File_Content del usuario existe? ---
def exist_file_for_user():
    file = os.path.join(get_content("ruta_forUser"))
    print(file)



def connect_file_for_user(content):
    mode = content.get("mode")

    if (mode == "create_bds"):
        name = content.get("name")
        ruta = content.get("ruta")
        del content

        exist_file_for_user()

        ## POR AQUI

