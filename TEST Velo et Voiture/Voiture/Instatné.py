import requests
import time
import os

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

def afficher_etat_parking(nom_parking):
    donnees_parking = obtenir_donnees_parking(nom_parking)
    if donnees_parking:
        places_libres = donnees_parking['availableSpotNumber']['value']
        total_places = donnees_parking['totalSpotNumber']['value']
        places_occupees = min(total_places - places_libres, total_places)
        status = donnees_parking.get('status', {'value': 'Unknown'})['value']
        is_open = "Ouvert" if status == "Open" else "Fermé" if status == "Closed" else "Inconnu"
        print(f"Parking: {nom_parking}")
        print(f"Places occupées: {places_occupees} sur {total_places} total")
        print(f"Statut: {is_open}")
    else:
        print(f"Parking '{nom_parking}' non trouvé")

def collecter_donnees(noms_parkings, Te, duree):
    start_time = time.time()
    fichiers = {}
    for nom_parking in noms_parkings:
        nom_fichier = f"{nom_parking}.txt"
        if not os.path.exists(nom_fichier):
            with open(nom_fichier, 'w') as fichier:
                fichier.write("")
        fichiers[nom_parking] = open(nom_fichier, 'a')
    while (time.time() - start_time) < duree:
        for nom_parking in noms_parkings:
            donnees_parking = obtenir_donnees_parking(nom_parking)
            if donnees_parking:
                horodatage = int(time.time())
                places_libres = donnees_parking['availableSpotNumber']['value']
                total_places = donnees_parking['totalSpotNumber']['value']
                places_occupees = min(total_places - places_libres, total_places)
                status = donnees_parking.get('status', {'value': 'Unknown'})['value']
                is_open = "Ouvert" if status == "Open" else "Fermé" if status == "Closed" else "Inconnu"
                fichiers[nom_parking].write(f"{horodatage}: {places_occupees} places occupées sur {total_places} total, Parking: {is_open}\n")
            else:
                fichiers[nom_parking].write(f"{horodatage}: Parking '{nom_parking}' non trouvé\n")
        time.sleep(Te)
    for fichier in fichiers.values():
        fichier.close()
    print("Les données ont été sauvegardées dans les fichiers correspondants.")

def principal():
    liste_parkings = obtenir_liste_parkings()
    print("Liste des parkings disponibles :")
    for i, parking in enumerate(liste_parkings):
        print(f"{i+1}: {parking}")
    print("0: Tous les parkings")

    while True:
        choix = input("Entrez le numéro du parking pour voir son état actuel ou 'q' pour quitter : ")
        if choix.lower() == 'q':
            break
        try:
            choix = int(choix)
            if choix == 0:
                for parking in liste_parkings:
                    afficher_etat_parking(parking)
            elif 1 <= choix <= len(liste_parkings):
                afficher_etat_parking(liste_parkings[choix - 1])
            else:
                print("Numéro de parking invalide.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro ou 'q' pour quitter.")

if __name__ == "__main__":
    principal()
