import requests
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Définir les dates de début et de fin pour l'année 2024
start_date = "2024-01-01T00:00:00"
end_date = "2024-12-31T23:59:59"

# Dictionnaire pour mapper les IDs des stations aux noms des parkings
station_names = {
    "001": "Gare Saint-Roch",
    "002": "Comédie",
    "003": "Corum",
    "004": "Antigone",
    "005": "Place de la Comédie",
    "006": "Esplanade Charles de Gaulle",
    "007": "Place Carnot",
    "008": "Place de la Canourgue",
    "009": "Place des Martyrs de la Résistance",
    "010": "Place Jean Jaurès",
    "011": "Place Albert 1er",
    "012": "Place de la République",
    "013": "Place de la Victoire",
    "014": "Place de la Liberté",
    "015": "Place de la Paix",
    "016": "Place de la Gare",
    "017": "Place de la Préfecture",
    "018": "Place de la Mairie",
    "019": "Place de la Cathédrale",
    "020": "Place de la Chapelle",
    "021": "Place de la Fontaine",
    "022": "Place de la Croix",
    "023": "Place de la Poste",
    "024": "Place de la République",
    "025": "Place de la Victoire",
    "026": "Place de la Liberté",
    "027": "Place de la Paix",
    "028": "Place de la Gare",
    "029": "Place de la Préfecture",
    "030": "Place de la Mairie",
    "031": "Place de la Cathédrale",
    "032": "Place de la Chapelle",
    "033": "Place de la Fontaine",
    "034": "Place de la Croix",
    "035": "Place de la Poste",
    "036": "Place de la République",
    "037": "Place de la Victoire",
    "038": "Place de la Liberté",
    "039": "Place de la Paix",
    "040": "Place de la Gare",
    "041": "Place de la Préfecture",
    "042": "Place de la Mairie",
    "043": "Place de la Cathédrale",
    "044": "Place de la Chapelle",
    "045": "Place de la Fontaine",
    "046": "Place de la Croix",
    "047": "Place de la Poste",
    "048": "Place de la République",
    "049": "Place de la Victoire",
    "050": "Place de la Liberté",
    "051": "Place de la Paix",
    "052": "Place de la Gare",
    "053": "Place de la Préfecture",
    "054": "Place de la Mairie",
    "055": "Place de la Cathédrale",
    "056": "Place de la Chapelle",
    "057": "Place de la Fontaine",
    "058": "Place de la Croix",
    "059": "Place de la Poste",
    "060": "Place de la République",
    "061": "Place de la Victoire",
    "062": "Place de la Liberté"
}

# Fonction pour récupérer les données d'une station
def get_station_data(station_id):
    url = f"https://portail-api-data.montpellier3m.fr/bikestation_timeseries/urn%3Angsi-ld%3Astation%3A{station_id}/attrs/availableBikeNumber?fromDate={start_date}&toDate={end_date}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for station {station_id}")
        return None

# Fonction pour convertir le timestamp ISO 8601 en format "Heure:minutes:secondes jour/mois/année"
def format_timestamp(timestamp):
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return dt.strftime("%H:%M:%S %d/%m/%Y")

# Fonction pour enregistrer les données dans un fichier .txt
def save_to_txt(station_id, station_name, data, total_places):
    filename = f"station_{station_id}.txt"
    with open(filename, 'w') as file:
        for timestamp, available_bikes in zip(data['index'], data['values']):
            formatted_timestamp = format_timestamp(timestamp)
            occupied_places = total_places - available_bikes
            parking_status = "ouvert" if available_bikes > 0 else "fermé"
            percentage_full = (occupied_places / total_places) * 100
            file.write(f"{station_name} le {formatted_timestamp}, a {occupied_places}/{total_places} place occupées, Statut : {parking_status}, {percentage_full:.2f}% de remplissage\n")

# Fonction pour créer un graphique pour une station
def create_graph(station_id, station_name, data, total_places):
    timestamps = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in data['index']]
    available_bikes = data['values']
    occupied_places = [total_places - bikes for bikes in available_bikes]

    plt.figure(figsize=(15, 8))
    plt.plot(timestamps, occupied_places, label=f'{station_name}')
    plt.xlabel('Date')
    plt.ylabel('Places Occupées')
    plt.title(f'Occupation des places à {station_name} en 2024')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=7))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gcf().autofmt_xdate()
    plt.savefig(f"Graphique_{station_name}.png")
    plt.close()

# Fonction pour créer un graphique global
def create_global_graph(all_data, total_places):
    plt.figure(figsize=(15, 10))
    for station_id, data in all_data.items():
        station_name = station_names.get(station_id, f"Unknown Station {station_id}")
        timestamps = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in data['index']]
        available_bikes = data['values']
        occupied_places = [total_places - bikes for bikes in available_bikes]
        plt.plot(timestamps, occupied_places, label=f'{station_name}')

    plt.xlabel('Date')
    plt.ylabel('Places Occupées')
    plt.title('Occupation des places dans tous les parkings en 2024')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=7))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gcf().autofmt_xdate()
    plt.savefig("Graphique_Global.png")
    plt.close()

# Boucle pour récupérer et enregistrer les données de chaque station
all_data = {}
for station_id in range(1, 63):  # Les IDs de station vont de 001 à 062
    station_id_str = f"{station_id:03}"  # Formatage pour avoir 3 chiffres
    station_name = station_names.get(station_id_str, f"Unknown Station {station_id_str}")
    data = get_station_data(station_id_str)
    if data:
        # Vérifier la structure de la réponse JSON
        if 'index' in data and 'values' in data:
            # Supposons que chaque station a un total de 239 places (à ajuster si nécessaire)
            total_places = 239
            save_to_txt(station_id_str, station_name, data, total_places)
            create_graph(station_id_str, station_name, data, total_places)
            all_data[station_id_str] = data
        else:
            print(f"Unexpected data format for station {station_id_str}: {json.dumps(data)}")

# Créer le graphique global
create_global_graph(all_data, 239)

print("Data retrieval, saving, and graph creation completed.")
