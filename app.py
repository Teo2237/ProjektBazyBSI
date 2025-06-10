from flask import Flask, jsonify, render_template, abort, request
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

# --- ZMODYFIKOWANY ENDPOINT - ZADANIE 2.3 ---
@app.route('/api/games', methods=['GET'])
def get_games():
    """
    Zwraca listę wszystkich gier z bazy danych.
    Obsługuje filtrowanie po gatunku (np. ?genre=RPG)
    oraz sortowanie (np. ?sort=title lub ?sort=-release_date).
    """
    games_collection = db.games
    query_filter = {}
    sort_criteria = []

    # Krok 1: Implementacja filtrowania po gatunku
    genre_param = request.args.get('genre')
    if genre_param:
        # Dodajemy warunek do słownika z filtrami.
        # Znajdzie gry, które w tablicy 'genres' mają podaną wartość.
        query_filter['genres'] = genre_param

    # Krok 2: Implementacja sortowania
    sort_param = request.args.get('sort')
    if sort_param:
        sort_field = sort_param
        # Domyślnie sortujemy rosnąco (wartość 1 w MongoDB)
        sort_order = 1
        
        # Jeśli parametr zaczyna się od '-', sortujemy malejąco
        if sort_param.startswith('-'):
            # Wartość -1 w MongoDB oznacza sortowanie malejące
            sort_order = -1
            # Usuwamy '-' z nazwy pola do sortowania
            sort_field = sort_param[1:]
        
        # Upewniamy się, że sortowanie odbywa się po dozwolonych polach
        if sort_field in ['title', 'release_date']:
            sort_criteria.append((sort_field, sort_order))

    # Budujemy zapytanie - najpierw filtrujemy...
    cursor = games_collection.find(query_filter)

    # ...a następnie, jeśli zdefiniowano sortowanie, dodajemy je do zapytania
    if sort_criteria:
        cursor = cursor.sort(sort_criteria)
    
    games_list = []
    for game in cursor:
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