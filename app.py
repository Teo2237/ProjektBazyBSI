from flask import Flask, jsonify, render_template, abort, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# --- Połączenie z MongoDB ---
client = MongoClient(os.environ.get("MONGO_URI")) 
db = client.gamesDB

# === ENDPOINTY PUBLICZNE ===

@app.route('/')
def index():
    """Serwuje główną stronę aplikacji."""
    return render_template('index.html')

@app.route('/admin')
def admin_panel():
    """Serwuje stronę panelu administracyjnego."""
    return render_template('admin.html')

# --- NOWA TRASA DLA STRONY SZCZEGÓŁÓW GRY (Faza 2) ---
@app.route('/games/<game_id>')
def game_details_page(game_id):
    """
    Serwuje dedykowaną stronę dla pojedynczej gry.
    Zmienna 'game_id' nie jest tu używana, ale jest częścią wzorca URL.
    JavaScript na stronie docelowej użyje jej do pobrania danych z API.
    """
    return render_template('game_details.html')
# --- Koniec nowego fragmentu ---

@app.route('/api/games', methods=['GET'])
def get_games():
    """Zwraca listę wszystkich gier z opcją filtrowania i sortowania."""
    games_collection = db.games
    query_filter = {}
    sort_criteria = []

    genre_param = request.args.get('genre')
    if genre_param:
        query_filter['genres'] = genre_param

    sort_param = request.args.get('sort')
    if sort_param:
        sort_field = sort_param.strip()
        sort_order = 1
        if sort_field.startswith('-'):
            sort_order = -1
            sort_field = sort_field[1:]
        if sort_field in ['title', 'release_date']:
            sort_criteria.append((sort_field, sort_order))

    cursor = games_collection.find(query_filter)
    if sort_criteria:
        cursor = cursor.sort(sort_criteria)
    
    games_list = [game for game in cursor]
    for game in games_list:
        game['_id'] = str(game['_id'])
        
    return jsonify(games_list)

@app.route('/api/games/<game_id>', methods=['GET'])
def get_game_details(game_id):
    """Zwraca szczegółowe dane jednej gry na podstawie jej ID."""
    games_collection = db.games
    try:
        obj_id = ObjectId(game_id)
    except Exception:
        abort(400, description="Invalid ID format.")

    game = games_collection.find_one({'_id': obj_id})
    if game:
        game['_id'] = str(game['_id'])
        return jsonify(game)
    else:
        abort(404, description="Game not found.")

# === ENDPOINTY ADMINISTRACYJNE (CRUD) ===
# ... (reszta kodu bez zmian) ...
@app.route('/api/admin/games', methods=['POST'])
def add_game():
    """Dodaje nową grę do bazy danych (operacja INSERT)."""
    if not request.json or not 'title' in request.json:
        abort(400, description="Missing 'title' in request body.")
    
    new_game_data = request.get_json()
    games_collection = db.games
    result = games_collection.insert_one(new_game_data)
    created_game = games_collection.find_one({'_id': result.inserted_id})
    created_game['_id'] = str(created_game['_id'])
    return jsonify(created_game), 201

@app.route('/api/admin/games/<game_id>', methods=['PUT'])
def update_game(game_id):
    """Aktualizuje istniejącą grę (operacja UPDATE)."""
    if not request.json:
        abort(400, description="Request body cannot be empty.")
    try:
        obj_id = ObjectId(game_id)
    except Exception:
        abort(400, description="Invalid ID format.")
    update_data = request.get_json()
    update_data.pop('_id', None)
    result = db.games.update_one({'_id': obj_id}, {'$set': update_data})
    if result.matched_count == 0:
        abort(404, description="Game not found.")
    updated_game = db.games.find_one({'_id': obj_id})
    updated_game['_id'] = str(updated_game['_id'])
    return jsonify(updated_game)

@app.route('/api/admin/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Usuwa grę z bazy danych (operacja DELETE)."""
    try:
        obj_id = ObjectId(game_id)
    except Exception:
        abort(400, description="Invalid ID format.")
    result = db.games.delete_one({'_id': obj_id})
    if result.deleted_count == 0:
        abort(404, description="Game not found.")
    return jsonify({'message': 'Game deleted successfully'})

@app.route('/about')
def about_page():
    """Serwuje stronę 'O nas'."""
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    """Serwuje stronę 'Kontakt'."""
    return render_template('contact.html')

@app.route('/faq')
def faq_page():
    """Serwuje stronę 'FAQ'."""
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)