#!/workspaces/.venv/bin/python
import os
from pymongo import MongoClient, UpdateOne

# Połączenie z MongoDB
client = MongoClient(os.environ.get("MONGO_URI")) 
db = client.gamesDB
games_collection = db.games


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
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/292030/ss_5710298af2318afd9aa72449ef29ac4a2ef64d8e.jpg?t=1749199563",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/292030/ss_0901e64e9d4b8ebaea8348c194e7a3644d2d832d.jpg?t=1749199563",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/292030/ss_112b1e176c1bd271d8a565eacb6feaf90f240bb2.1920x1080.jpg?t=1749199563"
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
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_2f649b68d579bf87011487d29bc4ccbfdd97d34f.jpg?t=1749198613",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_b529b0abc43f55fc23fe8058eddb6e37c9629a6a.1920x1080.jpg?t=1749198613",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/ss_8640d9db74f7cad714f6ecfb0e1aceaa3f887e58.1920x1080.jpg?t=1749198613"
        ],
        "youtube_trailer_id": "8X2kIfS6fb8"
    },
    {
        "title": "Red Dead Redemption 2",
        "description": "Ameryka, rok 1899. Era Dzikiego Zachodu chyli się ku końcowi. Po nieudanym napadzie w mieście Blackwater, Arthur Morgan i gang van der Lindego muszą uciekać.",
        "release_date": "2018-10-26",
        "publisher": "Rockstar Games",
        "developer": "Rockstar Studios",
        "platforms": ["PlayStation 4", "Xbox One", "PC"],
        "genres": ["Akcja", "Przygoda", "Western"],
        "cover_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1174180/header.jpg?t=1720558643",
        "screenshots": [
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1174180/ss_66b553f4c209476d3e4ce25fa4714002cc914c4f.jpg?t=1720558643",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1174180/ss_bac60bacbf5da8945103648c08d27d5e202444ca.jpg?t=1720558643",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1174180/ss_668dafe477743f8b50b818d5bbfcec669e9ba93e.jpg?t=1720558643"
        ],
        "youtube_trailer_id": "gmA6MrX81z4"
   },
   {
        "title": "The Last of Us Part I",
        "description": "Remake gry z 2013 roku. W spustoszonym przez cywilizację świecie, gdzie szaleje zaraza i grasują niebezpieczni ocaleńcy, doświadczony przez życie Joel podejmuje się eskorty 14-letniej Ellie.",
        "release_date": "2022-09-02",
        "publisher": "Sony Interactive Entertainment",
        "developer": "Naughty Dog",
        "platforms": ["PlayStation 5", "PC"],
        "genres": ["Akcja", "Przygoda", "Horror"],
        "cover_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1888930/header.jpg?t=1746041320",
        "screenshots": [
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1888930/ss_3f1805ecddafacee7f61f87cb8e4624435a83ee3.jpg?t=1746041320",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1888930/ss_89fffc2857dcae29dee2a09f1be33d745610e19d.jpg?t=1746041320",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1888930/ss_8cd55ab975b2e47f4d4d9a0da4ae6948040ef807.jpg?t=1746041320"
        ],
        "youtube_trailer_id": "W01L70IGBgE"
   },
   {
        "title": "Elden Ring",
        "description": "Wstań, zmatowieńcze, i pozwól, by łaska wskazała ci drogę. Stań przed Eldeńskim Kręgiem i zostań Eldeńskim Władcą w Krainach Pomiędzy.",
        "release_date": "2022-02-25",
        "publisher": "Bandai Namco Entertainment",
        "developer": "FromSoftware",
        "platforms": ["PC", "PlayStation 4", "Xbox One", "PlayStation 5", "Xbox Series X/S"],
        "genres": ["Akcja", "RPG", "Dark Fantasy"],
        "cover_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg?t=1748630546",
        "screenshots": [
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1245620/ss_943bf6fe62352757d9070c1d33e50b92fe8539f1.jpg?t=1748630546",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1245620/ss_dcdac9e4b26ac0ee5248bfd2967d764fd00cdb42.jpg?t=1748630546",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1245620/ss_3c41384a24d86dddd58a8f61db77f9dc0bfda8b5.jpg?t=1748630546"
        ],
        "youtube_trailer_id": "E3Huy2cdih0"
   },
   {
        "title": "God of War Ragnarök",
        "description": "Kratos i Atreus muszą udać się do każdego z dziewięciu światów w poszukiwaniu odpowiedzi, przygotowując się na przepowiedzianą bitwę, która ma zakończyć świat.",
        "release_date": "2022-11-09",
        "publisher": "Sony Interactive Entertainment",
        "developer": "Santa Monica Studio",
        "platforms": ["PlayStation 4", "PlayStation 5", "PC"],
        "genres": ["Akcja", "Przygoda", "Hack and slash"],
        "cover_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2322010/header.jpg?t=1749837021",
        "screenshots": [
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2322010/ss_05f27139b15c5410d07cd59b7b52adbdf73e13da.jpg?t=1749837021",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2322010/ss_974a7b998c0c14da7fe52a342cf36c98850a57ac.jpg?t=1749837021",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2322010/ss_78350297511e81f287b4bc361935efbc3016f6db.jpg?t=1749837021"
        ],
        "youtube_trailer_id": "hfJ4Km46A-0"
   },
   {
        "title": "Baldur's Gate 3",
        "description": "Zbierz swoją drużynę i wróć do Zapomnianych Krain w opowieści o przyjaźni i zdradzie, przetrwaniu i poświęceniu, i pokusie absolutnej władzy.",
        "release_date": "2023-08-03",
        "publisher": "Larian Studios",
        "developer": "Larian Studios",
        "platforms": ["PC", "PlayStation 5", "Xbox Series X/S"],
        "genres": ["RPG", "Strategia", "Fantasy"],
        "cover_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1086940/48a2fcbda8565bb45025e98fd8ebde8a7203f6a0/header.jpg?t=1748346026",
        "screenshots": [
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1086940/ss_c73bc54415178c07fef85f54ee26621728c77504.jpg?t=1748346026",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1086940/ss_73d93bea842b93914d966622104dcb8c0f42972b.jpg?t=1748346026",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1086940/ss_cf936d31061b58e98e0c646aee00e6030c410cda.jpg?t=1748346026"
        ],
        "youtube_trailer_id": "1T22wNvoNiU"
   },
   {
        "title": "Starfield",
        "description": "Starfield to stworzona przez Bethesda Game Studios, wielokrotnie nagradzanych twórców The Elder Scrolls V: Skyrim i Fallouta 4, pierwsza nowa marka od ponad 25 lat.",
        "release_date": "2023-09-06",
        "publisher": "Bethesda Softworks",
        "developer": "Bethesda Game Studios",
        "platforms": ["PC", "Xbox Series X/S"],
        "genres": ["RPG", "Akcja", "Sci-Fi"],
        "cover_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1716740/header.jpg?t=1749757928",
        "screenshots": [
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1716740/ss_4887dc140a637684ddcfca518458668409f946dc.jpg?t=1749757928",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1716740/ss_b2821283cb140cd5a6289a8160016b6a60d8f96e.jpg?t=1749757928",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1716740/ss_68f15d580bf91971f637be5e464bc803482d78f7.jpg?t=1749757928"
        ],
        "youtube_trailer_id": "kfYEiTdsyas"
   },
   {
        "title": "Alan Wake 2",
        "description": "Seria rytualnych morderstw zagraża Bright Falls. Saga Anderson, agentka FBI, przybywa, by zbadać sprawę. W tym samym czasie Alan Wake pisze mroczną opowieść, by ukształtować rzeczywistość i uciec z więzienia.",
        "release_date": "2023-10-27",
        "publisher": "Epic Games Publishing",
        "developer": "Remedy Entertainment",
        "platforms": ["PC", "PlayStation 5", "Xbox Series X/S"],
        "genres": ["Survival horror", "Akcja"],
        "cover_image": "https://cdn1.epicgames.com/offer/c4763f236d08423eb47b4c3008779c84/EGS_AlanWake2_RemedyEntertainment_S1_2560x1440-ec44404c0b41bc457cb94cd72cf85872",
        "screenshots": [
            "https://i.ytimg.com/vi/aAc8xQckYQw/maxresdefault.jpg",
            "https://cdn2.unrealengine.com/alan-wake-2-our-guide-to-surviving-the-horrors-within-break-1920x1080-7dab7b6fbe2f.jpg",
            "https://cdn2.unrealengine.com/the-first-gameplay-preview-of-alan-wake-2-1920x1080-6cd1f0e9b2df.jpg"
        ],
        "youtube_trailer_id": "dlQ3FeNu5Yw"
   },
   {
        "title": "Diablo IV",
        "description": "Diablo IV to fabularna gra akcji nowej generacji, w której na graczy czekają niezliczone zastępy zła do pokonania, moc umiejętności do opanowania, mrożące krew w żyłach podziemia i legendarna zdobycz.",
        "release_date": "2023-06-05",
        "publisher": "Blizzard Entertainment",
        "developer": "Blizzard Team 3",
        "platforms": ["PC", "PlayStation 4", "PlayStation 5", "Xbox One", "Xbox Series X/S"],
        "genres": ["Action RPG", "Hack and slash"],
        "cover_image": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2344520/header.jpg?t=1745947729",
        "screenshots": [
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2344520/17bb72fc846ce4a7abfa894e31a635553c86100b/ss_17bb72fc846ce4a7abfa894e31a635553c86100b.jpg?t=1745947729",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2344520/3de243799add7eb72ebee2cf60a64943d63ea5e5/ss_3de243799add7eb72ebee2cf60a64943d63ea5e5.jpg?t=1745947729",
            "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2344520/77d0df4cb12fac926a126a2baef29cf6ac6383b0/ss_77d0df4cb12fac926a126a2baef29cf6ac6383b0.jpg?t=1745947729"
        ],
        "youtube_trailer_id": "Ro26B394ZBM"
   }
]

# Lista operacji do wykonania na bazie danych
operations = []
for game_doc in games_data:
    # Operację typu "UpdateOne"
    # Filtr `{ 'title': game_doc['title'] }` znajduję grę po tytule.
    # `$set: game_doc` zaktulalizowanie wszystkich pól.
    # `upsert=True` jeżeli gra nie zostanie znalezniona, zostanie utworzona w bazie danych.
    operation = UpdateOne(
        { "title": game_doc["title"] },
        { "$set": game_doc },
        upsert=True
    )
    operations.append(operation)

# Wykonanie wszystkich operacji
if operations:
    result = games_collection.bulk_write(operations)
    print("Operacje na bazie danych zakończone.")
    print(f"Nowo wstawione dokumenty: {result.upserted_count}")
    print(f"Zaktualizowane dokumenty: {result.modified_count}")
else:
    print("Brak danych w skrypcie do przetworzenia.")