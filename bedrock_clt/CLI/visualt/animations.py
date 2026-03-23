import random
from colorama import Style, init, Fore
init(autoreset=True)

from config.load_config import get_content


# Animaciones en pantalla ~~~
def logo():
    lista_logotipos = get_content("logotipo")

    logo_aleatorio = random.choice(list(lista_logotipos.keys()))
    for i in lista_logotipos.get(logo_aleatorio):
        print(f"{Style.BRIGHT}{i}")
    
    print(f"{' '*20}{Style.DIM}by Nesantime {Style.NORMAL}---{Style.DIM} Version: {get_content("version")}{Style.RESET_ALL}")
    del logo_aleatorio
    del lista_logotipos



def recuadro_information(name, version, ruta):
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

    del primary_
    del secondary_
    del terciary_
    del linea1
    del linea2
    del linea3
    del name
    del version
    del ruta