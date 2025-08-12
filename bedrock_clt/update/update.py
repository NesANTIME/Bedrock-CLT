import os
import json
import requests
from colorama import Fore, Style

def load_config():
    base_path = os.path.dirname(__file__)
    update_path = os.path.join(base_path, "update.json")

    with open(update_path, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def Update():  
    datos = load_config()    
    VerLocal = datos["bedrock-clt_version"][0]
    VerNew = datos["bedrock-clt_version"][1]
    
    
    def V_NewVer(VerNew):
        try:
            response = requests.get(VerNew)
            if response.status_code == 200:
                remote_data = response.json()
                return remote_data["bedrock-clt_version"][0]
            else:
                print(f"[!] Error al obtener el archivo remoto, código de estado: {response.status_code}")
                return
        except requests.exceptions.Timeout:
            print("[!] Timeout al conectar con el servidor remoto.")
            return
        except requests.exceptions.ConnectionError as e:
            print(f"[!] Error de conexión: {e}")
            return
        except requests.exceptions.RequestException as e:
            print(f"[!] Error inesperado en la solicitud: {e}")
            return

        
    def V_LocalVer(VerLocal, V_NewUp):
        try:
            if VerLocal == V_NewUp:
                return f"{Fore.RESET + Style.RESET_ALL}"
            else:
                return f"\n   {Fore.CYAN + Style.BRIGHT}[!] {Fore.WHITE}Hay una nueva version disponible {Style.DIM + V_NewUp + Fore.GREEN} {Style.BRIGHT}¡Descargala YA!{Fore.RESET + Style.NORMAL}\n"
        except Exception as e:
            print(f"{Fore.RED}   [!] Error al leer el archivo local {VerLocal}: {e}")
            
    V_NewUp = V_NewVer(VerNew)
    if V_NewUp is not None:
        return V_LocalVer(VerLocal, V_NewUp)
    else:
        return Fore.RED + "[!] No se pudo obtener el contenido remoto para comparar."
    

def Install_Update():
    datos = load_config()  # Tu config local con rutas
    base_path = os.path.dirname(os.path.abspath(__file__))

    def obtener_main_update():
        url = "https://raw.githubusercontent.com/NesANTIME/Bedrock-CLT/refs/heads/main/update/main.json"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("[!] Timeout al conectar con el servidor remoto.")
        except requests.exceptions.ConnectionError as e:
            print(f"[!] Error de conexión: {e}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Error inesperado en la solicitud: {e}")
        return None

    respuesta = obtener_main_update()
    if not respuesta:
        print("[!] No se pudo obtener la información de actualización.")
        return

    # Recorremos todos los archivos dentro de la clave "1.6"
    archivos_remotos = respuesta.get("1.6", {})
    for nombre_archivo, ruta_lista in archivos_remotos.items():
        # Construimos ruta absoluta local para guardar el archivo
        ruta_local = os.path.normpath(os.path.join(base_path, *ruta_lista))

        # Construimos la URL remota del archivo para descargarlo
        # Esto depende de cómo esté organizado tu repo. 
        # Aquí asumo que el archivo está en la rama main bajo la carpeta update/
        url_archivo = f"https://raw.githubusercontent.com/NesANTIME/Bedrock-CLT/main/{nombre_archivo}"

        try:
            res = requests.get(url_archivo, timeout=10)
            res.raise_for_status()
            # Creamos carpetas si no existen
            os.makedirs(os.path.dirname(ruta_local), exist_ok=True)
            with open(ruta_local, 'w', encoding='utf-8') as f:
                f.write(res.text)
            print(f"[+] {ruta_local} actualizado correctamente.")
        except requests.exceptions.RequestException as e:
            print(f"[!] Error descargando {nombre_archivo}: {e}")

    # Si quieres, puedes usar 'datos' para algo más, pero así queda claro
    for nombre, partes_ruta in datos.get("archivos", {}).items():
        ruta = os.path.join(base_path, *partes_ruta)
        print(f"{nombre}: {ruta}")