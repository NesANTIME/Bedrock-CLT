import random
from colorama import Style, init
init(autoreset=True)

from config.load_config import get_content


# Animaciones en pantalla ~~~
def logo():
    lista_logotipos = get_content("logotipo")

    logo_aleatorio = random.choice(list(lista_logotipos.keys()))
    for i in lista_logotipos.get(logo_aleatorio):
        print(f"{Style.BRIGHT}{i}")
    
    print(f"{Style.DIM}by Nesantime {Style.NORMAL}---{Style.DIM} V{get_content("version")}{Style.RESET_ALL}")


