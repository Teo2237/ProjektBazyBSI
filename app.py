from flask import Flask, jsonify, render_template, abort
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# --- Połączenie z MongoDB ---
# Używamy nazwy serwisu z docker-compose.yml jako hosta
client = MongoClient(os.environ.get("MONGO_URI")) 
db = client.gamesDB # Nazwa bazy danych

@app.route('/')
def index():
    """
    Serwuje główną stronę aplikacji.
    """
    return render_template('index.html')

@app.route('/api/games', methods=['GET'])
def get_games():
    """
    Zwraca listę wszystkich gier z bazy danych.
    """
    games_collection = db.games
    games_list = []
    for game in games_collection.find({}):
        # Konwersja ObjectId na string, aby był serializowalny do JSON
        game['_id'] = str(game['_id'])
        games_list.append(game)
    return jsonify(games_list)

# --- NOWY ENDPOINT - ZADANIE 2.2 ---
@app.route('/api/games/<game_id>', methods=['GET'])
def get_game_details(game_id):
    """
    Zwraca szczegółowe dane jednej gry na podstawie jej ID.
    """
    games_collection = db.games
    try:
        # Konwertujemy string ID na ObjectId
        obj_id = ObjectId(game_id)
    except Exception:
        # Jeśli podany ID ma niepoprawny format, zwracamy błąd 400 Bad Request
        abort(400, description="Invalid ID format.")

    game = games_collection.find_one({'_id': obj_id})
    
    if game:
        # Jeśli znaleziono grę, konwertujemy jej _id na string i zwracamy dane
        game['_id'] = str(game['_id'])
        return jsonify(game)
    else:
        # Jeśli gra o danym ID nie istnieje, zwracamy błąd 404 Not Found
        abort(404, description="Game not found.")

if __name__ == '__main__':
    # Używamy 0.0.0.0, aby aplikacja była dostępna z zewnątrz kontenera
    app.run(host='0.0.0.0', port=5000, debug=True)