import requests
import time
import os

def obtenir_liste_stations():
    try:
        reponse=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
        reponse.raise_for_status()
        donnees=reponse.json()
        return [station['address']['value']['streetAddress'] for station in donnees]
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API : {e}")
        return []
    except ValueError as e:
        print(f"Erreur de décodage JSON : {e}")
        return []

def obtenir_donnees_station(nom_station):
    try:
        reponse=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
        reponse.raise_for_status()
        donnees=reponse.json()
        for station in donnees:
            if station['address']['value']['streetAddress']==nom_station:
                return station
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API : {e}")
        return None
    except ValueError as e:
        print(f"Erreur de décodage JSON : {e}")
        return None

def collecter_donnees(noms_stations,Te,duree):
    start_time=time.time()
    fichiers={}
    for nom_station in noms_stations:
        nom_fichier=f"{nom_station}.txt"
        if not os.path.exists(nom_fichier):
            with open(nom_fichier,'w') as fichier:
                fichier.write("")
        fichiers[nom_station]=open(nom_fichier,'a')
        time.sleep(Te)
    for fichier in fichiers.values():
        fichier.close()
    print("Les données ont été sauvegardées dans les fichiers correspondants.")

def principal():
    liste_stations=obtenir_liste_stations()
    if not liste_stations:
        print("Aucune station disponible.")
        return
    print("Liste des stations Vélomagg disponibles :")
    for i,station in enumerate(liste_stations):
        print(f"{i+1}: {station}")
    print("0: Toutes les stations")
    choix=input("Entrez le numéro de la station que vous souhaitez étudier ou 0 pour toutes les stations : ")
    if choix=='0':
        noms_stations=liste_stations
    else:
        choix_stations=[int(x.strip())-1 for x in choix.split(',')]
        if any(choix<0 or choix>=len(liste_stations) for choix in choix_stations):
            print("Numéro de station invalide.")
            return
        noms_stations=[liste_stations[choix] for choix in choix_stations]
        
    Te=2
    duree=10
    collecter_donnees(noms_stations,Te,duree)

if __name__=="__main__":
    principal()
