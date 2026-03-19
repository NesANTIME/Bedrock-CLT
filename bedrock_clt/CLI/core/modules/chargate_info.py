from colorama import Fore, Style, init
init(autoreset=True)

from config.load_config import get_content



def version_information():
    name = get_content("name_program")
    author = get_content("github_autor")
    version = f"v{get_content('version')}"
    repository = get_content("repository")

    print(f"\n╭{'─'*68}╮")
    print(f"│• {Style.BRIGHT}Code_Proyect{' '*8}:  {Style.RESET_ALL}{name}{' '*(43 - len(name))}│")
    print(f"│• {Style.BRIGHT}GitHub Autor{' '*8}:  {Style.RESET_ALL}{author}{' '*(43 - len(author))}│")
    print(f"│• {Style.BRIGHT}Version Instalada{' '*3}:  {Style.RESET_ALL}{version}{' '*(43 - len(version))}│")
    print(f"│• {Style.BRIGHT}Repositorio Oficial :  {Style.RESET_ALL}{repository}{' '*(43 - len(repository))}│")
    print(f"╰{'─'*68}╯\n")