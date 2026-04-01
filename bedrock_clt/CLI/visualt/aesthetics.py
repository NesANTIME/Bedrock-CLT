import random
from colorama import Style, init, Fore
init(autoreset=True)

from config.load_config import Return_Content_Config

LOAD_CONFIG = Return_Content_Config()



# Animaciones en pantalla ~~~
def imprimir_logo():
    lista_logotipos = LOAD_CONFIG.return_list_logos()
    logo_aleatorio = random.choice(list(lista_logotipos.keys()))

    for i in lista_logotipos.get(logo_aleatorio):
        print(f"{Style.BRIGHT}{i}")
    
    print(f"{' '*20}{Style.DIM}by Nesantime {Style.NORMAL}---{Style.DIM} Version: {LOAD_CONFIG.get_version}{Style.RESET_ALL}")
    
    del logo_aleatorio, lista_logotipos


def imprimir_recuadro_version():
    name = LOAD_CONFIG.get_name
    author = LOAD_CONFIG.get_author
    version = f"v{LOAD_CONFIG.get_version}"
    repository = LOAD_CONFIG.get_repository

    print(f"\n╭{'─'*68}╮")
    print(f"│• {Style.BRIGHT}Code_Proyect{' '*8}:  {Style.RESET_ALL}{name}{' '*(43 - len(name))}│")
    print(f"│• {Style.BRIGHT}GitHub Autor{' '*8}:  {Style.RESET_ALL}{author}{' '*(43 - len(author))}│")
    print(f"│• {Style.BRIGHT}Version Instalada{' '*3}:  {Style.RESET_ALL}{version}{' '*(43 - len(version))}│")
    print(f"│• {Style.BRIGHT}Repositorio Oficial :  {Style.RESET_ALL}{repository}{' '*(43 - len(repository))}│")
    print(f"╰{'─'*68}╯\n")




# funcion de "spaces list" ~~~
def generar_recuadro_para_listar(name, version, ruta):
    len_name = len(name)
    if (len_name >= 10):
        name = name[:10] + "..."
    
    len_version = len(version)
    if (len_version >= 15):
        version = version[:17] + "..."

    len_ruta = len(ruta)
    if (len_ruta >= 40):
        ruta = ruta[:40] + "..."

    primary_ = '─'*(11 + (len_name + (12 - len_name)))
    secondary_ = '─'*(11 + (len_version + (19 - len_version)))
    terciary_ = '─'*(7 + (len_ruta + (45 - len_ruta)))
        

    linea1 = f"│ • {Fore.CYAN}Nombre: {Style.RESET_ALL}{name.ljust(12)}"
    linea2 = f"{Fore.GREEN + Style.BRIGHT}Version: {Style.RESET_ALL}{version.ljust(20)}"
    linea3 = f"{Fore.YELLOW + Style.BRIGHT}Ruta: {Style.RESET_ALL}{ruta.ljust(45)}"


    print(f"╭{primary_}┬{secondary_}┬{terciary_}╮")
    print(f"{linea1}│ {linea2}│ {linea3}│")
    print(f"╰{primary_}┴{secondary_}┴{terciary_}╯")

    del primary_, secondary_, terciary_
    del linea1, linea2, linea3
    del name, version, ruta