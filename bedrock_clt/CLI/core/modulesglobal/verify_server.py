import os
import re
import time
import subprocess
from pathlib import Path
from alive_progress import alive_bar
from colorama import Fore, Style, init

init(autoreset=True)

from config.load_config import Return_Content_Config


def verificar_integridad_servidor_bds(ruta_bds):
    content_list = Return_Content_Config.return_list_filesfolders()
    ruta_bds = Path(ruta_bds)

    print(f"{' '*4}{Fore.GREEN}[i]{Style.RESET_ALL} Iniciando verificacion!{Style.RESET_ALL}")

    files_and_foldes_not_exist = []

    with alive_bar(len(content_list), title=f'{' '*5}Verificando integridad', bar='classic', spinner='classic') as bar:
        for item in content_list:
            destino = ruta_bds / item
            
            if (not destino.is_file()):
                bar.text(f" Error: {item}")
                files_and_foldes_not_exist.append(item)
            else:
                bar.text(f" OK: {item}")
            
            time.sleep(0.3) 
            bar()

    del content_list, destino

    print(f"{' '*4}{Fore.BLUE}[B-CLT]{Style.RESET_ALL} Verificacion finalizada.\n")

    file_exists = ruta_bds / "./b-clt" / ".connections_spaces"
    repeat = file_exists.is_file()

    return files_and_foldes_not_exist, repeat



def obtener_version_servidor_bds(ruta):
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "." 

    executable_path = Path(ruta) / 'bedrock_server'

    try:
        process = subprocess.Popen(
            [executable_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            bufsize=1
        )

        version = False

        for _ in range(20):
            line = process.stdout.readline()
            if not line:
                break
            
            match = re.search(r"Version:\s+([0-9a-zA-Z\.-]+)", line)
            if match:
                version = match.group(1)
                break
        
        process.terminate()
        process.wait(timeout=2)

        cache_BDS = Path(__file__).parent.parent / "Dedicated_Server.txt"
        if (cache_BDS.is_file()):
            cache_BDS.unlink()

        del cache_BDS
        return version

    except Exception as e:
        return f"Error: {e}"