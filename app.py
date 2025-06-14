from flask import Flask, jsonify, render_template, abort, request, session, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import math
from functools import wraps # Potrzebne do stworzenia dekoratora

app = Flask(__name__)

# --- Połączenie z MongoDB ---
client = MongoClient(os.environ.get("MONGO_URI")) 
db = client.gamesDB
# Krok 2: Konfiguracja sekretnego klucza dla sesji
# W prawdziwej aplikacji klucz ten powinien być bardziej złożony i przechowywany w bezpiecznym miejscu
app.secret_key = 'bardzo-tajny-klucz-do-zmiany'

# Ustawienie stałych danych logowania (w praktyce powinny być np. w zmiennych środowiskowych)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

# Krok 4: Stworzenie dekoratora do zabezpieczania tras
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            # Dla zapytań API zwracamy błąd, dla stron - przekierowujemy
            if request.path.startswith('/api/admin'):
                return jsonify({'error': 'Wymagana autoryzacja'}), 401
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# === NOWE TRASY LOGOWANIA ===

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = 'Nieprawidłowy login lub hasło'
    # Jeśli metoda to GET lub logowanie nie powiodło się, wyświetl formularz
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


# === ENDPOINTY PUBLICZNE ===
# ... (trasy /, /games/<game_id>, /about, /contact, /faq pozostają bez zmian) ...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/faq')
def faq_page():
    return render_template('faq.html')


# === ZABEZPIECZONE ENDPOINTY ADMINISTRACYJNE ===

@app.route('/admin')
@login_required  # Zastosowanie dekoratora
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
@login_required
def add_game():
    if not request.json or not 'title' in request.json:
        abort(400, description="Missing 'title' in request body.")
    
    new_game_data = request.get_json()
    
    # Przetwarzanie pola screenshots z bloku tekstu na tablicę URL-i
    if 'screenshots' in new_game_data and isinstance(new_game_data['screenshots'], str):
        new_game_data['screenshots'] = [url.strip() for url in new_game_data['screenshots'].splitlines() if url.strip()]
    
    result = db.games.insert_one(new_game_data)
    created_game = db.games.find_one({'_id': result.inserted_id})
    created_game['_id'] = str(created_game['_id'])
    return jsonify(created_game), 201

@app.route('/api/admin/games/<game_id>', methods=['PUT'])
@login_required
def update_game(game_id):
    if not request.json:
        abort(400, description="Request body cannot be empty.")
    try:
        obj_id = ObjectId(game_id)
    except Exception:
        abort(400, description="Invalid ID format.")
        
    update_data = request.get_json()
    update_data.pop('_id', None)

    # Przetwarzanie pola screenshots z bloku tekstu na tablicę URL-i
    if 'screenshots' in update_data and isinstance(update_data['screenshots'], str):
        update_data['screenshots'] = [url.strip() for url in update_data['screenshots'].splitlines() if url.strip()]

    result = db.games.update_one({'_id': obj_id}, {'$set': update_data})
    
    if result.matched_count == 0:
        abort(404, description="Game not found.")
        
    updated_game = db.games.find_one({'_id': obj_id})
    updated_game['_id'] = str(updated_game['_id'])
    
    return jsonify(updated_game)

@app.route('/api/admin/games/<game_id>', methods=['DELETE'])
@login_required # Zastosowanie dekoratora
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)