import os
import time
from alive_progress import alive_bar
from colorama import Fore, Style, init

init(autoreset=True)

from config.load_config import get_content



def check_files_and_folders_BDS(ruta):
    files, folders = get_content("resources_checkBDS")
    content_list = (files + folders)

    exists = True

    print(f"\n{' '*2}[i] Iniciando verificación en:\n{' '*4}{Style.DIM}{ruta}{Style.RESET_ALL}")

    with alive_bar(len(content_list), title='  Verificando integridad', bar='classic', spinner='classic') as bar:
        for item in content_list:
            destino = os.path.join(ruta, item)
            
            if (not os.path.exists(destino)):
                bar.text(f" Error: {item}")
                exists = False
            else:
                bar.text(f" OK: {item}")
            
            time.sleep(0.3) 
            bar()

    print(f"\n{' '*2}[+] Verificación finalizada.")
    return exists



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