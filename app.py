import os
from flask import Flask, jsonify
from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)
MONGO_URI = "mongodb://mongo:mongo@mongo:27017"
client = MongoClient(MONGO_URI)
db = client.gamesDB

@app.route('/api/games')
def get_games():
    """Endpoint do pobierania listy wszystkich gier."""
    games = db.games.find({})
    # Użyj json_util do poprawnej konwersji danych z MongoDB (np. ObjectId) na JSON
    response = json.loads(json_util.dumps(games))
    return jsonify(response)

# Usunęliśmy domyślny endpoint '/' i render_template,
# skupiamy się na API.