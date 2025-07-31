import os
import sys
import json
import time
import threading
import subprocess
from colorama import init, Fore, Style
init(autoreset=True)

def load_config():
    with open("bedrock_clt/config.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def load_playersConnect():
    with open("bedrock_clt/modules/players_connect.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def save_playersConnect(data):
    with open("bedrock_clt/modules/players_connect.json", "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)

def load_protocolStopServer():
    with open("bedrock_clt/modules/protocol_stop_server.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def load_commands():
    with open("bedrock_clt/commands/commands.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)


    
def connected_and_disconnected(jugador, mode):
    list_players = load_playersConnect()

    if mode == "connected":
        if jugador not in list_players["players_online"]:
            list_players["players_online"].append(jugador)
    
    elif mode == "disconnected":
        if jugador in list_players["players_online"]:
            list_players["players_online"].remove(jugador)

    else:
        comandos = load_protocolStopServer()
        for i in comandos["protocol_stop_server"]:
            enviar(i)
            time.sleep(1)

        for player in list_players["players_online"]:
            enviar("kick "+ player + " El servidor se ha Apagado, Por favor vuelve más tarde.")
            time.sleep(1)
            
        list_players["players_online"].clear()

    save_playersConnect(list_players)






def leer_logs():
    for line in iter(bedrock_server.stdout.readline, ''):  
        line = line.strip()

        if ("Player connected" in line):
            nombre = line.split("Player connected: ")[1].split(",")[0].strip()
            connected_and_disconnected(nombre, "connected")
            print(f"{Fore.GREEN}[B-CLT]{Fore.RESET} Se ha conectado el Jugador {Fore.BLUE + Style.DIM + nombre + Style.RESET_ALL}")

        elif ("Player disconnected" in line):
            nombre = line.split("Player disconnected: ")[1].split(",")[0].strip()
            print(f"{Fore.RED}[B-CLT]{Fore.RESET} Se desconectó un Jugador: {Fore.RED + Style.DIM} {nombre}{Style.RESET_ALL}")
            connected_and_disconnected(nombre, "disconnected")

        else:
            print(f"{Fore.CYAN}[B-CLT]{Fore.RESET}", line.strip())

        print("> ", end="", flush=True)


def enviar(cmd):
    bedrock_server.stdin.write(cmd + "\n")
    bedrock_server.stdin.flush()











config = load_config()
commands_for_user = load_commands()
if (config["VersionSO"] == 0):
    subprocess.run("bash -c 'ulimit -n 1048576 && ulimit -u unlimited'", shell=True)
    execute = ["taskset", "-c", "0-3", "nice", "-n", "-20", "./bedrock_server"]
    print(f"{Fore.GREEN}[B-CLT]{Style.DIM} INICIADO CORRECTAMENTE {Style.RESET_ALL}")

elif (config["VersionSO"] == 1):
    execute = "bedrock_server.exe"
    if ("ruta_raiz" in config):
        execute = f"{config["ruta_raiz"]}/{execute}"
    print(f"{Fore.GREEN}[B-CLT]{Style.DIM} INICIADO CORRECTAMENTE {Style.RESET_ALL}")

else:
    print(f"{Fore.RED}[B-CLT [ERROR]]{Style.DIM} Configuracion en config.json Erronea {Style.RESET_ALL}")
    sys.exit(1)
    

bedrock_server = subprocess.Popen(execute, cwd=os.path.dirname(execute), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        bufsize=1, universal_newlines=True)

threading.Thread(target=leer_logs, daemon=True).start()


# ----------------- INTERFAZ -----------------
try:
    print(Fore.CYAN + Style.BRIGHT + "\n[✔] Servidor BDS iniciado correctamente.")

    while True:
        cmd = input(Fore.CYAN + Style.BRIGHT + "> " + Style.RESET_ALL).strip()
        if not cmd:
            continue

        if cmd.startswith("#"):
            if cmd in commands_for_user:
                comando = commands_for_user[cmd]
                print(f"{Fore.BLUE + Style.BRIGHT}[B-CLT] {Style.NORMAL}Comando Personalizado Enviado: {Style.RESET_ALL}{comando}")
                enviar(comando)
                continue
            else:
                print(f"[X] Comando desconocido: {cmd}")
                continue

        if cmd.lower() == "stop":
            print(f"\n{Fore.BLUE}[B-CLT {Fore.YELLOW}[INFO]{Fore.BLUE}]{Fore.YELLOW} Iniciando apagado del servidor...{Style.RESET_ALL}\n")
            time.sleep(0.3)
            print(f"{Fore.BLUE}[B-CLT {Fore.GREEN}[✔]{Fore.BLUE}]{Style.RESET_ALL} Limpiado cache...")
            time.sleep(0.3)
            print(f"{Fore.BLUE}[B-CLT {Fore.GREEN}[✔]{Fore.BLUE}]{Style.RESET_ALL} Expulsando jugadores...")
            connected_and_disconnected("none", "none")
            time.sleep(0.3)
            print(f"{Fore.WHITE + Style.BRIGHT}[✖] BDS Apagado...\n")
            bedrock_server.terminate()
            break

        else:
            print(f"{Fore.BLUE}[B-CLT] {Style.DIM}Comando Enviado: {Style.RESET_ALL}{cmd}")
            enviar(cmd)

except KeyboardInterrupt:
    print(Fore.RED + "\n\n[INTERRUPCIÓN] Tecla CTRL+C detectada. Apagando servidor...")
    time.sleep(0.3)
    bedrock_server.terminate()
