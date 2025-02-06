import os
import json
import requests
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# 🔧 Configuración
with open(os.path.join(BASE_PATH, "config.json")) as f:
    config = json.load(f)
CLOUDFLARE_API_TOKEN = config["CLOUDFLARE_API_TOKEN"]
ZONE_ID = config["ZONE_ID"]
DOMINIOS = config["DOMINIOS"]
LOG_FILE = os.path.join(BASE_PATH, "update.log")  # Archivo de log único
LAST_IP_FILE = os.path.join(BASE_PATH, "last_ip.txt")  # Archivo para almacenar la última IP usada

# 📡 Obtener la IP pública actual
def obtener_ip_publica():
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        return response.json()["ip"]
    except Exception as e:
        print(f"Error obteniendo la IP pública: {e}")
        return None

# 📂 Guardar log en un solo archivo
def guardar_log(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} - {mensaje}\n")

# 🔄 Actualizar registros en Cloudflare
def actualizar_dns():
    ip_actual = obtener_ip_publica()
    if not ip_actual:
        print("No se pudo obtener la IP pública. Saliendo...")
        return

    # Leer última IP almacenada
    if os.path.exists(LAST_IP_FILE):
        with open(LAST_IP_FILE, "r") as file:
            last_ip = file.read().strip()
    else:
        last_ip = ""

    # Si la IP no ha cambiado, no hacemos nada
    if ip_actual == last_ip:
        print("La IP no ha cambiado. No se necesita actualizar.")
        return

    print(f"⚡ Nueva IP detectada: {ip_actual}")

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    cambios_realizados = False

    for dominio in DOMINIOS:
        # Buscar el ID del registro DNS en Cloudflare
        url_busqueda = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?type=A&name={dominio}"
        respuesta_busqueda = requests.get(url_busqueda, headers=headers).json()

        if respuesta_busqueda["success"] and respuesta_busqueda["result"]:
            record_id = respuesta_busqueda["result"][0]["id"]
            
            # Actualizar el registro con la nueva IP
            url_actualizar = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}"
            data = {
                "type": "A",
                "name": dominio,
                "content": ip_actual,
                "ttl": 120,  # Tiempo de vida (TTL)
                "proxied": DOMINIOS[dominio]["proxied"],  # True para proxy activado (nube naranja)
            }
            respuesta_actualizar = requests.put(url_actualizar, headers=headers, json=data).json()

            if respuesta_actualizar["success"]:
                print(f"✔ IP actualizada para {dominio}: {ip_actual}")
                cambios_realizados = True
            else:
                print(f"❌ Error actualizando {dominio}: {respuesta_actualizar}")
        else:
            print(f"❌ No se encontró el registro DNS para {dominio}")

    # Si hubo cambios, guardamos la nueva IP y añadimos un log
    if cambios_realizados:
        with open(LAST_IP_FILE, "w") as file:
            file.write(ip_actual)
        guardar_log(f"IP cambiada a {ip_actual} para {', '.join(DOMINIOS)}")


if __name__ == "__main__":
    # Ejecutar script
    actualizar_dns()