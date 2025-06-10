# Dockerfile

# Krok 1: Wybierz oficjalny obraz Pythona jako bazę
FROM python:3.9-slim

# Krok 2: Ustaw folder roboczy w kontenerze
WORKDIR /app

# Krok 3: Skopiuj plik z zależnościami i zainstaluj je
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Krok 4: Skopiuj resztę kodu aplikacji do folderu roboczego
COPY ./backend /app

# Krok 5: Określ komendę, która uruchomi aplikację
CMD ["flask", "run", "--host=0.0.0.0"]