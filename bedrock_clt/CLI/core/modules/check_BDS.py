import os
import re
import time
import subprocess
from alive_progress import alive_bar
from colorama import Fore, Style, init

init(autoreset=True)

from config.load_config import get_content



def check_files_and_folders_BDS(ruta):
    files, folders = get_content("resources_checkBDS")
    content_list = (files + folders)

    exists = True

    print(f"{' '*4}{Fore.GREEN}[i]{Style.RESET_ALL} Iniciando verificacion!{Style.RESET_ALL}")

    with alive_bar(len(content_list), title=f'{' '*5}Verificando integridad', bar='classic', spinner='classic') as bar:
        for item in content_list:
            destino = os.path.join(ruta, item)
            
            if (not os.path.exists(destino)):
                bar.text(f" Error: {item}")
                exists = False
            else:
                bar.text(f" OK: {item}")
            
            time.sleep(0.3) 
            bar()

    print(f"{' '*4}{Fore.BLUE}[B-CLT]{Style.RESET_ALL} Verificacion finalizada.\n")
    return exists



def return_version_for_BDS(ruta):
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "." 

    executable_path = os.path.join(ruta, 'bedrock_server')

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
        return version

    except Exception as e:
        return f"Error: {e}"



#with alive_bar(50, title='Burbujas', bar='bubbles', spinner='dots_waves') as bar:
#    for _ in range(50): time.sleep(0.05); bar()

#with alive_bar(50, title='Encriptando', bar='blocks', spinner='waves') as bar:
#    for _ in range(50):
#        time.sleep(0.05)
#        bar()

#with alive_bar(50, title='Procesando', bar='filling', spinner='dots_waves') as bar:
#    for _ in range(50):
#        time.sleep(0.05)
#        bar()

#with alive_bar(50, title='Legacy Mode', bar='classic', spinner='classic') as bar:
#    for _ in range(50): time.sleep(0.05); bar()


#with alive_bar(50, title='Smooth', bar='smooth', spinner='classic') as bar:
#    for _ in range(50): time.sleep(0.05); bar()