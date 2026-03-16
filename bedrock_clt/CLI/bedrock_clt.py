import os
import sys
import argparse
from colorama import Fore, Style, init
init(autoreset=True)

from visualt.prints import printt
from visualt.animations import logo
from config.load_config import get_content
from core.controller import controller_Servers



def info_version():
    logo()
    version_instalada = get_content("version")
    print(f"┌{'─'*68}┐")
    printt(f"{Style.BRIGHT}[Code_Proyect]{Style.RESET_ALL} B-CTL")
    printt(f"{Style.BRIGHT}[GitHub Autor] {Style.RESET_ALL}{get_content("github_autor")}")
    printt(f"{Style.BRIGHT}[Version Instalada] {Style.RESET_ALL}{version_instalada}")
    printt(f"{Style.BRIGHT}[Repositorio Oficial] {Style.RESET_ALL}{get_content("repository")}")
    print(f"└{'─'*68}┘\n")
    sys.exit(0)




Cli_Parser = argparse.ArgumentParser(prog="Bedrock-CLT", description="Administrador de DBS (Minecraft Dedicated Server)")

# Version
Cli_Parser.add_argument("--version", action="store_true", help="[!] Imprimir la version actual del programa.")


# Contenedor de subcomandos "Servers"
subparsers = Cli_Parser.add_subparsers(dest="comando_principal", help="Comandos de Bedrock-CLT")
parser_servers = subparsers.add_parser("servers", help="Gestión de servidores")
sub_servers = parser_servers.add_subparsers(dest="accion", required=True)
# Create
parser_create = sub_servers.add_parser("create", help="Crea un nuevo servidor")
# List
parser_list = sub_servers.add_parser("list", help="Lista los servidores configurados")
# Remove
parser_remove = sub_servers.add_parser("remove", help="Elimina un servidor")
parser_remove.add_argument("id", type=int, help="ID del servidor a eliminar")
# Edit
parser_edit = sub_servers.add_parser("edit", help="Edita la configuración de un servidor")




args = Cli_Parser.parse_args()

logo()
if (args.version):
    info_version()
elif (args.comando_principal == "servers"):
    controller_Servers(args.accion)
else:
    Cli_Parser.print_help()