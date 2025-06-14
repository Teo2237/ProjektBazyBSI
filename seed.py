#!/workspaces/.venv/bin/python
import os
from pymongo import MongoClient, UpdateOne

# Połączenie z MongoDB
client = MongoClient(os.environ.get("MONGO_URI")) 
db = client.gamesDB
games_collection = db.games

# UWAGA: Celowo usunęliśmy linię `games_collection.delete_many({})`,
# aby skrypt nie kasował istniejących danych.

# Dane, które chcemy wstawić lub zaktualizować
games_data = [
    {
        "title": "The Witcher 3: Wild Hunt",
        "release_date": "2015-05-19",
        "genres": ["RPG", "Akcja", "Fantasy"],
        "developer": "CD Projekt Red",
        "publisher": "CD Projekt",
        "description": "Jako wiedźmin Geralt, musisz odnaleźć Dziecko Niespodziankę w rozległym, otwartym świecie pełnym potworów i niebezpieczeństw.",
        "cover_image": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg?t=1704991122",
        "screenshots": [
            "https://cdn.akamai.steamstatic.com/steam/apps/292030/ss_1132274435835820563c87f4a233622474581423.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/292030/ss_c56b6812895690623de8785634289745428383e5.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/292030/ss_81e5953062363e15779cb03025642a4c90e96455.1920x1080.jpg"
        ],
        "youtube_trailer_id": "c0i88t0Kacs"
    },
    {
        "title": "Cyberpunk 2077",
        "release_date": "2020-12-10",
        "genres": ["RPG", "Akcja", "Sci-Fi"],
        "developer": "CD Projekt Red",
        "publisher": "CD Projekt",
        "description": "Cyberpunk 2077 to gra akcji z otwartym światem, osadzona w Night City, megalopolis rządzonym przez obsesyjną pogoń za władzą, sławą i modyfikacjami ciała.",
        "cover_image": "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg?t=1717508383",
        "screenshots": [
            "https://cdn.akamai.steamstatic.com/steam/apps/1091500/ss_1395f95201145947a06400d1ec39512398687299.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1091500/ss_a4394545560a89456e308f4c02da867901966d51.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1091500/ss_914b4342267562092549243a859a8598a2829289.1920x1080.jpg"
        ],
        "youtube_trailer_id": "8X2kIfS6fb8"
    },
    # Możesz tu dodawać kolejne gry, które chcesz mieć w bazie "na starcie"
]

# Przygotowanie listy operacji do wykonania na bazie danych
operations = []
for game_doc in games_data:
    # Tworzymy operację typu "UpdateOne"
    # Filtr `{ 'title': game_doc['title'] }` znajdzie grę po tytule.
    # `$set: game_doc` zaktualizuje wszystkie pola dokumentu danymi z pliku.
    # `upsert=True` to kluczowa opcja: jeśli gra nie zostanie znaleziona, zostanie utworzona.
    operation = UpdateOne(
        { "title": game_doc["title"] },
        { "$set": game_doc },
        upsert=True
    )
    operations.append(operation)

# Wykonanie wszystkich operacji za jednym razem (jest to bardziej wydajne)
if operations:
    result = games_collection.bulk_write(operations)
    print("Operacje na bazie danych zakończone.")
    print(f"Nowo wstawione dokumenty: {result.upserted_count}")
    print(f"Zaktualizowane dokumenty: {result.modified_count}")
else:
    print("Brak danych w skrypcie do przetworzenia.")