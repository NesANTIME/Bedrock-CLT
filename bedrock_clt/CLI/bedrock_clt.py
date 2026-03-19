import sys
import argparse

from visualt.animations import logo
from core.modules.chargate_info import version_information
from core.controller import controller_Servers




Cli_Parser = argparse.ArgumentParser(prog="Bedrock-CLT", description="Administrador de DBS (Minecraft Dedicated Server)")

# Version
Cli_Parser.add_argument("--version", action="store_true", help="[!] Imprimir la version actual del programa.")


# Contenedor de subcomandos "spaces"
subparsers = Cli_Parser.add_subparsers(dest="comando_principal", help="Comandos de Bedrock-CLT")
parser_servers = subparsers.add_parser("spaces", help="Gestión de servidores")
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
    version_information()
    sys.exit(0)

elif (args.comando_principal == "spaces"):
    controller_Servers(args.accion)
else:
    Cli_Parser.print_help()