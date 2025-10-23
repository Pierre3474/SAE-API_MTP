import requests
import time
import os
import matplotlib.pyplot as plt
import schedule
from datetime import datetime

def obtenir_liste_parkings():
    reponse = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    donnees = reponse.json()
    return [parking['name']['value'] for parking in donnees]

def obtenir_donnees_parking(nom_parking):
    reponse = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    donnees = reponse.json()
    for parking in donnees:
        if parking['name']['value'] == nom_parking:
            return parking
    return None

def lire_donnees_fichier(nom_fichier):
    if not os.path.exists(nom_fichier):
        return [], []
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()
    horodatages = []
    places_occupees = []
    for ligne in lignes:
        parts = ligne.split(': ')
        if len(parts) > 1:
            horodatage = datetime.fromtimestamp(int(parts[0]))
            places = int(parts[1].split(' ')[0])
            horodatages.append(horodatage)
            places_occupees.append(places)
    return horodatages, places_occupees

def generer_graphique(noms_parkings):
    plt.figure(figsize=(10, 6))
    for nom_parking in noms_parkings:
        nom_fichier = f"{nom_parking}.txt"
        horodatages, places_occupees = lire_donnees_fichier(nom_fichier)
        if horodatages and places_occupees:
            plt.plot(horodatages, places_occupees, label=nom_parking)
    plt.xlabel('Temps')
    plt.ylabel('Places occupées')
    plt.title('Évolution des places de parking')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('parking_evolution.png')
    plt.close()

def mise_a_jour_donnees(noms_parkings):
    for nom_parking in noms_parkings:
        donnees_parking = obtenir_donnees_parking(nom_parking)
        if donnees_parking:
            horodatage = int(time.time())
            places_libres = donnees_parking['availableSpotNumber']['value']
            total_places = donnees_parking['totalSpotNumber']['value']
            places_occupees = min(total_places - places_libres, total_places)
            status = donnees_parking.get('status', {'value': 'Unknown'})['value']
            is_open = "Ouvert" if status == "Open" else "Fermé" if status == "Closed" else "Inconnu"
            with open(f"{nom_parking}.txt", 'a') as fichier:
                fichier.write(f"{horodatage}: {places_occupees} places occupées sur {total_places} total, Parking: {is_open}\n")

def mise_a_jour_graphique(noms_parkings):
    mise_a_jour_donnees(noms_parkings)
    generer_graphique(noms_parkings)

def principal():
    liste_parkings = obtenir_liste_parkings()
    print("Liste des parkings disponibles :")
    for i, parking in enumerate(liste_parkings):
        print(f"{i+1}: {parking}")
    print("0: Tous les parkings")
    choix = input("Entrez le numéro du parking que vous souhaitez étudier ou 0 pour tous les parkings : ")
    if choix == '0':
        noms_parkings = liste_parkings
    else:
        choix_parkings = [int(x.strip()) - 1 for x in choix.split(',')]
        if any(choix < 0 or choix >= len(liste_parkings) for choix in choix_parkings):
            print("Numéro de parking invalide.")
            return
        noms_parkings = [liste_parkings[choix] for choix in choix_parkings]

    # Planifier la mise à jour des données et du graphique toutes les 10 minutes
    schedule.every(10).minutes.do(mise_a_jour_graphique, noms_parkings)
    while True:
        schedule.run_pending()
        time.sleep(1)

principal()
