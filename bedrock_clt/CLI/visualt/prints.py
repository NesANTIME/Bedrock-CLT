from colorama import Fore, Style, init
init(autoreset=True)


# Categoria de mensajes en pantalla ~~~
def print_error(message):
    print(f"{' '*2}{Fore.RED}[⚠]{Fore.WHITE + Style.BRIGHT} Bedrock-CLT - Error:{Style.RESET_ALL} {message}")

def printt(message):
    print(f"{' '*2}{message}")