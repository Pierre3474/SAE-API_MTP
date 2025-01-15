import requests
import time
import os

def obtenir_liste_parkings():
    reponse=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    donnees=reponse.json()
    return [parking['name']['value'] for parking in donnees]

def obtenir_donnees_parking(nom_parking):
    reponse=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    donnees=reponse.json()
    for parking in donnees:
        if parking['name']['value']==nom_parking:
            return parking
    return None

def collecter_donnees(noms_parkings,Te,duree):
    start_time=time.time()
    fichiers={}
    for nom_parking in noms_parkings:
        nom_fichier=f"{nom_parking}.txt"
        if not os.path.exists(nom_fichier):
            with open(nom_fichier,'w') as fichier:
                fichier.write("")
        fichiers[nom_parking]=open(nom_fichier,'a')
    while(time.time()-start_time)<duree:
        for nom_parking in noms_parkings:
            donnees_parking=obtenir_donnees_parking(nom_parking)
            if donnees_parking:
                horodatage=int(time.time())
                places_libres=donnees_parking['availableSpotNumber']['value']
                total_places=donnees_parking['totalSpotNumber']['value']
                places_occupees=min(total_places-places_libres,total_places)
                fichiers[nom_parking].write(f"{horodatage}: {places_occupees} places occupées sur {total_places} total\n")
            else:
                fichiers[nom_parking].write(f"{horodatage}: Parking '{nom_parking}' non trouvé\n")
        time.sleep(Te)
    for fichier in fichiers.values():
        fichier.close()
    print("Les données ont été sauvegardées dans les fichiers correspondants.")

def principal():
    liste_parkings=obtenir_liste_parkings()
    print("Liste des parkings disponibles :")
    for i,parking in enumerate(liste_parkings):
        print(f"{i+1}: {parking}")
    print("0: Tous les parkings")
    choix=input("Entrez le numéro du parking que vous souhaitez étudier ou 0 pour tous les parkings : ")
    if choix=='0':
        noms_parkings=liste_parkings
    else:
        choix_parkings=[int(x.strip())-1 for x in choix.split(',')]
        if any(choix<0 or choix>=len(liste_parkings) for choix in choix_parkings):
            print("Numéro de parking invalide.")
            return
        noms_parkings=[liste_parkings[choix] for choix in choix_parkings]
    Te=2
    duree=10
    collecter_donnees(noms_parkings,Te,duree)

if __name__=="__main__":
    principal()
