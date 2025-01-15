from flask import Flask, render_template, request, jsonify
import requests
from geopy.distance import geodesic

app = Flask(__name__)

# Fonction pour obtenir la liste des parkings avec des places disponibles
def obtenir_liste_parkings():
    reponse = requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    donnees = reponse.json()
    parkings = [(parking['name']['value'], parking['location']['value']['coordinates'], parking['availableSpotNumber']['value'], parking['totalSpotNumber']['value']) for parking in donnees if parking['availableSpotNumber']['value'] > 0]
    print("Parkings:", parkings)  # Ajoutez cette ligne pour vérifier les coordonnées des parkings
    return parkings

# Fonction pour obtenir la liste des stations de vélos
def obtenir_liste_stations():
    reponse = requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
    donnees = reponse.json()
    stations = [(station['address']['value']['streetAddress'], station['location']['value']['coordinates'], station['availableBikeNumber']['value'], station['totalSlotNumber']['value']) for station in donnees]
    print("Stations:", stations)  # Ajoutez cette ligne pour vérifier les coordonnées des stations de vélos
    return stations

# Fonction pour calculer le trajet et le temps entre deux points
def calculer_trajet(coordinates1, coordinates2):
    url = f"http://router.project-osrm.org/route/v1/driving/{coordinates1[0]},{coordinates1[1]};{coordinates2[0]},{coordinates2[1]}?overview=false"
    response = requests.get(url)
    data = response.json()
    if data.get('routes'):
        route = data['routes'][0]
        distance = route['distance']
        duration = route['duration']
        return distance, duration
    return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parkings')
def parkings():
    parkings = obtenir_liste_parkings()
    return jsonify(parkings)

@app.route('/stations')
def stations():
    stations = obtenir_liste_stations()
    return jsonify(stations)

@app.route('/nearest_station', methods=['POST'])
def nearest_station():
    data = request.json
    lat = data['lat']
    lon = data['lon']
    stations = obtenir_liste_stations()
    nearest_station = None
    min_distance = float('inf')

    # Filtrer les stations avec des vélos disponibles
    available_stations = [station for station in stations if station[2] > 0]

    for station in available_stations:
        station_coords = (station[1][1], station[1][0])
        parking_coords = (lat, lon)
        distance = geodesic(parking_coords, station_coords).meters
        if distance < min_distance:
            min_distance = distance
            nearest_station = station

    if nearest_station:
        distance, duration = calculer_trajet((lon, lat), (nearest_station[1][0], nearest_station[1][1]))
        return jsonify({
            'name': nearest_station[0],
            'coordinates': nearest_station[1],
            'available_bikes': nearest_station[2],
            'distance': distance,
            'duration': duration
        })
    else:
        return jsonify({'error': 'Aucune station de vélos avec des vélos disponibles trouvée'}), 404

if __name__ == '__main__':
    app.run(debug=True)
