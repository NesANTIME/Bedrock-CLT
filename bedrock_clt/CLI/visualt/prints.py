import sys

from colorama import Fore, Style, init
init(autoreset=True)


# Manejo de errores en B-CLT ~~~
def exception_error(message, code):
    print(f"{' '*2}{Fore.RED + Style.BRIGHT}[⚠]{Style.NORMAL} Bedrock-CLT - Error (EFx{code}): {Style.RESET_ALL}{message}")
    sys.exit(int(code))


def exception_alert(message):
    print(f"{' '*2}{Fore.YELLOW + Style.BRIGHT}[⚠]{Style.NORMAL} Bedrock-CLT - Alerta: {Style.RESET_ALL}{message}")


# Funciones de Imprimida ~~~
def print_title(title):
    print(f"{' '*2}{Fore.YELLOW + Style.BRIGHT}[!]{Style.NORMAL} {title} {Style.BRIGHT}[!] {Style.RESET_ALL}")

def print_information(message):
    print(f"\n{Fore.BLUE + Style.BRIGHT}[INFO]{Style.RESET_ALL} {message}")







def printt(message):
    print(f"{' '*2}{message}")