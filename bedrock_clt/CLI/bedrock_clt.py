import sys
import argparse

from core.controller import controller_functions_bclt
from visualt.aesthetics import imprimir_logo, imprimir_recuadro_version



Cli_Parser = argparse.ArgumentParser(prog="Bedrock-CLT", description="Administrador de DBS (Minecraft Dedicated Server)")

#   Version ~~
Cli_Parser.add_argument("--version", action="store_true", help="[!] Imprimir la version actual del programa.")


#   Comando Principal ~~
subparsers = Cli_Parser.add_subparsers(dest="comando_principal", help="[!] Comandos principales de Bedrock-CLT")

#  Subcomando "spaces" ~~~
parser_servers = subparsers.add_parser("spaces", help="[!] Gestion de los espacios!")
# Subcomando principal en "spaces" ~~~
sub_servers = parser_servers.add_subparsers(dest="accionSpaces", required=True)
# Create ~~~~
parser_create = sub_servers.add_parser("create", help="[!] Crea un nuevo espacio para servidor.")
# List ~~~~
parser_list = sub_servers.add_parser("list", help="[!] Lista los espacios creados.")
# Remove ~~~~
parser_remove = sub_servers.add_parser("remove", help="[!] Elimina un espacio creado.")
parser_remove.add_argument("nameforemove", help="Nombre de el espacio")
# Edit ~~~~
parser_edit = sub_servers.add_parser("edit", help="Edita la configuración de un servidor")
parser_edit.add_argument("nameforedit", help="Nombre de el espacio")


args = Cli_Parser.parse_args()

imprimir_logo()
if (args.version):
    imprimir_recuadro_version()
    sys.exit(0)

elif (args.comando_principal == "spaces"):
    functions = args.accionSpaces

    if (functions == "remove"):
        func = { "func": functions, "complements": args.nameforemove }
    
    elif (functions == "edit"):
        func = { "func": functions, "complements": args.nameforedit }

    else:
        func = { "func": functions, "complements": None }

    del functions
    controller_functions_bclt(func)
else:
    Cli_Parser.print_help()