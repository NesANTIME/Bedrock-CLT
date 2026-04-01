import sys
import argparse

from core.controller import Controller_Functions_Bclt
from visualt.aesthetics import imprimir_logo, imprimir_recuadro_version


CONTROLLER_FUNCTIONS_BCLT = Controller_Functions_Bclt()



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
    accion = args.accionSpaces

    if (accion == "create"):
        CONTROLLER_FUNCTIONS_BCLT.create()

    elif (accion == "list"):
        CONTROLLER_FUNCTIONS_BCLT.lists()

    elif (accion == "remove"):
        CONTROLLER_FUNCTIONS_BCLT.remove(args.nameforemove)

    del accion
else:
    Cli_Parser.print_help()