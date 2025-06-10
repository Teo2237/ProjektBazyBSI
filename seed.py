#!/workspaces/.venv/bin/python
import os
from pymongo import MongoClient

# Pobierz URI do połączenia z MongoDB ze zmiennej środowiskowej,
# tak samo jak w głównej aplikacji Flask.
MONGO_URI = os.environ.get("MONGO_URI")
# MONGO_URI = "mongodb://mongo:mongo@mongo:27017"

# Dane do wstawienia do bazy
GAMES_DATA = [
  {
    "title": "The Witcher 3: Wild Hunt",
    "description": "Jako profesjonalny łowca potworów, Geralt z Rivii, musisz odnaleźć Dziecko Niespodziankę w rozległym świecie pełnym miast handlowych, wysp piratów, niebezpiecznych górskich przełęczy i zapomnianych jaskiń.",
    "release_date": "2015-05-19T00:00:00.000Z",
    "publisher": "CD Projekt",
    "developer": "CD Projekt Red",
    "platforms": ["PC", "PlayStation 4", "Xbox One", "Nintendo Switch", "PlayStation 5", "Xbox Series X/S"],
    "genres": ["Akcja", "RPG", "Fantasy"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/6/326435937.jpg",
    "screenshots": []
  },
  {
    "title": "Cyberpunk 2077",
    "description": "Cyberpunk 2077 to osadzona w otwartym świecie przygoda, której akcja toczy się w Night City, megalopolis rządzonym przez obsesyjną pogoń za władzą, sławą i modyfikowaniem ciała.",
    "release_date": "2020-12-10T00:00:00.000Z",
    "publisher": "CD Projekt",
    "developer": "CD Projekt Red",
    "platforms": ["PC", "PlayStation 4", "Xbox One", "PlayStation 5", "Xbox Series X/S"],
    "genres": ["RPG", "Akcja", "Sci-Fi"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/8/481288593.jpg",
    "screenshots": []
  },
  {
    "title": "Red Dead Redemption 2",
    "description": "Ameryka, rok 1899. Era Dzikiego Zachodu chyli się ku końcowi. Po nieudanym napadzie w mieście Blackwater, Arthur Morgan i gang van der Lindego muszą uciekać.",
    "release_date": "2018-10-26T00:00:00.000Z",
    "publisher": "Rockstar Games",
    "developer": "Rockstar Studios",
    "platforms": ["PlayStation 4", "Xbox One", "PC"],
    "genres": ["Akcja", "Przygoda", "Western"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/8/481351578.jpg",
    "screenshots": []
  },
  {
    "title": "The Last of Us Part I",
    "description": "Remake gry z 2013 roku. W spustoszonym przez cywilizację świecie, gdzie szaleje zaraza i grasują niebezpieczni ocaleńcy, doświadczony przez życie Joel podejmuje się eskorty 14-letniej Ellie.",
    "release_date": "2022-09-02T00:00:00.000Z",
    "publisher": "Sony Interactive Entertainment",
    "developer": "Naughty Dog",
    "platforms": ["PlayStation 5", "PC"],
    "genres": ["Akcja", "Przygoda", "Horror"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/11/530595343.jpg",
    "screenshots": []
  },
  {
    "title": "Elden Ring",
    "description": "Wstań, zmatowieńcze, i pozwól, by łaska wskazała ci drogę. Stań przed Eldeńskim Kręgiem i zostań Eldeńskim Władcą w Krainach Pomiędzy.",
    "release_date": "2022-02-25T00:00:00.000Z",
    "publisher": "Bandai Namco Entertainment",
    "developer": "FromSoftware",
    "platforms": ["PC", "PlayStation 4", "Xbox One", "PlayStation 5", "Xbox Series X/S"],
    "genres": ["Akcja", "RPG", "Dark Fantasy"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/10/506351531.jpg",
    "screenshots": []
  },
  {
    "title": "God of War Ragnarök",
    "description": "Kratos i Atreus muszą udać się do każdego z dziewięciu światów w poszukiwaniu odpowiedzi, przygotowując się na przepowiedzianą bitwę, która ma zakończyć świat.",
    "release_date": "2022-11-09T00:00:00.000Z",
    "publisher": "Sony Interactive Entertainment",
    "developer": "Santa Monica Studio",
    "platforms": ["PlayStation 4", "PlayStation 5", "PC"],
    "genres": ["Akcja", "Przygoda", "Hack and slash"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/11/530520625.jpg",
    "screenshots": []
  },
  {
    "title": "Baldur's Gate 3",
    "description": "Zbierz swoją drużynę i wróć do Zapomnianych Krain w opowieści o przyjaźni i zdradzie, przetrwaniu i poświęceniu, i pokusie absolutnej władzy.",
    "release_date": "2023-08-03T00:00:00.000Z",
    "publisher": "Larian Studios",
    "developer": "Larian Studios",
    "platforms": ["PC", "PlayStation 5", "Xbox Series X/S"],
    "genres": ["RPG", "Strategia", "Fantasy"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/11/530602062.jpg",
    "screenshots": []
  },
  {
    "title": "Starfield",
    "description": "Starfield to stworzona przez Bethesda Game Studios, wielokrotnie nagradzanych twórców The Elder Scrolls V: Skyrim i Fallouta 4, pierwsza nowa marka od ponad 25 lat.",
    "release_date": "2023-09-06T00:00:00.000Z",
    "publisher": "Bethesda Softworks",
    "developer": "Bethesda Game Studios",
    "platforms": ["PC", "Xbox Series X/S"],
    "genres": ["RPG", "Akcja", "Sci-Fi"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/10/506354968.jpg",
    "screenshots": []
  },
  {
    "title": "Alan Wake 2",
    "description": "Seria rytualnych morderstw zagraża Bright Falls. Saga Anderson, agentka FBI, przybywa, by zbadać sprawę. W tym samym czasie Alan Wake pisze mroczną opowieść, by ukształtować rzeczywistość i uciec z więzienia.",
    "release_date": "2023-10-27T00:00:00.000Z",
    "publisher": "Epic Games Publishing",
    "developer": "Remedy Entertainment",
    "platforms": ["PC", "PlayStation 5", "Xbox Series X/S"],
    "genres": ["Survival horror", "Akcja"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/12/564344406.jpg",
    "screenshots": []
  },
  {
    "title": "Diablo IV",
    "description": "Diablo IV to fabularna gra akcji nowej generacji, w której na graczy czekają niezliczone zastępy zła do pokonania, moc umiejętności do opanowania, mrożące krew w żyłach podziemia i legendarna zdobycz.",
    "release_date": "2023-06-05T00:00:00.000Z",
    "publisher": "Blizzard Entertainment",
    "developer": "Blizzard Team 3",
    "platforms": ["PC", "PlayStation 4", "PlayStation 5", "Xbox One", "Xbox Series X/S"],
    "genres": ["Action RPG", "Hack and slash"],
    "cover_image_url": "https://cdn.gracza.pl/i/h/10/506351000.jpg",
    "screenshots": []
  }
]

def seed_database():
    """Główna funkcja do wypełniania bazy danych."""
    try:
        print("Łączenie z bazą danych...")
        client = MongoClient(MONGO_URI)
        db = client.gamesDB
        games_collection = db.games
        print("Połączenie udane.")

        # Sprawdź, czy kolekcja jest pusta, aby uniknąć duplikowania danych
        if games_collection.count_documents({}) == 0:
            print("Baza danych jest pusta. Wypełnianie danymi...")
            games_collection.insert_many(GAMES_DATA)
            print("Wypełnianie bazy danych zakończone.")
        else:
            print("Baza danych już zawiera dane. Pomijanie wypełniania.")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
    finally:
        if 'client' in locals():
            client.close()
            print("Połączenie z bazą danych zostało zamknięte.")

if __name__ == "__main__":
    seed_database()